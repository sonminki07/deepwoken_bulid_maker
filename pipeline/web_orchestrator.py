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
        """단일 웹 URL에 대해 웹 스크래핑을 수행하고 텍스트 원본을 마크다운으로 저장합니다."""
        start_time = time.time()
        logger.info(f"=== [Web Scraping Pipeline] Starting for: {url} ===")

        # Step 0: 중복 검사
        import hashlib
        potential_doc_id = "web_" + hashlib.md5(url.encode("utf-8")).hexdigest()[:12]
        
        target_dir = self.structurer.knowledge_base_dir / "web_docs"
        target_dir.mkdir(parents=True, exist_ok=True)
        cached_md_path = target_dir / f"{potential_doc_id}.md"
        
        if cached_md_path.exists():
            logger.info(f"⚡ [Cache Hit] Found existing scraped doc for {potential_doc_id}")
            return {
                "status": "success",
                "cached": True,
                "doc_id": potential_doc_id,
                "url": url,
                "build_name": potential_doc_id,
                "json_path": "",
                "md_path": str(cached_md_path),
                "elapsed_seconds": 0.05,
                "build_data": {}
            }

        # Step 1: 웹페이지 스크래핑
        logger.info("Scraping HTML and text structure via WebScraperAgent...")
        scraped: ScrapedWebContent = self.scraper.scrape(url)

        # Step 2: 마크다운 파일로 원문 통째로 저장
        logger.info("Saving scraped raw text to markdown...")
        doc_id = scraped.doc_id
        md_content = f"# {scraped.title}\n\n"
        md_content += f"**URL**: {scraped.url}\n\n"
        if scraped.meta_description:
            md_content += f"**Description**: {scraped.meta_description}\n\n"
        
        md_content += "---\n\n"
        md_content += scraped.cleaned_text
        
        if scraped.tables_text:
            md_content += "\n\n## Tables\n\n" + scraped.tables_text

        if scraped.sub_pages:
            md_content += "\n\n## Sub Pages Explored\n"
            for sp in scraped.sub_pages:
                md_content += f"- {sp}\n"

        md_path = target_dir / f"{doc_id}.md"
        md_path.write_text(md_content, encoding="utf-8")

        # dummy json path for compatibility with gui_app.py
        json_dir = self.structurer.analysis_dir / "web_docs"
        json_dir.mkdir(parents=True, exist_ok=True)
        json_path = json_dir / f"{doc_id}.json"
        json_path.write_text(json.dumps({"url": url, "title": scraped.title}, ensure_ascii=False, indent=2), encoding="utf-8")

        elapsed = time.time() - start_time
        logger.info(f"=== Web Scraping Pipeline completed in {elapsed:.2f}s for '{scraped.title}' ===")

        return {
            "status": "success",
            "doc_id": doc_id,
            "url": url,
            "build_name": scraped.title,
            "json_path": str(json_path),
            "md_path": str(md_path),
            "elapsed_seconds": elapsed,
            "build_data": {"title": scraped.title, "url": url}
        }
