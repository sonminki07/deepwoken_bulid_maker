import os
import time
import logging
from pathlib import Path
from typing import Optional, Dict, Any
import yaml

from agents.collector import VideoCollector, DownloadResult
from agents.analyzer import BuildAnalyzer
from agents.structurer import BuildStructurer
from agents.knowledge_builder import KnowledgeBuilder

logger = logging.getLogger(__name__)

class PipelineOrchestrator:
    """전체 멀티 에이전트 파이프라인 총괄 오케스트레이터"""

    def __init__(self, config_path: str = "config/settings.yaml"):
        self.config = self._load_config(config_path)
        
        # 설정 파싱
        gemini_cfg = self.config.get("gemini", {})
        download_cfg = self.config.get("download", {})
        rag_cfg = self.config.get("rag", {})
        paths_cfg = self.config.get("paths", {})

        self.api_key = os.getenv("GEMINI_API_KEY")
        self.cleanup_local_video = download_cfg.get("cleanup_after_analysis", True)

        # 에이전트 초기화
        self.collector = VideoCollector(
            output_dir=download_cfg.get("output_dir", "data/videos"),
            max_filesize_bytes=download_cfg.get("max_filesize_bytes", 2 * 1024 * 1024 * 1024)
        )

        self.analyzer = BuildAnalyzer(
            api_key=self.api_key,
            model_name=gemini_cfg.get("model", "gemini-2.5-pro"),
            prompt_path=paths_cfg.get("analysis_prompt_path", "prompts/analysis_prompt.txt"),
            schema_path=paths_cfg.get("schema_path", "config/build_schema.json"),
            temperature=gemini_cfg.get("temperature", 0.1)
        )

        self.structurer = BuildStructurer(
            schema_path=paths_cfg.get("schema_path", "config/build_schema.json"),
            analysis_dir=paths_cfg.get("analysis_dir", "data/analysis"),
            knowledge_base_dir=paths_cfg.get("knowledge_base_dir", "data/knowledge_base")
        )

        self.knowledge_builder = KnowledgeBuilder(
            db_path=rag_cfg.get("db_path", "data/chromadb"),
            collection_name=rag_cfg.get("collection_name", "deepwoken_builds"),
            api_key=self.api_key
        )

    def _load_config(self, path: str) -> dict:
        p = Path(path)
        if not p.exists():
            logger.warning(f"Config file not found at {path}. Using default configurations.")
            return {}
        return yaml.safe_load(p.read_text(encoding="utf-8")) or {}

    def process_url(self, url: str) -> Dict[str, Any]:
        """단일 유튜브 URL 전체 분석 및 지식 베이스 인덱싱 파이프라인 실행"""
        start_time = time.time()
        logger.info(f"=== Starting pipeline for: {url} ===")

        # Step 1: 영상 및 메타데이터 다운로드
        logger.info("[Step 1/4] Collecting video and metadata via yt-dlp...")
        download_result: DownloadResult = self.collector.download(url)
        video_id = download_result.video_id
        video_path = download_result.video_path
        meta_dict = {
            "title": download_result.metadata.title,
            "channel": download_result.metadata.channel,
            "url": download_result.metadata.url,
            "upload_date": download_result.metadata.upload_date,
            "description": download_result.metadata.description,
        }

        # Step 2: Gemini 멀티모달 분석
        logger.info(f"[Step 2/4] Analyzing video content with Gemini Multimodal ({self.analyzer.model_name})...")
        raw_analysis = self.analyzer.analyze(video_path=video_path, metadata=meta_dict)

        # Step 3: JSON 검증 및 Markdown 변환/저장
        logger.info("[Step 3/4] Structuring data into JSON and Markdown knowledge base...")
        saved_paths = self.structurer.process_and_save(raw_json=raw_analysis, video_id=video_id)

        # Step 4: ChromaDB RAG 인덱싱
        logger.info("[Step 4/4] Ingesting build into ChromaDB vector index...")
        self.knowledge_builder.ingest_build(
            video_id=video_id,
            json_path=saved_paths["json_path"],
            md_path=saved_paths["md_path"]
        )

        # 로컬 영상 파일 정리 (설정 시)
        if self.cleanup_local_video and video_path.exists() and not download_result.from_cache:
            try:
                logger.info(f"Cleaning up local video file: {video_path.name}")
                video_path.unlink()
            except Exception as e:
                logger.warning(f"Failed to delete local video: {e}")

        elapsed = time.time() - start_time
        summary_name = raw_analysis.get("build_summary", {}).get("build_name", "Deepwoken Build")
        logger.info(f"=== Pipeline completed successfully in {elapsed:.2f}s for '{summary_name}' ===")

        return {
            "status": "success",
            "video_id": video_id,
            "build_name": summary_name,
            "json_path": str(saved_paths["json_path"]),
            "md_path": str(saved_paths["md_path"]),
            "elapsed_seconds": elapsed,
            "build_data": raw_analysis
        }

BuildPipelineOrchestrator = PipelineOrchestrator

