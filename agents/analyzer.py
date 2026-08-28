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
                    progress_callback(75, "Gemini 3.6 Flash 멀티모달 AI 빌드 추출 중...")
                
                for m_name in [
                    "gemini-flash-latest",
                    "gemini-3.7-flash",
                    "gemini-3.6-flash",
                    "gemini-flash-lite-latest",
                    "gemini-3.1-flash-lite",
                    "gemini-3.5-flash-lite",
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

                        # 스탯 검증 및 정밀 비전(VisionExtractor) 교차 보정
                        stats = parsed_json.get("stats", {}) or parsed_json.get("stats_and_attunements", {}).get("stats", {})
                        stat_sum = sum(v for v in stats.values() if isinstance(v, (int, float))) if stats else 0
                        
                        if stat_sum == 0 or stat_sum < 100:
                            logger.info(f"Stats sum is low ({stat_sum}), running Precision Keyframe Vision AI...")
                            try:
                                from agents.frame_extractor import FrameExtractor
                                from agents.vision_extractor import VisionExtractor
                                fe = FrameExtractor()
                                ve = VisionExtractor()
                                kfs = fe.extract_sharp_keyframes(video_path, max_keyframes=5)
                                vision_data = ve.extract_from_keyframes(kfs)
                                if vision_data:
                                    if "stats" in vision_data and vision_data["stats"]:
                                        parsed_json["stats"] = vision_data["stats"]
                                    if "attunements" in vision_data and vision_data["attunements"]:
                                        parsed_json["attunements"] = vision_data["attunements"]
                                    if vision_data.get("race"):
                                        parsed_json["race"] = vision_data["race"]
                                    if vision_data.get("oath") and vision_data["oath"] != "None":
                                        parsed_json["oath"] = vision_data["oath"]
                                    if vision_data.get("traits"):
                                        parsed_json["traits"] = vision_data["traits"]
                                    if vision_data.get("combat_stats"):
                                        parsed_json["combat_stats"] = vision_data["combat_stats"]
                                    if vision_data.get("resistances"):
                                        parsed_json["resistances"] = vision_data["resistances"]
                            except Exception as v_err:
                                logger.warning(f"Precision keyframe vision fallback warning: {v_err}")
                            
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

    def analyze_keyframes_vision(self, video_path: Path, client: genai.Client) -> Optional[Dict[str, Any]]:
        """FFmpeg로 영상 전 구간(초반, 중반, 종반 쇼케이스)을 동적 샘플링하여 스탯창/빌더 화면을 100% 탐지하고 Vision OCR 정밀 판독"""
        try:
            import subprocess, shutil, tempfile
            from PIL import Image, ImageEnhance
            import imageio_ffmpeg
            ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
            
            total_duration = self._get_video_duration(video_path, ffmpeg_exe)
            logger.info(f"Video total duration: {total_duration:.1f}s ({total_duration/60:.1f} minutes)")
            
            temp_dir = Path(tempfile.mkdtemp(prefix="deepwoken_frames_"))
            try:
                # 동적 타임스탬프 생성:
                # 1) 초반부 (0s ~ min(240s, duration)): 6초 간격
                ts_early = list(range(10, min(240, int(total_duration)), 6))
                
                # 2) 종반부 쇼케이스 (duration - 360s ~ duration): 5초 간격
                ts_late = []
                if total_duration > 240:
                    start_late = max(240, int(total_duration - 360))
                    ts_late = list(range(start_late, int(total_duration) - 5, 5))
                
                # 3) 전체 구간 10등분 분할점
                ts_mid = [int(total_duration * (i / 15.0)) for i in range(1, 15)]
                
                all_ts = sorted(list(set(ts_early + ts_late + ts_mid)))
                logger.info(f"Generated {len(all_ts)} candidate frame timestamps spanning 0s to {int(total_duration)}s")
                
                candidate_images = []
                
                for ts in all_ts:
                    out_img = temp_dir / f"frame_{ts}s.jpg"
                    cmd = [ffmpeg_exe, "-y", "-ss", str(ts), "-i", str(video_path), "-vframes", "1", "-q:v", "1", str(out_img)]
                    subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    
                    if out_img.exists() and out_img.stat().st_size > 5000:
                        try:
                            pil_img = Image.open(out_img)
                            w, h = pil_img.size
                            
                            # 우측 Stat Sheet 영역 크롭 및 확대 (x: 70%~100%, y: 2%~95%로 하단 STATS/RESISTANCES까지 완전 포함)
                            stat_crop = pil_img.crop((int(0.68 * w), int(0.02 * h), int(0.995 * w), int(0.95 * h)))
                            stat_crop = stat_crop.resize((stat_crop.width * 2, stat_crop.height * 2), Image.LANCZOS)
                            enhancer = ImageEnhance.Contrast(stat_crop)
                            stat_crop = enhancer.enhance(1.4)
                            crop_path = temp_dir / f"crop_stat_{ts}s.png"
                            stat_crop.save(crop_path)
                            
                            candidate_images.append((out_img, crop_path, ts))
                        except Exception as crop_err:
                            logger.debug(f"Crop failed on frame {ts}s: {crop_err}")
                
                if not candidate_images:
                    return None
                
                # 프롬프트: 인게임 UI, deepwoken.co 빌더 화면, 텍스트 카드 슬라이드 편집 등 모든 형태 1:1 직독직해
                prompt = """
🚨 [CRITICAL: STRICT 1:1 PIXEL-LEVEL MULTI-UI OCR INSTRUCTION]
제공된 이미지들 중 Deepwoken 게임의 스탯창(Stat Sheet) 또는 deepwoken.co 빌더 웹 화면이 있습니다.
절대로 임의로 추론하거나 지어내지 말고, 화면에 적힌 실제 텍스트와 숫자를 1:1로 있는 그대로 전사하여 JSON으로 추출하세요:

1. traits (우측 상단 4대 특성):
   - vitality, erudition, proficiency, songchant (숫자 0~6)
2. stats (BODY & WEAPONS 수치):
   - strength, fortitude, agility, intelligence, willpower, charisma, heavy_wep, medium_wep, light_wep
3. attunements (속성 수치):
   - shadowcast, flamecharm, frostdraw, thundercall, galebreathe, ironsing, bloodrend
4. combat_stats (스탯창 하단 STATS 수치):
   - hp (Max Health 수치), posture, ether, tempo, sanity, move_speed_pct, pve_dmg_pct
5. resistances (스탯창 하단 RESISTANCES 수치):
   - physical_slash, physical_blunt, physical_pierce, fire, ice, wind, shadow, lightning, iron, acid (예: "43.0%")
6. character_setup:
   - origin (Deepbound, Lone Warrior, Castaway 등)
   - oath (Dawnwalker, Bladeharper, Starkindred 등)
   - race / aspect (Canor, Khan, Vesperian 등)
7. weapons_and_equipment:
   - weapon (Fist, Legion Cestus, Evanspear Handaxe 등)
   - outfit (Black Diver, Prophet's Cloak 등)
   - accessories [장비/반지 목록]
8. mantras: [스킬바에 보이는 만트라 영문명 목록]

반드시 화면에 노출된 정확한 실제 수치만 JSON으로 반환하세요. 마크다운 백틱 없이 순수 JSON만 반환하세요.
"""
                # 균등하게 분배하여 최대 12장 선택
                step = max(1, len(candidate_images) // 6)
                selected_samples = candidate_images[::step][:6]
                
                contents = []
                for full_p, crop_p, _ in selected_samples:
                    contents.append(types.Part.from_bytes(data=full_p.read_bytes(), mime_type="image/jpeg"))
                    contents.append(types.Part.from_bytes(data=crop_p.read_bytes(), mime_type="image/png"))
                contents.append(prompt)
                
                for v_model in ["gemini-3.6-flash", "gemini-3.7-flash"]:
                    try:
                        resp = client.models.generate_content(
                            model=v_model,
                            contents=contents,
                            config=types.GenerateContentConfig(temperature=0.0, response_mime_type="application/json")
                        )
                        text = resp.text.strip()
                        if text.startswith("```json"): text = text[7:]
                        if text.startswith("```"): text = text[3:]
                        if text.endswith("```"): text = text[:-3]
                        data = json.loads(text.strip())
                        logger.info(f"Dense Vision OCR extracted exact stats using {v_model}")
                        return data
                    except Exception as ve:
                        logger.debug(f"Vision model {v_model} failed: {ve}")
            finally:
                shutil.rmtree(temp_dir, ignore_errors=True)
        except Exception as e:
            logger.warning(f"Keyframe vision analysis error: {e}")
        return None
