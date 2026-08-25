import os
import time
import logging
from typing import List, Optional
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

class KeyManager:
    """Gemini API 키 순환 및 429 쿼터 초과 시 자동 페일오버(Failover) 매니저"""

    def __init__(self, keys_str: Optional[str] = None):
        self.keys: List[str] = []
        raw_keys = keys_str or os.getenv("GEMINI_API_KEYS") or os.getenv("GEMINI_API_KEY", "")
        
        # 콤마, 세미콜론 또는 줄바꿈으로 분리된 다중 키 로드
        for k in raw_keys.replace(";", ",").replace("\n", ",").split(","):
            cleaned = k.strip()
            if cleaned and cleaned not in self.keys:
                self.keys.append(cleaned)

        self.current_idx = 0
        if not self.keys:
            logger.warning("No API keys configured in KeyManager.")
        else:
            self._apply_key(self.keys[0])

    def get_current_key(self) -> str:
        if not self.keys:
            return ""
        return self.keys[self.current_idx]

    def _apply_key(self, key: str):
        genai.configure(api_key=key)

    def rotate_key(self, reason: str = "Quota Exceeded") -> str:
        """다음 사용 가능한 키로 순환"""
        if len(self.keys) <= 1:
            logger.warning(f"Key rotation triggered ({reason}), but only 1 key is available. Waiting 10s...")
            time.sleep(10)
            return self.get_current_key()

        prev_idx = self.current_idx
        self.current_idx = (self.current_idx + 1) % len(self.keys)
        new_key = self.keys[self.current_idx]
        masked_new = f"{new_key[:6]}...{new_key[-4:]}"
        masked_old = f"{self.keys[prev_idx][:6]}...{self.keys[prev_idx][-4:]}"
        
        logger.info(f"🔄 [KeyManager] Key Rotated ({reason}): {masked_old} (Key #{prev_idx+1}) ➔ {masked_new} (Key #{self.current_idx+1}/{len(self.keys)})")
        self._apply_key(new_key)
        return new_key

    def execute_with_failover(self, func, *args, max_retries: int = 5, **kwargs):
        """429 ResourceExhausted 에러 발생 시 자동으로 다음 키로 교체 후 재시도"""
        attempts = 0
        total_keys = max(len(self.keys), 1)
        max_total_attempts = max(max_retries, total_keys * 2)

        while attempts < max_total_attempts:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                err_str = str(e).lower()
                attempts += 1
                
                # 429, Quota, ResourceExhausted 에러 감지
                if "429" in err_str or "quota" in err_str or "resourceexhausted" in err_str or "rate limit" in err_str:
                    logger.warning(f"⚠️ [API 429/Quota Hit] Attempt {attempts}: {e}")
                    self.rotate_key(reason="429 Quota Exceeded")
                    time.sleep(2)
                elif "503" in err_str or "deadline" in err_str or "unavailable" in err_str:
                    logger.warning(f"⚠️ [Server Busy] Attempt {attempts}: {e}. Retrying in 5s...")
                    time.sleep(5)
                else:
                    logger.error(f"❌ Unhandled API Error: {e}")
                    raise e

        raise RuntimeError(f"All API keys exhausted after {attempts} attempts.")

# 싱글톤 전역 인스턴스
global_key_manager = KeyManager()
