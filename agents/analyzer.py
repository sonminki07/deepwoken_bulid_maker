import os
import time
import json
import logging
from pathlib import Path
from typing import Optional, Dict, Any, List

from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

PROJECT_DIR = Path(__file__).resolve().parent.parent

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
                    progress_callback(75, "Gemini 3.6 Flash 멀티모달 AI 빌드 추출 중...")
                
                for m_name in [
                    "gemini-2.5-flash",
                    "gemini-2.0-flash",
                    "gemini-1.5-flash",
                    "gemini-flash-latest",
                    "gemini-3.6-flash"
                ]:
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
                        if isinstance(parsed_json, list) and len(parsed_json) > 0:
                            parsed_json = parsed_json[0]
                        if not isinstance(parsed_json, dict):
                            parsed_json = {}
                        
                        # 메타데이터 기본값 보강
                        if metadata:
                            video_meta = parsed_json.setdefault("video_meta", {})
                            video_meta.setdefault("title", metadata.get("title"))
                            video_meta.setdefault("channel", metadata.get("channel"))
                            video_meta.setdefault("url", metadata.get("url"))
                            video_meta.setdefault("upload_date", metadata.get("upload_date"))

                        # 정밀 3-Region Vision OCR 교차 보정 (Traits, Stats, Combat Stats, Resistances 1:1 팩트 동기화)
                        vid_id = metadata.get("id") if metadata else video_path.stem
                        try:
                            logger.info("🎯 Running 3-Region High-Res Keyframe Vision OCR calibration...")
                            vision_data = self.analyze_keyframes_vision(video_path, client, video_id=vid_id)
                            if vision_data:
                                if vision_data.get("traits"):
                                    parsed_json["traits"] = vision_data["traits"]
                                if vision_data.get("combat_stats"):
                                    parsed_json["combat_stats"] = vision_data["combat_stats"]
                                if vision_data.get("resistances"):
                                    parsed_json["resistances"] = vision_data["resistances"]
                                if vision_data.get("stats") and sum(v for v in vision_data["stats"].values() if isinstance(v, (int, float))) > 50:
                                    parsed_json["stats"] = vision_data["stats"]
                                if vision_data.get("attunements") and any(v > 0 for v in vision_data["attunements"].values() if isinstance(v, (int, float))):
                                    parsed_json["attunements"] = vision_data["attunements"]
                                if vision_data.get("character_setup"):
                                    cs = vision_data["character_setup"]
                                    if cs.get("oath"): parsed_json["oath"] = cs["oath"]
                                    if cs.get("origin"): parsed_json["origin"] = cs["origin"]
                                    if cs.get("race") or cs.get("aspect"): parsed_json["race"] = cs.get("race") or cs.get("aspect")
                        except Exception as v_err:
                            logger.warning(f"3-Region keyframe vision calibration warning: {v_err}")
                            
                        return parsed_json
                    except Exception as e:
                        err_str = str(e).lower()
                        logger.warning(f"Model {m_name} failed on attempt {attempt}: {e}")
                        last_error = e
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

    def _get_video_duration(self, video_path: Path, ffmpeg_exe: str) -> float:
        """비디오의 총 길이(초)를 ffprobe/ffmpeg로 측정"""
        try:
            import subprocess, json
            probe_cmd = [
                ffmpeg_exe.replace("ffmpeg.exe", "ffprobe.exe").replace("ffmpeg", "ffprobe"),
                "-v", "error", "-show_entries", "format=duration", "-of", "json", str(video_path)
            ]
            res = subprocess.run(probe_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if res.returncode == 0:
                data = json.loads(res.stdout)
                return float(data.get("format", {}).get("duration", 0.0))
        except Exception:
            pass
        return 300.0  # 기본값 5분

    def _save_trace_log(self, video_id: str, best_full_img: Path, crop_files: List[Path], raw_vision_text: str, parsed_data: Dict[str, Any]):
        """분석 당시의 크롭 이미지, AI 응답, 추출 결과를 로컬 logs/analysis_traces/ 폴더에 영구 보존"""
        try:
            import datetime, shutil
            trace_dir = PROJECT_DIR / "logs" / "analysis_traces" / f"{video_id}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
            frames_dir = trace_dir / "frames"
            frames_dir.mkdir(parents=True, exist_ok=True)

            if best_full_img and best_full_img.exists():
                shutil.copy2(best_full_img, frames_dir / "best_showcase_full.jpg")
            
            for cp in crop_files:
                if cp and cp.exists():
                    shutil.copy2(cp, frames_dir / cp.name)

            (trace_dir / "raw_vision_response.json").write_text(raw_vision_text, encoding="utf-8")
            (trace_dir / "extracted_build.json").write_text(json.dumps(parsed_data, indent=2, ensure_ascii=False), encoding="utf-8")
            logger.info(f"📁 [Trace Log Saved] Analysis artifacts permanently stored at: {trace_dir}")
        except Exception as te:
            logger.debug(f"Failed to save trace log: {te}")

    def analyze_keyframes_vision(self, video_path: Path, client: genai.Client, video_id: str = "unknown") -> Optional[Dict[str, Any]]:
        """영상 전 구간을 훑어 100% 스탯창 노출 프레임을 포착하고, 전체 프레임 1장을 강력한 Vision Pro 모델로 직독직해"""
        try:
            import shutil, tempfile
            from PIL import Image
            from agents.frame_extractor import FrameExtractor

            fe = FrameExtractor()
            hud_keyframes = fe.extract_sharp_keyframes(video_path, max_keyframes=4, fps_step=1.0)
            
            if not hud_keyframes:
                logger.warning("No Stat-HUD keyframes detected.")
                return None

            temp_dir = Path(tempfile.mkdtemp(prefix="deepwoken_fullframe_"))
            try:
                all_crop_files = [] # 기존 로그 시스템 호환을 위해 빈 배열 유지
                contents = []

                # 가장 점수가 높은 1등 프레임 1장만 사용
                best_kf = hud_keyframes[0]
                full_img_p = Path(best_kf["path"])
                
                # 원본 이미지 1장만 추가
                contents.append(types.Part.from_bytes(data=full_img_p.read_bytes(), mime_type="image/jpeg"))

                # 통이미지용 정밀 프롬프트
                prompt = """
🚨 [CRITICAL: FULL-FRAME VISION OCR INSTRUCTION]
제공된 이미지는 Deepwoken 게임의 스크린샷 1장입니다. 화면 우측에 있는 전체 스탯창(Stat Sheet) 패널을 찾아 다음 수치들을 절대 지어내지 말고 1:1로 있는 그대로 전사하세요.

1. traits (우측 상단 4대 특성 원형 아이콘 안의 숫자 0~6):
   - vitality (생명력), erudition (학식), proficiency (숙련), songchant (영창)
2. stats (BODY & MIND & WEAPONS 영역):
   - strength, fortitude, agility, intelligence, willpower, charisma, heavy_wep, medium_wep, light_wep
3. attunements (ELEMENTS 영역):
   - flamecharm, frostdraw, thundercall, galebreathe, shadowcast, ironsing, bloodrend
4. combat_stats (하단 실전 전투 수치):
   - hp (❤️ 아이콘 옆 Max Health)
   - posture (🛡️ 아이콘 옆 자세)
   - ether (💧 아이콘 옆 에테르)
   - tempo (⚡ 템포)
   - sanity (🧠 정신력)
   - move_speed_pct (👟 이동속도 백분율)
   - pve_dmg_pct (💀 몬스터 대상 피해 백분율)
   - physical_armor_pct (방어 백분율)
5. resistances (하단 10종 저항력 아이콘 백분율):
   - physical_blunt (🔨 타격), physical_slash (🗡️ 베기), physical_pierce (🩸/관통)
   - fire (🔥 화염), ice (❄️ 빙결), lightning (⚡ 번개), wind (💨 바람), shadow (🌌 암흑), iron (⚙️ 금속), acid (🩸/🧪 혈액/산성)
6. character_setup:
   - origin, oath, race / aspect, age

반드시 순수 JSON만 반환하세요. 마크다운 백틱 없이 유효한 JSON 형식으로 출력하세요.
"""
                contents.append(prompt)
                
                raw_response_text = ""
                extracted_data = None

                # Pro 모델을 최우선으로 배치하여 고해상도 전체 텍스트 판독력 극대화
                for v_model in ["gemini-1.5-pro", "gemini-2.0-pro", "gemini-1.5-flash", "gemini-flash-latest"]:
                    try:
                        resp = client.models.generate_content(
                            model=v_model,
                            contents=contents,
                            config=types.GenerateContentConfig(temperature=0.0, response_mime_type="application/json")
                        )
                        raw_response_text = resp.text.strip()
                        text = raw_response_text
                        if text.startswith("```json"): text = text[7:]
                        if text.startswith("```"): text = text[3:]
                        if text.endswith("```"): text = text[:-3]
                        extracted_data = json.loads(text.strip())
                        logger.info(f"🎯 Full-Frame Vision OCR extracted exact stats using {v_model}")
                        break
                    except Exception as ve:
                        logger.debug(f"Vision model {v_model} failed: {ve}")

                if extracted_data:
                    best_full_p = full_img_p
                    self._save_trace_log(video_id, best_full_p, all_crop_files, raw_response_text, extracted_data)
                    return extracted_data
            finally:
                shutil.rmtree(temp_dir, ignore_errors=True)
        except Exception as e:
            logger.warning(f"3-Region Keyframe vision analysis error: {e}")
        return None
