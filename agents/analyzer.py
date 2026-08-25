import os
import json
import time
import logging
import warnings
from pathlib import Path
from typing import Dict, Any, Optional

with warnings.catch_warnings():
    warnings.simplefilter("ignore", category=FutureWarning)
    import google.generativeai as genai
    from google.generativeai.types import File

logger = logging.getLogger(__name__)

class BuildAnalyzer:
    """2단계: Gemini Files API 기반 멀티모달(영상+음성) 빌드 분석기"""

    def __init__(
        self,
        api_key: Optional[str] = None,
        model_name: str = "gemini-3.7-flash",
        prompt_path: str = "prompts/analysis_prompt.txt",
        schema_path: str = "config/build_schema.json",
        temperature: float = 0.1,
        cleanup_remote_file: bool = True
    ):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY is not set. Please set the environment variable or pass api_key.")
        
        genai.configure(api_key=self.api_key)
        self.model_name = model_name
        self.temperature = temperature
        self.cleanup_remote_file = cleanup_remote_file

        # 시스템 프롬프트 로드
        self.system_prompt = self._load_text(prompt_path)
        # 빌드 JSON 스키마 로드
        self.schema = self._load_json(schema_path)

    def _load_text(self, path: str) -> str:
        p = Path(path)
        if not p.exists():
            raise FileNotFoundError(f"Prompt file not found at: {path}")
        return p.read_text(encoding="utf-8")

    def _load_json(self, path: str) -> dict:
        p = Path(path)
        if not p.exists():
            raise FileNotFoundError(f"Schema file not found at: {path}")
        return json.loads(p.read_text(encoding="utf-8"))

    def _wait_for_file_active(self, remote_file: File, timeout_seconds: int = 600, poll_interval: int = 5) -> File:
        """Gemini Files API에 업로드된 비디오 파일의 프로세싱이 ACTIVE 상태가 될 때까지 대기"""
        logger.info(f"Waiting for video processing on Gemini Cloud: {remote_file.name}...")
        start_time = time.time()
        
        while time.time() - start_time < timeout_seconds:
            f = genai.get_file(remote_file.name)
            state = f.state.name
            logger.debug(f"File state: {state}")
            
            if state == "ACTIVE":
                logger.info(f"Video file is ready for analysis: {f.name}")
                return f
            elif state == "FAILED":
                raise RuntimeError(f"Gemini video processing failed: {f.error.message if hasattr(f, 'error') else 'Unknown error'}")
            
            time.sleep(poll_interval)
            
        raise TimeoutError(f"Video processing timed out after {timeout_seconds} seconds")

    def analyze(self, video_path: Path, metadata: Optional[Dict[str, Any]] = None, max_retries: int = 3) -> Dict[str, Any]:
        """영상 파일을 Gemini에 업로드하고 멀티모달 분석을 실행하여 JSON을 반환"""
        if not video_path.exists():
            raise FileNotFoundError(f"Video file does not exist: {video_path}")

        logger.info(f"Uploading {video_path.name} to Gemini Files API...")
        remote_file = genai.upload_file(path=str(video_path))
        
        try:
            active_file = self._wait_for_file_active(remote_file)
            
            # 메타데이터 컨텍스트 구성
            context_prompt = self.system_prompt
            if metadata:
                meta_str = (
                    f"\n[영상 메타데이터]\n"
                    f"- 제목: {metadata.get('title', 'N/A')}\n"
                    f"- 채널: {metadata.get('channel', 'N/A')}\n"
                    f"- URL: {metadata.get('url', 'N/A')}\n"
                    f"- 업로드 날짜: {metadata.get('upload_date', 'N/A')}\n"
                    f"- 설명: {metadata.get('description', '')[:500]}...\n"
                )
                context_prompt = context_prompt + "\n" + meta_str

            logger.info(f"Invoking Gemini models for build extraction...")
            from agents.key_manager import global_key_manager

            models_to_try = [self.model_name, "gemini-2.5-flash-lite", "gemini-flash-latest", "gemini-2.5-pro"]
            last_error = None

            for m_name in dict.fromkeys(models_to_try):
                for attempt in range(1, max_retries + 1):
                    try:
                        model = genai.GenerativeModel(
                            model_name=m_name,
                            generation_config={
                                "temperature": self.temperature,
                                "response_mime_type": "application/json",
                            }
                        )
                        response = model.generate_content([active_file, context_prompt])
                        response_text = response.text.strip()
                        
                        # 마크다운 백틱 제거 (```json ... ``` 처리)
                        if response_text.startswith("```json"):
                            response_text = response_text[7:]
                        if response_text.startswith("```"):
                            response_text = response_text[3:]
                        if response_text.endswith("```"):
                            response_text = response_text[:-3]
                        response_text = response_text.strip()

                        parsed_json = json.loads(response_text)
                        
                        # 메타데이터 기본값 보강
                        if metadata:
                            video_meta = parsed_json.setdefault("video_meta", {})
                            video_meta.setdefault("title", metadata.get("title"))
                            video_meta.setdefault("channel", metadata.get("channel"))
                            video_meta.setdefault("url", metadata.get("url"))
                            video_meta.setdefault("upload_date", metadata.get("upload_date"))
                            
                        return parsed_json
                    except Exception as e:
                        err_str = str(e).lower()
                        last_error = e
                        logger.warning(f"Analysis with {m_name} attempt {attempt}/{max_retries} failed: {e}")
                        if "429" in err_str or "quota" in err_str or "resourceexhausted" in err_str:
                            global_key_manager.rotate_key(reason="Video Analysis 429")
                        time.sleep(3 * attempt)

            raise RuntimeError(f"Build analysis failed after multiple model attempts: {last_error}")

        finally:
            if self.cleanup_remote_file and remote_file:
                try:
                    logger.info(f"Cleaning up remote file: {remote_file.name}")
                    genai.delete_file(remote_file.name)
                except Exception as cleanup_err:
                    logger.warning(f"Failed to delete remote file {remote_file.name}: {cleanup_err}")
