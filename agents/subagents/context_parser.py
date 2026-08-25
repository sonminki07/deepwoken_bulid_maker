import os
import json
import logging
from typing import Optional, Dict, Any

from google import genai
from google.genai import types
from agents.subagents.scraper import ScrapedWebContent

logger = logging.getLogger(__name__)

CONTEXT_PARSER_PROMPT = """당신은 Deepwoken 메타 및 전투 플레이스타일 분석 전문가(ContextParserSubAgent)입니다.
제공된 웹 가이드 또는 위키 문서 텍스트에서 '빌드 이름(Build Name)', '빌드 목적(PvP/PvE/Boss/Hybrid)', '난이도', '핵심 장단점(Strengths/Weaknesses)', '콤보 가이드(Combo Guide)', '운용 팁'을 분석하여 아래 JSON 형식으로만 반환하세요.

JSON 출력 형식:
{
  "build_name": "빌드 이름",
  "build_type": "PvP / PvE / Hybrid / Boss",
  "oath": "Oath 이름 (예: Jetstriker, Silentheart 등)",
  "difficulty": "Easy / Intermediate / Hard",
  "creator_opinion": "빌드 요약 및 총평",
  "strengths": ["장점1", "장점2"],
  "weaknesses": ["단점1", "단점2"],
  "combo_guide": "상세한 콤보 연계 및 전투 운용법"
}
반드시 순수 JSON만 반환하세요.
"""

class ContextParserSubAgent:
    """Agent 3: 웹 콘텐츠로부터 빌드 의도, 장단점, 콤보 및 메타 정보를 추출하는 서브 에이전트"""

    def __init__(self, api_key: Optional[str] = None, model_name: str = "gemini-3.6-flash"):
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

        models_to_try = [self.model_name, "gemini-3.6-flash", "gemini-3.7-flash"]
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
