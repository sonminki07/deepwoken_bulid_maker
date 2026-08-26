import os
import time
import logging
from typing import List, Optional
from google import genai
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

class KeyManager:
    """Gemini API 키 순환 및 지능형 템포 조절(Pacing Rate-Limiter) 매니저 (google-genai)"""

    def __init__(self, keys_str: Optional[str] = None):
        self.keys: List[str] = []
        raw_keys = keys_str or os.getenv("GEMINI_API_KEYS") or os.getenv("GEMINI_API_KEY", "")
        
        for k in raw_keys.replace(";", ",").replace("\n", ",").split(","):
            cleaned = k.strip()
            if cleaned and cleaned not in self.keys:
                self.keys.append(cleaned)

        self.current_idx = 0
        self.last_request_time = 0.0
        self.min_request_interval = 2.0  # 15 RPM 한도 방지를 위해 요청 간 2초의 안전 템포 유지

        if not self.keys:
            logger.warning("No API keys configured in KeyManager.")

    def _pace_request(self):
        """15 RPM(분당 15회) 한도를 넘지 않도록 간당간당하게 안전 템포 유지"""
        now = time.time()
        elapsed = now - self.last_request_time
        if elapsed < self.min_request_interval:
            time.sleep(self.min_request_interval - elapsed)
        self.last_request_time = time.time()

    def get_current_key(self) -> str:
        if not self.keys:
            return os.getenv("GEMINI_API_KEY", "")
        return self.keys[self.current_idx]

    def get_client(self) -> genai.Client:
        self._pace_request()
        return genai.Client(api_key=self.get_current_key())

    def rotate_key(self, reason: str = "Quota Exceeded") -> str:
        """다음 사용 가능한 키로 순환"""
        if len(self.keys) <= 1:
            logger.warning(f"Key rotation triggered ({reason}), but only 1 key is available. Waiting 5s...")
            time.sleep(5)
            return self.get_current_key()

        prev_idx = self.current_idx
        self.current_idx = (self.current_idx + 1) % len(self.keys)
        new_key = self.keys[self.current_idx]
        masked_new = f"{new_key[:6]}...{new_key[-4:]}"
        masked_old = f"{self.keys[prev_idx][:6]}...{self.keys[prev_idx][-4:]}"
        
        logger.info(f"🔄 [KeyManager] Key Rotated ({reason}): {masked_old} (Key #{prev_idx+1}) ➔ {masked_new} (Key #{self.current_idx+1}/{len(self.keys)})")
        return new_key

    def execute_with_failover(self, func, *args, max_retries: int = 6, **kwargs):
        """429 ResourceExhausted 에러 발생 시 자동으로 다음 키로 교체 및 지능형 쿨타임 대기"""
        attempts = 0
        total_keys = max(len(self.keys), 1)
        max_total_attempts = max(max_retries, total_keys * 3)

        while attempts < max_total_attempts:
            try:
                client = self.get_client()
                return func(client, *args, **kwargs)
            except Exception as e:
                err_str = str(e).lower()
                attempts += 1
                
                # 429, Quota, ResourceExhausted 에러 감지
                if "429" in err_str or "quota" in err_str or "resourceexhausted" in err_str or "rate limit" in err_str or "exhausted" in err_str:
                    logger.warning(f"⚠️ [API 429/Quota Hit] Attempt {attempts}: {e}")
                    
                    # 만약 모든 키를 한 바퀴 돌았으면 구글 쿨타임(5~10초) 동안 잠시 숨고르기
                    if attempts % total_keys == 0:
                        logger.info("⏳ [Rate-Limiter] All keys visited once. Breathing for 5s before next pass...")
                        time.sleep(5.0)
                    else:
                        time.sleep(1.0)

                    self.rotate_key(reason="429 Quota Exceeded")
                elif "503" in err_str or "deadline" in err_str or "unavailable" in err_str:
                    logger.warning(f"⚠️ [Server Busy] Attempt {attempts}: {e}. Retrying in 3s...")
                    time.sleep(3.0)
                else:
                    logger.error(f"❌ Unhandled API Error: {e}")
                    raise e

        raise RuntimeError(f"All API keys exhausted after {attempts} attempts.")

# 싱글톤 전역 인스턴스
global_key_manager = KeyManager()
