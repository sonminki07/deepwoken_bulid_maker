import os
import json
import logging
from typing import Optional, Dict, Any

from google import genai
from google.genai import types
from agents.subagents.scraper import ScrapedWebContent

logger = logging.getLogger(__name__)

BUILD_PARSER_PROMPT = """당신은 Deepwoken 빌드 구조화 전문가(BuildParserSubAgent)입니다.
제공된 웹 가이드 또는 위키 문서 텍스트에서 '스탯(Attributes)', '속성(Attunements)', '마스터리(Weapon Mastery)', '만트라(Mantras)', '탤런트(Talents)', '장비(Equipment)' 정보를 추출하여 아래 JSON 형식으로만 반환하세요.

JSON 출력 형식:
{
  "stats": {
    "strength": 0,
    "fortitude": 0,
    "agility": 0,
    "intelligence": 0,
    "willpower": 0,
    "charisma": 0
  },
  "attunements": {
    "flamecharm": 0,
    "frostdraw": 0,
    "thundercall": 0,
    "galebreathe": 0,
    "shadowcast": 0,
    "ironsing": 0
  },
  "weapon_mastery": {
    "type": "Medium / Heavy / Light",
    "points": 0
  },
  "talents": ["탤런트1", "탤런트2"],
  "mantras": ["만트라1", "만트라2"],
  "equipment_recommendations": {
    "outfit": "추천 의상",
    "weapon": "추천 무기",
    "enchants": ["추천 인챈트"],
    "accessories": ["추천 악세서리"]
  }
}
반드시 순수 JSON만 반환하세요.
"""

class BuildParserSubAgent:
    """Agent 2: 웹 콘텐츠로부터 스탯, 스킬, 장비, 탤런트 메커니즘을 추출하는 서브 에이전트"""

    def __init__(self, api_key: Optional[str] = None, model_name: str = "gemini-3.6-flash"):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY is not set.")
        self.client = genai.Client(api_key=self.api_key)
        self.model_name = model_name

    def parse(self, scraped: ScrapedWebContent) -> Dict[str, Any]:
        logger.info(f"[BuildParserSubAgent] Parsing build mechanics for {scraped.url}...")
        
        user_content = (
            f"=== Page Title: {scraped.title} ===\n"
            f"=== Meta Description: {scraped.meta_description} ===\n\n"
            f"=== Tables Found ===\n{scraped.tables_text}\n\n"
            f"=== Page Text Content ===\n{scraped.cleaned_text[:30000]}\n"
        )

        models_to_try = [self.model_name, "gemini-3.6-flash", "gemini-3.7-flash"]
        last_err = None
        for m_name in dict.fromkeys(models_to_try):
            try:
                response = self.client.models.generate_content(
                    model=m_name,
                    contents=user_content,
                    config=types.GenerateContentConfig(
                        system_instruction=BUILD_PARSER_PROMPT,
                        temperature=0.1,
                        response_mime_type="application/json"
                    )
                )
                text = response.text.strip()
                return json.loads(text)
            except Exception as e:
                last_err = e
                logger.warning(f"[BuildParserSubAgent] Model {m_name} failed ({e}), trying next fallback...")

        logger.error(f"BuildParserSubAgent failed: {last_err}")
        return {
            "stats": {},
            "attunements": {},
            "weapon_mastery": {"type": "Medium", "points": 0},
            "talents": [],
            "mantras": [],
            "equipment_recommendations": {}
        }
