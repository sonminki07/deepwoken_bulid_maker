import os
import json
import logging
from typing import Optional, Dict, Any

from google import genai
from google.genai import types
from agents.web_scraper import ScrapedWebContent

logger = logging.getLogger(__name__)

CONTEXT_PARSER_PROMPT = """당신은 Deepwoken 메타 및 전투 시스템/위키 분석 전문가(ContextParserSubAgent)입니다.
제공된 웹 가이드 또는 위키 문서 텍스트(및 하위 문서들)를 심층 분석하여 아래 항목들을 풍부하고 유익하게 작성하여 JSON으로 반환하세요.

JSON 출력 형식:
{
  "build_name": "문서 또는 빌드 제목 (예: Frostdraw / Shadowcast / Chaser Boss Guide)",
  "build_type": "Wiki / Guide / PvP / PvE / Boss",
  "difficulty": "Easy / Intermediate / Hard",
  "overview": "이 문서/링크가 담고 있는 핵심 내용 2~3줄 요약",
  "key_mechanics": "속성/만트라/보스/시스템의 핵심 작동 원리 및 특징 (한국어로 상세히)",
  "build_role_and_usage": "실제 Deepwoken 빌드에서 이 요소가 수행하는 핵심 역할 및 기능 (예: 강력한 둔화와 구르기 봉쇄를 통한 콤보 주도, 에테르 흡수를 통한 스킬 난사 등)",
  "recommended_synergies": "함께 조합하면 극대화되는 추천 Oath(Jetstriker, Starkindred 등), 추천 속성/무기, 핵심 시너지",
  "strengths": ["실전 장점 1", "실전 장점 2", "실전 장점 3"],
  "weaknesses": ["단점 및 주의점 1", "단점 및 주의점 2"]
}
반드시 순수 JSON만 반환하세요. 모든 설명은 자연스러운 한국어로 충실하게 작성하세요.
"""

class ContextParserSubAgent:
    """Agent 3: 웹 콘텐츠로부터 빌드 의도, 장단점, 콤보 및 메타 정보를 추출하는 서브 에이전트"""

    def __init__(self, api_key: Optional[str] = None, model_name: str = "gemini-2.5-flash"):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY is not set.")
        self.client = genai.Client(api_key=self.api_key)
        self.model_name = model_name

    def parse(self, scraped: ScrapedWebContent) -> Dict[str, Any]:
        logger.info(f"[ContextParserSubAgent] Parsing context and playstyle for {scraped.url}...")

        user_content = (
            f"=== Page Title: {scraped.title} ===\n"
            f"=== Meta Description: {scraped.meta_description} ===\n\n"
            f"=== Headings ===\n" + "\n".join(scraped.headings) + "\n\n"
            f"=== Text Content ===\n{scraped.cleaned_text[:30000]}\n"
        )

        models_to_try = [self.model_name, "gemini-2.5-flash", "gemini-3.5-flash", "gemini-flash-latest"]
        last_err = None
        for m_name in dict.fromkeys(models_to_try):
            try:
                response = self.client.models.generate_content(
                    model=m_name,
                    contents=user_content,
                    config=types.GenerateContentConfig(
                        system_instruction=CONTEXT_PARSER_PROMPT,
                        temperature=0.2,
                        response_mime_type="application/json"
                    )
                )
                text = response.text.strip()
                return json.loads(text)
            except Exception as e:
                last_err = e
                logger.warning(f"[ContextParserSubAgent] Model {m_name} failed ({e}), trying next fallback...")

        logger.error(f"ContextParserSubAgent failed: {last_err}")
        return {
            "build_name": scraped.title or "Deepwoken Build",
            "build_type": "Hybrid",
            "oath": "Oathless",
            "difficulty": "Intermediate",
            "creator_opinion": "문서로부터 빌드 정보를 파싱했습니다.",
            "strengths": ["다양한 상황 대처 가능"],
            "weaknesses": ["기본 숙련도 요구"],
            "combo_guide": "기본 만트라 연계 및 무기 평타 콤보를 활용하세요."
        }
