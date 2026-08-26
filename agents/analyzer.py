import os
import time
import json
import logging
from pathlib import Path
from typing import Optional, Dict, Any

from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

class BuildAnalyzer:
    """Agent 2: Gemini 3.6 Flash 멀티모달 비디오 분석 및 빌드 추출 에이전트"""

    def __init__(
        self,
        api_key: Optional[str] = None,
        model_name: str = "gemini-3.6-flash",
        prompt_path: str = "prompts/analysis_prompt.txt",
        schema_path: str = "config/build_schema.json",
        temperature: float = 0.1,
        cleanup_remote_file: bool = True
    ):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY is not set.")
        
        self.client = genai.Client(api_key=self.api_key)
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

    def _wait_for_file_active(self, client: genai.Client, file_name: str, timeout_seconds: int = 3600, poll_interval: int = 5):
        """비디오 파일 프로세싱 완료 대기"""
        logger.info(f"Waiting for video processing on Gemini Cloud: {file_name}...")
        start_time = time.time()
        
        while time.time() - start_time < timeout_seconds:
            f = client.files.get(name=file_name)
            state = f.state.name if hasattr(f.state, 'name') else str(f.state)
            logger.debug(f"File state: {state}")
            
            if "ACTIVE" in state.upper():
                logger.info(f"Video file is ready for analysis: {f.name}")
                return f
            elif "FAILED" in state.upper():
                raise RuntimeError(f"Gemini video processing failed for {file_name}")
            
            time.sleep(poll_interval)
            
        raise TimeoutError(f"Video processing timed out after {timeout_seconds} seconds")

    def analyze(self, video_path: Path, metadata: Optional[Dict[str, Any]] = None, max_retries: int = 3, progress_callback = None) -> Dict[str, Any]:
        """영상 파일을 Gemini에 업로드하고 멀티모달 분석을 실행하여 JSON을 반환"""
        if not video_path.exists():
            raise FileNotFoundError(f"Video file does not exist: {video_path}")

        from agents.key_manager import global_key_manager

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

        last_error = None
        for attempt in range(1, 6):
            client = global_key_manager.get_client()
            remote_file = None
            try:
                if progress_callback:
                    progress_callback(35, f"Gemini 클라우드로 영상 업로드 중... (시도 {attempt})")
                logger.info(f"Uploading {video_path.name} to Gemini Files API with active client key (Attempt {attempt})...")
                remote_file = client.files.upload(file=str(video_path))
                
                if progress_callback:
                    progress_callback(55, "Gemini 클라우드 비디오 프레임 변환 및 인코딩 중...")
                active_file = self._wait_for_file_active(client=client, file_name=remote_file.name)
                
                if progress_callback:
                    progress_callback(75, "Gemini 2.5 Flash 멀티모달 AI 빌드 추출 중...")
                
                for m_name in ["gemini-2.5-flash", "gemini-3.5-flash", "gemini-flash-latest"]:
                    try:
                        logger.info(f"Sending video to model {m_name} with matching client key (Attempt {attempt})...")
                        response = client.models.generate_content(
                            model=m_name,
                            contents=[active_file, context_prompt],
                            config=types.GenerateContentConfig(
                                temperature=self.temperature,
                                response_mime_type="application/json"
                            )
                        )
                        response_text = response.text.strip()
                        
                        # 마크다운 백틱 제거
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
                        logger.warning(f"Model {m_name} failed on attempt {attempt}: {e}")
                        last_error = e
                        if "429" in err_str or "quota" in err_str or "exhausted" in err_str:
                            break  # Try next key attempt
            except Exception as e:
                err_str = str(e).lower()
                logger.warning(f"Key attempt {attempt} failed during upload/analysis: {e}")
                last_error = e
            finally:
                if self.cleanup_remote_file and remote_file:
                    try:
                        logger.info(f"Cleaning up remote file from Gemini Cloud: {remote_file.name}")
                        client.files.delete(name=remote_file.name)
                    except Exception as ex:
                        logger.warning(f"Failed to delete remote file: {ex}")

            # 429 또는 에러 시 다음 키로 로테이션
            global_key_manager.rotate_key(reason=f"Gemini API Error on attempt {attempt}: {last_error}")

        raise RuntimeError(f"All Gemini models and API keys failed for video analysis: {last_error}")
