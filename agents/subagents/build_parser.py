import os
import json
import logging
import warnings
from typing import Dict, Any, Optional

with warnings.catch_warnings():
    warnings.simplefilter("ignore", category=FutureWarning)
    import google.generativeai as genai

from agents.web_scraper import ScrapedWebContent

logger = logging.getLogger(__name__)

BUILD_PARSER_PROMPT = """당신은 Deepwoken 인게임 메커니즘 분석 전문 서브 에이전트(BuildParser)입니다.
제공된 웹페이지 텍스트 및 표 데이터에서 캐릭터 빌드의 수치와 게임 요소(스탯, 속성, Oath, 탤런트, 만트라, 무기 등)를 정밀 추출하세요.

[추출 대상]
1. stats: strength, fortitude, agility, intelligence, willpower, charisma, heavy_wep, medium_wep, light_wep (정수값)
2. attunements: flamecharm, frostdraw, galebreathe, thundercall, shadowcast, ironsing (정수값)
3. oath, race, origin, murmur, resonance (문자열)
4. weapons: [{"name": str, "type": str, "enchant": str, "stars": int}]
5. talents: [{"name": str, "category": str, "is_core": bool}]
6. mantras: [{"name": str, "attunement": str, "is_core": bool, "modifications": str}]
7. equipment: [{"name": str, "slot": str, "pip_summary": str}]
8. shrine_of_order_path: Shrine of Order 관련 스탯 투자 순서

[출력 형식]
반드시 다음 키들을 포함하는 유효한 JSON 형식으로만 응답하세요:
{
  "stats": { ... },
  "attunements": { ... },
  "oath": "...",
  "race": "...",
  "origin": "...",
  "murmur": "...",
  "resonance": "...",
  "weapons": [ ... ],
  "talents": [ ... ],
  "mantras": [ ... ],
  "equipment": [ ... ],
  "shrine_of_order_path": "..."
}
"""

class BuildParserSubAgent:
    """Agent 2: 웹 콘텐츠로부터 스탯, 스킬, 장비, 탤런트 메커니즘을 추출하는 서브 에이전트"""

    def __init__(self, api_key: Optional[str] = None, model_name: str = "gemini-2.5-flash-lite"):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY is not set.")
        genai.configure(api_key=self.api_key)
        self.model_name = model_name

    def parse(self, scraped: ScrapedWebContent) -> Dict[str, Any]:
        logger.info(f"[BuildParserSubAgent] Parsing build mechanics for {scraped.url}...")
        
        user_content = (
            f"=== Page Title: {scraped.title} ===\n"
            f"=== Meta Description: {scraped.meta_description} ===\n\n"
            f"=== Tables Found ===\n{scraped.tables_text}\n\n"
            f"=== Page Text Content ===\n{scraped.cleaned_text[:30000]}\n"
        )

        models_to_try = [self.model_name, "gemini-2.5-flash-lite", "gemini-flash-latest", "gemini-2.5-pro"]
        last_err = None
        for m_name in dict.fromkeys(models_to_try):
            try:
                model = genai.GenerativeModel(
                    model_name=m_name,
                    system_instruction=BUILD_PARSER_PROMPT,
                    generation_config={"temperature": 0.1, "response_mime_type": "application/json"}
                )
                response = model.generate_content(user_content)
                text = response.text.strip()
                return json.loads(text)
            except Exception as e:
                last_err = e
                logger.warning(f"[BuildParserSubAgent] Model {m_name} failed ({e}), trying next fallback...")

        logger.error(f"BuildParserSubAgent failed: {last_err}")
        return {
            "stats": {},
            "attunements": {},
            "oath": "Unknown",
            "weapons": [],
            "talents": [],
            "mantras": []
        }
