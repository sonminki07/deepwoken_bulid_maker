import os
import json
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional
from google import genai
from google.genai import types
from agents.key_manager import global_key_manager

logger = logging.getLogger(__name__)

STRICT_VISION_PROMPT = """You are an absolute zero-hallucination Vision AI specialized in reading Roblox Deepwoken in-game character sheets (Stat Sheets), inventory, and hotbars from high-resolution screenshots and cropped panels.

CRITICAL INSTRUCTIONS:
1. Extract ONLY what is physically and visually legible on the screen.
2. DO NOT GUESS, infer, extrapolate, or hallucinate stats. If not shown or 0, return 0.
3. Roblox Deepwoken Stat Sheet UI Structure:
   - Header Bar:
     * Name: character name (e.g. "Phoenix Jura")
     * Level: "POWER [number]" (e.g. 20)
     * Origin: "ORIGIN: [name]" (e.g. "Castaway", "Deepbound")
     * Oath: "OATH: [name]" (e.g. "Linkstrider", "Silentheart", "Oathless")
     * Race: "ASPECT: [name]" (e.g. "Gremor", "Capra", "Felinor")
   - 4 Trait Circles (Upper right):
     * Top-Left: Vitality
     * Top-Right: Erudition
     * Bottom-Left: Proficiency
     * Bottom-Right: Songchant
   - Attributes Box (Middle right):
     * BODY: Strength, Fortitude, Agility
     * MIND: Intelligence, Willpower, Charisma
     * WEAPONS: Heavy Wep, Medium Wep, Light Wep
     * ELEMENTS: Flamecharm, Frostdraw, Thundercall, Galebreathe, Shadowcast, Ironsing, Bloodrend
   - Bottom Left Box (STATS):
     * Health (HP), Posture, Ether, Tempo, Sanity, Speed %, Monster Dmg %
   - Bottom Right Box (RESISTANCES):
     * Slash %, Blunt %, Pierce %, Fire %, Ice %, Wind %, Shadow %, Lightning %, Iron %
   - Inventory / Hotbar (Left & Bottom):
     * Equipped weapon/attire, visible inventory items, hotbar mantra names.

Output strictly as valid JSON matching this schema:
{
  "character_name": str or null,
  "power": int,
  "race": str,
  "origin": str,
  "oath": str,
  "traits": {
    "vitality": int,
    "erudition": int,
    "proficiency": int,
    "songchant": int
  },
  "stats": {
    "strength": int,
    "fortitude": int,
    "agility": int,
    "intelligence": int,
    "willpower": int,
    "charisma": int,
    "heavy_wep": int,
    "medium_wep": int,
    "light_wep": int
  },
  "attunements": {
    "flamecharm": int,
    "frostdraw": int,
    "thundercall": int,
    "galebreathe": int,
    "shadowcast": int,
    "ironsing": int,
    "bloodrend": int
  },
  "combat_stats": {
    "hp": float,
    "posture": float,
    "ether": float,
    "tempo": float,
    "sanity": float,
    "move_speed_pct": str,
    "pve_monster_dmg_pct": str
  },
  "resistances": {
    "physical_slash": str,
    "physical_blunt": str,
    "physical_pierce": str,
    "fire": str,
    "ice": str,
    "wind": str,
    "shadow": str,
    "lightning": str,
    "iron": str
  },
  "equipped_items": list of str,
  "inventory_items": list of str,
  "talents_visible": list of str,
  "mantras_visible": list of str
}
"""

class VisionExtractor:
    """고해상도 전처리 프레임 기반 초정밀 비전 추출기 (환각 원천 차단)"""

    def __init__(self, model_name: str = "gemini-flash-latest"):
        self.model_name = model_name

    def extract_from_keyframes(self, keyframe_dicts: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """선별된 키프레임들(스탯창 크롭 + 인벤토리 크롭 + 전체화면)을 비전 AI에 전송하여 100% 쌩 실측 데이터 추출"""
        if not keyframe_dicts:
            logger.warning("No keyframes provided for Vision extraction.")
            return None

        # 가장 선명하고 UI 점수가 높은 상위 2개 키프레임 선별 투입
        selected_frames = keyframe_dicts[:2]
        contents = []

        for kf in selected_frames:
            # 1) 우측 스탯창 고화질 크롭 이미지 최우선 투입
            stat_crop_path = kf.get("stat_crop_path")
            if stat_crop_path and Path(stat_crop_path).exists():
                img_bytes = Path(stat_crop_path).read_bytes()
                contents.append(types.Part.from_bytes(data=img_bytes, mime_type="image/jpeg"))

            # 2) 전체 원본 프레임 투입
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
                "gemini-3.5-flash",
                "gemini-flash-lite-latest",
                "gemini-3.1-flash-lite"
            ]
            for m in candidate_models:
                try:
                    logger.info(f"Sending {len(contents)-1} high-res visual crops/frames to Vision AI ({m})...")
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

                    # 100% 실측 쌩 데이터 콘솔 로그 즉시 출력
                    self._print_raw_ground_truth(parsed)
                    logger.info(f"✅ Vision raw extraction succeeded with model {m}!")
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

    def _print_raw_ground_truth(self, data: Dict[str, Any]):
        """추출된 100% 쌩(Raw) 시각 데이터를 터미널 및 로그에 명확하게 출력"""
        print("\n" + "="*70)
        print("📊 [1단계: 100% 실측 원시(Raw) 시각 데이터 추출 완료]")
        print("="*70)
        print(f"• 캐릭터/레벨 : {data.get('character_name', 'N/A')} (Power {data.get('power', 20)})")
        print(f"• 종족/출신/서약: {data.get('race', 'N/A')} / {data.get('origin', 'N/A')} / {data.get('oath', 'N/A')}")
        
        traits = data.get("traits", {})
        print(f"• 특성 (Traits): Vitality {traits.get('vitality',0)}, Erudition {traits.get('erudition',0)}, Proficiency {traits.get('proficiency',0)}, Songchant {traits.get('songchant',0)}")
        
        stats = data.get("stats", {})
        print(f"• 기본 스탯 (Stats): STR {stats.get('strength',0)}, FTD {stats.get('fortitude',0)}, AGL {stats.get('agility',0)}, INT {stats.get('intelligence',0)}, WLL {stats.get('willpower',0)}, CHA {stats.get('charisma',0)}")
        print(f"• 무기 수치 : Heavy {stats.get('heavy_wep',0)}, Medium {stats.get('medium_wep',0)}, Light {stats.get('light_wep',0)}")
        
        atts = data.get("attunements", {})
        active_atts = {k: v for k, v in atts.items() if v > 0}
        print(f"• 속성 (Attunements): {active_atts if active_atts else 'None (Attunementless)'}")
        
        c_stats = data.get("combat_stats", {})
        print(f"• 전투 수치 : HP {c_stats.get('hp',0)}, Posture {c_stats.get('posture',0)}, Ether {c_stats.get('ether',0)}, Tempo {c_stats.get('tempo',0)}, Sanity {c_stats.get('sanity',0)}, Speed {c_stats.get('move_speed_pct',0)}, Monster Dmg {c_stats.get('pve_monster_dmg_pct',0)}")
        
        res = data.get("resistances", {})
        print(f"• 7대 저항력 (Resistances): {res}")
        print("="*70 + "\n")