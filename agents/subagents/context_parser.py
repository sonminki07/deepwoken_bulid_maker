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

CONTEXT_PARSER_PROMPT = """당신은 Deepwoken 빌드 메타 및 플레이 전략 분석 전문 서브 에이전트(ContextParser)입니다.
제공된 웹페이지 텍스트에서 빌드의 전체적인 의도, 목적(PvP/PvE), 난이도, 작성자 의견, 장단점, 콤보 운용 가이드를 분석하세요.

[추출 대상]
1. build_name: 빌드 통칭/이름 (예: "Flamecharm Blindseer Curved Blade")
2. build_type: "PvP", "PvE", "Hybrid", "Meme/Fun", "Boss Raid" 중 하나
3. difficulty: "Beginner", "Intermediate", "Advanced", "Expert" 중 하나
4. creator_opinion: 빌드의 주요 장점 및 설계 의도 요약 (2~3문장)
5. strengths: [장점 2~4개]
6. weaknesses: [단점 1~3개]
7. combo_guide: 딜사이클, 콤보 연계 및 운용 팁
8. author: 글 작성자/출처 채널 또는 사이트명
9. estimated_patch: 언급된 패치 버전/시즌

[출력 형식]
반드시 다음 구조의 유효한 JSON 형식으로만 응답하세요:
{
  "build_name": "...",
  "build_type": "...",
  "difficulty": "...",
  "creator_opinion": "...",
  "strengths": [ ... ],
  "weaknesses": [ ... ],
  "combo_guide": "...",
  "author": "...",
  "estimated_patch": "..."
}
"""

class ContextParserSubAgent:
    """Agent 3: 웹 콘텐츠로부터 빌드 의도, 장단점, 콤보 및 메타 정보를 추출하는 서브 에이전트"""

    def __init__(self, api_key: Optional[str] = None, model_name: str = "gemini-flash-latest"):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY is not set.")
        genai.configure(api_key=self.api_key)
        self.model_name = model_name

    def parse(self, scraped: ScrapedWebContent) -> Dict[str, Any]:
        logger.info(f"[ContextParserSubAgent] Parsing context and playstyle for {scraped.url}...")

        user_content = (
            f"=== Page Title: {scraped.title} ===\n"
            f"=== Meta Description: {scraped.meta_description} ===\n\n"
            f"=== Headings ===\n" + "\n".join(scraped.headings) + "\n\n"
            f"=== Text Content ===\n{scraped.cleaned_text[:30000]}\n"
        )

        models_to_try = ["gemini-flash-latest", "gemini-3.7-flash", "gemini-3.6-flash", "gemini-pro-latest"]
        last_err = None
        for m_name in dict.fromkeys(models_to_try):
            try:
                model = genai.GenerativeModel(
                    model_name=m_name,
                    system_instruction=CONTEXT_PARSER_PROMPT,
                    generation_config={"temperature": 0.1, "response_mime_type": "application/json"}
                )
                response = model.generate_content(user_content)
                text = response.text.strip()
                return json.loads(text)
            except Exception as e:
                last_err = e
                logger.warning(f"[ContextParserSubAgent] Model {m_name} failed ({e}), trying next fallback...")

        logger.error(f"ContextParserSubAgent failed: {last_err}")
        return {
            "build_name": scraped.title,
            "build_type": "Hybrid",
            "difficulty": "Intermediate",
            "creator_opinion": scraped.meta_description or "웹페이지에서 추출된 빌드입니다.",
            "strengths": [],
            "weaknesses": [],
            "combo_guide": "",
            "author": "Web",
            "estimated_patch": "Unknown"
        }
