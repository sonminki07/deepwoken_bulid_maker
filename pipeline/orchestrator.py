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
from agents.raw_build_model import RawBuildData, BuildDataReconciler

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

        self.reconciler = BuildDataReconciler()

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

    def _find_cached_analysis(self, url: str):
        """기존 분석 캐시 파일 및 비디오 ID 검색"""
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
                has_raw_source = "_raw_source_data" in cached_data
                traits = cached_data.get("traits", {})
                has_traits = any(v > 0 for v in traits.values() if isinstance(v, (int, float))) if traits else False
                stats = cached_data.get("stats", {})
                stat_sum = sum(v for v in stats.values() if isinstance(v, (int, float))) if stats else 0
                has_real_stats = stat_sum >= 80
                
                # 3-Tier 원시 데이터 아키텍처 및 유효 특성이 포함된 최신 캐시만 인정
                if has_raw_source and has_traits and has_real_stats:
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

        # Step 1.5: OpenCV 고해상도 UI 키프레임 추출 (2-Stage Coarse -> 0.2s Dense, Pre/Post 버킷 분리)
        if progress_callback:
            progress_callback(35, "OpenCV 1080p UI 키프레임 추출 및 Pre/Post 2단계 고밀도 스캔 중...")
        logger.info("[Step 2/5] Extracting sharp UI keyframes with Dual-Stage Smart Scanner...")
        dual_keyframes = {"pre_shrine": [], "post_shrine": []}
        dual_vision_data = None
        try:
            dual_keyframes = self.frame_extractor.extract_dual_stage_keyframes(video_path)
            total_kf = len(dual_keyframes.get("pre_shrine", [])) + len(dual_keyframes.get("post_shrine", []))
            if total_kf > 0:
                if progress_callback:
                    progress_callback(45, f"선별된 {total_kf}장 고해상도 스탯 창 픽셀 단위 정밀 판독 중...")
                logger.info(f"Analyzing {total_kf} dual-stage keyframes with Precision Vision AI...")
                dual_vision_data = self.vision_extractor.extract_dual_stage_vision(dual_keyframes)
        except Exception as kf_err:
            logger.warning(f"Dual-stage keyframe extraction or vision analysis warning: {kf_err}")

        # Step 2: Gemini 멀티모달 분석 (비디오 음성, 콤보, 보스전 공략 분석)
        logger.info(f"[Step 3/5] Analyzing video content with Gemini Multimodal ({self.analyzer.model_name})...")
        raw_analysis = self.analyzer.analyze(video_path=video_path, metadata=meta_dict, progress_callback=progress_callback)

        # Step 2.5: 설명란 deepwoken.co 빌더 링크 직접 스크래핑
        builder_url = meta_dict.get("extra", {}).get("builder_url") or self.stat_inferrer._find_builder_url(meta_dict.get("description", ""))
        builder_data = None
        if builder_url:
            logger.info(f"🌐 [Builder Grounding] Scraping builder data from: {builder_url}")
            builder_data = self.stat_inferrer._scrape_builder_url(builder_url)

        # Step 2.8: 3-Tier 아키텍처 - RawBuildData 불변 객체 생성 및 330pt 무결성 Reconciler 실행
        if progress_callback:
            progress_callback(80, "3-Tier 원시 데이터 무결성 검증 및 Pre/Post 330pt 수학적 동기화 중...")
        logger.info("⚖️ [Tier 2 Reconciliation] Reconciling RawBuildData (Vision > Builder > VLM)...")
        raw_build = RawBuildData(
            video_id=video_id,
            video_meta=meta_dict,
            pre_shrine_raw=dual_vision_data.get("pre_shrine") if dual_vision_data else None,
            post_shrine_raw=dual_vision_data.get("post_shrine") if dual_vision_data else None,
            builder_scraped=builder_data,
            vlm_narrative=raw_analysis,
            captured_keyframes=dual_keyframes.get("pre_shrine", []) + dual_keyframes.get("post_shrine", [])
        )
        normalized_build = self.reconciler.reconcile(raw_build)

        # 여전히 스탯이 부족할 경우만 최종 웹 검색 폴백
        normalized_build = self.stat_inferrer.enrich_if_missing(normalized_build, meta_dict)

        # Step 3: JSON 검증 및 Markdown 변환/저장
        if progress_callback:
            progress_callback(85, "JSON 스키마 검증 및 Markdown 지식 문서 구조화 중...")
        logger.info("[Step 3/4] Structuring data into JSON and Markdown knowledge base...")
        saved_paths = self.structurer.process_and_save(raw_json=normalized_build, video_id=video_id)

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

