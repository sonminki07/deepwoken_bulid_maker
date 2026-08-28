import os
import json
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional
from google import genai
from google.genai import types
from agents.key_manager import global_key_manager

logger = logging.getLogger(__name__)

STRICT_VISION_PROMPT = """You are a precision Vision AI specialized in reading Roblox Deepwoken in-game stat sheets and builder screens from high-resolution screenshots.

CRITICAL EXTRACTION RULES:
1. Extract the EXACT numerical digits and text visible on screen.
2. DO NOT GUESS, infer, extrapolate, or hallucinate stats.
3. If a stat value is clearly visible, extract its integer value. If not visible or 0, return 0.
4. Extract the following fields:
   - "power": Character Power/Level (e.g. 20)
   - "race": Race/Aspect (e.g. "Vesperian", "Canor", "Khan", "Capra", etc.)
   - "origin": Origin (e.g. "Castaway", "Lone Warrior", "Deepbound")
   - "oath": Oath (e.g. "Silentheart", "Starkindred", "Blindseer", "Oathless", etc.)
   - "stats": {
       "strength": int,
       "fortitude": int,
       "agility": int,
       "intelligence": int,
       "willpower": int,
       "charisma": int,
       "heavy_wep": int,
       "medium_wep": int,
       "light_wep": int
     }
   - "attunements": {
       "flamecharm": int,
       "frostdraw": int,
       "thundercall": int,
       "galebreathe": int,
       "shadowcast": int,
       "ironsing": int,
       "bloodrend": int
     }
   - "traits": {
       "vitality": int,
       "erudition": int,
       "proficiency": int,
       "songchant": int
     }
   - "combat_stats": {
       "hp": int or float,
       "posture": int or float,
       "ether": int or float,
       "tempo": int or float,
       "sanity": int or float,
       "move_speed_pct": float,
       "pve_dmg_pct": float
     }
   - "resistances": {
       "physical_slash": str,
       "physical_blunt": str,
       "physical_pierce": str,
       "fire": str,
       "ice": str,
       "wind": str,
       "shadow": str,
       "lightning": str,
       "iron": str
     }
   - "weapons": list of strings (e.g. ["Petra\'s Anchor", "Enforcer\'s Blade"])
   - "talents_visible": list of strings (talents explicitly shown in cards/inventory)
   - "mantras_visible": list of strings (mantras explicitly equipped in slots)

Output strictly as valid JSON matching this schema.
"""

class VisionExtractor:
    """고해상도 전처리 프레임 기반 초정밀 비전 추출기 (환각 원천 차단)"""

    def __init__(self, model_name: str = "gemini-flash-latest"):
        self.model_name = model_name

    def extract_from_keyframes(self, keyframe_dicts: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """선별된 키프레임들(최대 3~4장)을 Gemini Vision에 전송하여 픽셀 기반 스탯 데이터 추출"""
        if not keyframe_dicts:
            logger.warning("No keyframes provided for Vision extraction.")
            return None

        # 가장 선명하고 UI 점수가 높은 상위 키프레임 선택
        selected_frames = keyframe_dicts[:4]
        contents = []

        for kf in selected_frames:
            # 원본 및 고대비 enhanced 이미지 준비
            raw_path = kf.get("raw_path")
            if raw_path and Path(raw_path).exists():
                img_bytes = Path(raw_path).read_bytes()
                contents.append(types.Part.from_bytes(data=img_bytes, mime_type="image/jpeg"))

        if not contents:
            logger.warning("No readable keyframe image bytes found.")
            return None

        contents.append(STRICT_VISION_PROMPT)

        def _call_vision(client: genai.Client):
            candidate_models = [
                self.model_name,
                "gemini-flash-latest",
                "gemini-3.7-flash",
                "gemini-3.6-flash",
                "gemini-3.5-flash",
                "gemini-3.1-flash-lite",
            ]
            for m in candidate_models:
                try:
                    logger.info(f"Sending {len(contents)-1} high-res keyframes to Vision AI ({m})...")
                    resp = client.models.generate_content(
                        model=m,
                        contents=contents,
                        config=types.GenerateContentConfig(
                            temperature=0.0,
                            response_mime_type="application/json"
                        )
                    )
                    text = resp.text.strip()
                    parsed = json.loads(text)
                    if isinstance(parsed, list) and len(parsed) > 0:
                        parsed = parsed[0]
                    logger.info(f"✅ Vision extraction succeeded with model {m}!")
                    return parsed
                except Exception as e:
                    err_str = str(e).lower()
                    if "429" in err_str or "quota" in err_str:
                        raise e
                    logger.warning(f"Vision model {m} failed: {e}")
            raise RuntimeError("All vision candidate models failed.")

        try:
            return global_key_manager.execute_with_failover(_call_vision)
        except Exception as e:
            logger.error(f"❌ Vision extraction failover exhausted: {e}")
            return None