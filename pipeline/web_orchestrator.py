import os
import time
import json
import logging
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Dict, Any, Optional
try:
    import yaml
    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False

from agents.web_scraper import WebScraperAgent, ScrapedWebContent
from agents.subagents.build_parser import BuildParserSubAgent
from agents.subagents.context_parser import ContextParserSubAgent
from agents.subagents.validator import CrossValidatorAgent
from agents.stat_inferrer import StatInferenceAgent
from agents.structurer import BuildStructurer
from agents.knowledge_builder import KnowledgeBuilder

logger = logging.getLogger(__name__)

class WebPipelineOrchestrator:
    """웹사이트 멀티 서브 에이전트 파이프라인 총괄 오케스트레이터"""

    def __init__(self, config_path: str = "config/settings.yaml"):
        self.config = self._load_config(config_path)
        gemini_cfg = self.config.get("gemini", {})
        rag_cfg = self.config.get("rag", {})
        paths_cfg = self.config.get("paths", {})
        self.api_key = os.getenv("GEMINI_API_KEY")

        # 에이전트 초기화
        self.scraper = WebScraperAgent()
        self.build_parser = BuildParserSubAgent(
            api_key=self.api_key,
            model_name=gemini_cfg.get("model", "gemini-2.5-flash")
        )
        self.context_parser = ContextParserSubAgent(
            api_key=self.api_key,
            model_name=gemini_cfg.get("model", "gemini-2.5-flash")
        )
        self.validator = CrossValidatorAgent()
        self.stat_inferrer = StatInferenceAgent(
            api_key=self.api_key,
            model_name=gemini_cfg.get("model", "gemini-2.5-flash")
        )

        self.structurer = BuildStructurer(
            schema_path=paths_cfg.get("schema_path", "config/build_schema.json"),
            analysis_dir=paths_cfg.get("analysis_dir", "data/analysis"),
            knowledge_base_dir=paths_cfg.get("knowledge_base_dir", "data/knowledge_base")
        )

        self.knowledge_builder = KnowledgeBuilder(
            db_path=rag_cfg.get("db_path", "data/chromadb"),
            collection_name=rag_cfg.get("collection_name", "deepwoken_builds"),
            api_key=self.api_key,
            use_gemini_embedding=False
        )

    def _load_config(self, path: str) -> dict:
        if not YAML_AVAILABLE:
            return {}
        p = Path(path)
        if not p.exists():
            return {}
        try:
            return yaml.safe_load(p.read_text(encoding="utf-8")) or {}
        except Exception:
            return {}

    def process_url(self, url: str) -> Dict[str, Any]:
        """단일 웹 URL에 대해 서브 에이전트들을 가동하여 빌드 분석 및 RAG 적재 수행 (중복 소스 자동 캐시 로드)"""
        start_time = time.time()
        logger.info(f"=== [Web Multi-Agent Pipeline] Starting for: {url} ===")

        # Step 0: 중복 검사
        import hashlib
        potential_doc_id = "web_" + hashlib.md5(url.encode("utf-8")).hexdigest()[:12]
        cached_files = list(self.structurer.analysis_dir.rglob(f"{potential_doc_id}.json"))
        if cached_files:
            cached_json_path = cached_files[0]
            category = cached_json_path.parent.name
            cached_md_path = self.structurer.knowledge_base_dir / category / f"{potential_doc_id}.md"
            logger.info(f"⚡ [Cache Hit] Found existing web analysis for {potential_doc_id} in {category}/")
            try:
                cached_data = json.loads(cached_json_path.read_text(encoding="utf-8"))
                b_name = cached_data.get("build_summary", {}).get("build_name", "Deepwoken Guide")
                return {
                    "status": "success",
                    "cached": True,
                    "doc_id": potential_doc_id,
                    "url": url,
                    "build_name": b_name,
                    "json_path": str(cached_json_path),
                    "md_path": str(cached_md_path),
                    "elapsed_seconds": 0.05,
                    "build_data": cached_data
                }
            except Exception as e:
                logger.warning(f"Failed to read cached web JSON ({e}), re-analyzing...")

        # Step 1: 웹페이지 스크래핑
        logger.info("[SubAgent 1/5] Scraping HTML and text structure via WebScraperAgent...")
        scraped: ScrapedWebContent = self.scraper.scrape(url)

        # Step 2 & 3: 서브 에이전트 병렬 가동 (BuildParser & ContextParser)
        logger.info("[SubAgent 2 & 3] Running BuildParser and ContextParser subagents in parallel...")
        with ThreadPoolExecutor(max_workers=2) as executor:
            future_mechanics = executor.submit(self.build_parser.parse, scraped)
            future_context = executor.submit(self.context_parser.parse, scraped)

            build_mechanics = future_mechanics.result()
            context_data = future_context.result()

        # Step 4: 교차 검증 및 데이터 병합
        logger.info("[SubAgent 4/5] Merging and cross-validating via CrossValidatorAgent...")
        merged_build = self.validator.validate_and_merge(scraped, build_mechanics, context_data)
        if scraped.sub_pages:
            merged_build["explored_sub_pages"] = scraped.sub_pages

        # Step 4.5: 스탯 누락 시 자가 질의응답 및 웹 검색을 통한 자동 스탯 추론/보강
        merged_build = self.stat_inferrer.enrich_if_missing(merged_build, {"title": scraped.title})

        # Step 5: JSON 검증 & Markdown 생성 및 ChromaDB 인덱싱
        logger.info("[SubAgent 5/5] Structuring and indexing to ChromaDB knowledge base...")
        doc_id = scraped.doc_id
        saved_paths = self.structurer.process_and_save(raw_json=merged_build, video_id=doc_id)

        self.knowledge_builder.ingest_build(
            video_id=doc_id,
            json_path=saved_paths["json_path"],
            md_path=saved_paths["md_path"]
        )

        elapsed = time.time() - start_time
        build_name = merged_build.get("build_summary", {}).get("build_name", scraped.title)
        logger.info(f"=== Web Pipeline completed in {elapsed:.2f}s for '{build_name}' ===")

        return {
            "status": "success",
            "doc_id": doc_id,
            "url": url,
            "build_name": build_name,
            "json_path": str(saved_paths["json_path"]),
            "md_path": str(saved_paths["md_path"]),
            "elapsed_seconds": elapsed,
            "build_data": merged_build
        }
