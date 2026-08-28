import os
import time
import json
import logging
from pathlib import Path
from typing import Optional, Dict, Any, Callable, List
try:
    import yaml
    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False

from agents.collector import VideoCollector, DownloadResult
from agents.analyzer import BuildAnalyzer
from agents.stat_inferrer import StatInferenceAgent
from agents.structurer import BuildStructurer
from agents.knowledge_builder import KnowledgeBuilder
from agents.frame_extractor import FrameExtractor
from agents.vision_extractor import VisionExtractor

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

        self.frame_extractor = FrameExtractor(
            output_dir="data/keyframes"
        )

        self.vision_extractor = VisionExtractor(
            model_name="gemini-flash-latest"
        )

        self.analyzer = BuildAnalyzer(
            api_key=self.api_key,
            model_name=gemini_cfg.get("model", "gemini-3.6-flash"),
            prompt_path=paths_cfg.get("analysis_prompt_path", "prompts/analysis_prompt.txt"),
            schema_path=paths_cfg.get("schema_path", "config/build_schema.json"),
            temperature=gemini_cfg.get("temperature", 0.1)
        )

        self.stat_inferrer = StatInferenceAgent(
            api_key=self.api_key,
            model_name=gemini_cfg.get("model", "gemini-3.6-flash")
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
            logger.warning(f"Config file not found at {path}. Using default configurations.")
            return {}
        try:
            return yaml.safe_load(p.read_text(encoding="utf-8")) or {}
        except Exception:
            return {}

    def process_url(self, url: str, progress_callback = None) -> Dict[str, Any]:
        """단일 유튜브 URL 전체 분석 및 지식 베이스 인덱싱 파이프라인 실행 (중복 소스 자동 캐시 로드)"""
        start_time = time.time()
        logger.info(f"=== Starting pipeline for: {url} ===")

        # Step 0: 중복 검사 (이미 분석된 영상인지 확인하여 API 토큰 및 시간 절약)
        import re
        vid_match = re.search(r'(?:v=|\/|youtu\.be\/)([0-9A-Za-z_-]{11})', url)
        if vid_match:
            potential_vid = vid_match.group(1)
            for jf in self.structurer.analysis_dir.rglob("*.json"):
                try:
                    cached_data = json.loads(jf.read_text(encoding="utf-8"))
                    meta_url = cached_data.get("video_meta", {}).get("url", "")
                    if potential_vid in jf.stem or potential_vid in meta_url:
                        return jf, cached_data, potential_vid
                except Exception:
                    continue
        return None, None, url

    def process_url(
        self,
        url: str,
        progress_callback: Optional[Callable[[int, str], None]] = None,
        force_reanalyze: bool = False
    ) -> Dict[str, Any]:
        start_time = time.time()

        # Step 0: 기존 분석 캐시 확인 (유효한 실측 데이터가 있는 경우만 재사용)
        if not force_reanalyze:
            cached_json_path, cached_data, potential_vid = self._find_cached_analysis(url)
            if cached_json_path and cached_data:
                stats = cached_data.get("stats", {})
                stat_sum = sum(v for v in stats.values() if isinstance(v, (int, float))) if stats else 0
                has_power = cached_data.get("power") is not None
                
                if stat_sum >= 50 and has_power:
                    category = cached_json_path.parent.name
                    cached_md_path = self.structurer.knowledge_base_dir / category / f"{cached_json_path.stem}.md"
                    logger.info(f"⚡ [Cache Hit] Found valid analysis for {potential_vid} in {category}/{cached_json_path.name}")
                    if progress_callback:
                        progress_callback(95, "⚡ 이미 분석된 영상입니다. 저장된 정밀 보고서를 즉시 불러옵니다!")
                    b_name = cached_data.get("build_summary", {}).get("build_name", "Deepwoken Build")
                    return {
                        "status": "success",
                        "cached": True,
                        "video_id": potential_vid,
                        "build_name": b_name,
                        "json_path": str(cached_json_path),
                        "md_path": str(cached_md_path),
                        "elapsed_seconds": 0.05,
                        "build_data": cached_data
                    }
                else:
                    logger.info(f"⚠️ [Cache Invalid] Stale or incomplete cache for {potential_vid}, forcing fresh re-analysis...")

        # Step 1: 영상 및 메타데이터 다운로드
        if progress_callback:
            progress_callback(15, "유튜브 고화질(1080p) 영상 및 메타데이터 다운로드 중...")
        logger.info("[Step 1/5] Collecting video and metadata via yt-dlp...")
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

        # Step 1.5: OpenCV 고해상도 UI 키프레임 추출 및 전처리 (모션블러 필터링, CLAHE 대비강화)
        if progress_callback:
            progress_callback(35, "OpenCV 1080p UI 키프레임 추출 및 모션블러/대비 전처리 중...")
        logger.info("[Step 2/5] Extracting sharp UI keyframes with OpenCV...")
        keyframes = []
        vision_stats = None
        try:
            keyframes = self.frame_extractor.extract_sharp_keyframes(video_path, max_keyframes=6, sample_step_sec=1.5)
            if keyframes:
                if progress_callback:
                    progress_callback(45, "선별된 고해상도 스탯 창 픽셀 단위 정밀 판독 중...")
                logger.info(f"Analyzing {len(keyframes)} high-res keyframes with Precision Vision AI...")
                vision_stats = self.vision_extractor.extract_from_keyframes(keyframes)
        except Exception as kf_err:
            logger.warning(f"Keyframe extraction or vision analysis warning: {kf_err}")

        # Step 2: Gemini 멀티모달 분석 (비디오 음성, 콤보, 보스전 공략 분석)
        logger.info(f"[Step 3/5] Analyzing video content with Gemini Multimodal ({self.analyzer.model_name})...")
        raw_analysis = self.analyzer.analyze(video_path=video_path, metadata=meta_dict, progress_callback=progress_callback)

        # 픽셀 기반 실측 비전 스탯이 존재하면 100% 최우선 병합 (VLM 환각 원천 차단)
        if vision_stats and isinstance(vision_stats, dict):
            raw_analysis["_raw_vision_data"] = vision_stats
            
            v_stats = vision_stats.get("stats")
            if v_stats and isinstance(v_stats, dict) and sum([v for v in v_stats.values() if isinstance(v, (int, float))]) > 0:
                logger.info("🎯 [Vision Grounding] Overriding stats with 100% pixel-exact vision extracted numbers!")
                raw_analysis["stats"] = v_stats
            
            v_att = vision_stats.get("attunements")
            if v_att and isinstance(v_att, dict):
                raw_analysis["attunements"] = v_att

            if vision_stats.get("power"):
                raw_analysis["power"] = vision_stats["power"]
            if vision_stats.get("origin"):
                raw_analysis["origin"] = vision_stats["origin"]
            if vision_stats.get("race"):
                raw_analysis["race"] = vision_stats["race"]
            if vision_stats.get("oath") and vision_stats["oath"] != "None":
                raw_analysis["oath"] = vision_stats["oath"]
            if vision_stats.get("traits"):
                raw_analysis["traits"] = vision_stats["traits"]
            if vision_stats.get("combat_stats"):
                raw_analysis["combat_stats"] = vision_stats["combat_stats"]
            if vision_stats.get("resistances"):
                raw_analysis["resistances"] = vision_stats["resistances"]

        # Step 2.5: 스탯 누락 시 자가 질의응답 및 웹 검색을 통한 자동 스탯 추론/보강
        if progress_callback:
            progress_callback(80, "스탯 유효성 검증 및 빌드 스키마 무결성 확인 중...")
        raw_analysis = self.stat_inferrer.enrich_if_missing(raw_analysis, meta_dict)

        # Step 3: JSON 검증 및 Markdown 변환/저장
        if progress_callback:
            progress_callback(85, "JSON 스키마 검증 및 Markdown 지식 문서 구조화 중...")
        logger.info("[Step 3/4] Structuring data into JSON and Markdown knowledge base...")
        saved_paths = self.structurer.process_and_save(raw_json=raw_analysis, video_id=video_id)

        # Step 4: ChromaDB RAG 인덱싱
        if progress_callback:
            progress_callback(90, "ChromaDB 벡터 데이터베이스 인덱싱 중...")
        logger.info("[Step 4/4] Ingesting build into ChromaDB vector index...")
        self.knowledge_builder.ingest_build(
            video_id=video_id,
            json_path=saved_paths["json_path"],
            md_path=saved_paths["md_path"]
        )

        # Step 5: 마스터 소스 재컴파일 및 구글 드라이브 실시간 자동 동기화
        if progress_callback:
            progress_callback(95, "NotebookLM 마스터 소스 컴파일 및 구글 드라이브 자동 동기화 중...")
        try:
            from agents.gdrive_sync import sync_to_google_drive
            sync_ok, sync_msg, _ = sync_to_google_drive()
            if sync_ok:
                logger.info(f"Auto-synced to Google Drive: {sync_msg}")
        except Exception as sync_err:
            logger.warning(f"Auto GDrive sync warning: {sync_err}")

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

