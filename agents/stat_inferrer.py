import os
import json
import logging
from typing import Dict, Any, Optional
from google import genai
from google.genai import types
from duckduckgo_search import DDGS

logger = logging.getLogger(__name__)

STAT_INFERENCE_PROMPT = """당신은 Roblox Deepwoken 게임의 스탯 역산 및 빌드 메타 최고 전문가(StatInferenceAgent)입니다.
분석 대상 빌드에 스탯 정보가 누락되어 있습니다. 제공된 빌드명, 탤런트, 만트라, 무기, Oath, 검색 결과 단서들을 종합하여
가장 표준적이고 최적화된 딥위큰 스탯(총합 약 250~330 포인트)과 Shrine of Order 분배를 논리적으로 역산하여 완성된 JSON으로 반환하세요.

[필수 역산 규칙]
1. 핵심 탤런트 요구치 반영 (예: Brick Wall -> Fortitude 100, Willpower 100 / Million Ton Piercer -> Strength 90 / Conditioned Runner -> Agility 25 등)
2. 무기 및 속성 요구치 반영 (예: Pale Briar -> Heavy 80, Frostdraw 80 / Kyrsglaive -> Heavy 75, Gale 80 등)
3. Oath 요구치 반영 (예: Silentheart -> Strength 40, Agility 40, Weapon 75 / Starkindred -> Strength 40 등)
4. 6대 기본 스탯 및 무기/속성 수치의 합이 250~330 사이의 유효한 완성형 빌드가 되도록 숫자를 정확히 기입하세요.

JSON 출력 형식:
{
  "stats": {
    "strength": 40,
    "fortitude": 50,
    "agility": 25,
    "intelligence": 0,
    "willpower": 40,
    "charisma": 25,
    "heavy_wep": 90,
    "medium_wep": 0,
    "light_wep": 0
  },
  "attunements": {
    "flamecharm": 0,
    "frostdraw": 0,
    "thundercall": 0,
    "galebreathe": 0,
    "shadowcast": 0,
    "ironsing": 90,
    "bloodrend": 0
  },
  "shrine_of_order_progression": {
    "pre_shrine": {"strength": 40, "fortitude": 50, "willpower": 40},
    "post_shrine_priority": ["Ironsing 90 마스터", "Heavy Weapon 90 달성"]
  }
}
반드시 순수 JSON만 반환하세요.
"""

class StatInferenceAgent:
    """누락된 스탯/장비 데이터를 자가 검색(Self-Search) 및 AI 질의응답으로 자동 복원하는 에이전트"""

    def __init__(self, api_key: Optional[str] = None, model_name: str = "gemini-2.5-flash"):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY is not set.")
        self.client = genai.Client(api_key=self.api_key)
        self.model_name = model_name

    def enrich_if_missing(self, build_data: Dict[str, Any], raw_meta: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """스탯이 0이거나 비어있으면 스스로 검색하고 AI 질의응답을 통해 복원"""
        stats = build_data.get("stats", {})
        attunements = build_data.get("attunements", {})
        
        total_points = sum([v for v in stats.values() if isinstance(v, (int, float))]) + \
                       sum([v for v in attunements.values() if isinstance(v, (int, float))])

        if total_points >= 50:
            return build_data

        logger.info("⚠️ [StatInferenceAgent] Missing/empty stats detected! Launching autonomous self-querying & search enrichment...")
        inferred = self._self_query_and_infer(build_data, raw_meta or {})
        if inferred:
            build_data["stats"] = inferred.get("stats", stats)
            build_data["attunements"] = inferred.get("attunements", attunements)
            if "shrine_of_order_progression" in inferred:
                build_data["shrine_of_order_progression"] = inferred["shrine_of_order_progression"]
            logger.info("✅ [StatInferenceAgent] Successfully enriched missing stats via autonomous inference!")
        return build_data

    def _self_query_and_infer(self, build_data: Dict[str, Any], raw_meta: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        b_name = build_data.get("build_summary", {}).get("build_name") or raw_meta.get("title", "Deepwoken Build")
        oath = build_data.get("oath") or "None"
        talents = [t.get("name") if isinstance(t, dict) else str(t) for t in build_data.get("talents", [])]
        mantras = [m.get("name") if isinstance(m, dict) else str(m) for m in build_data.get("mantras", [])]
        
        # 1. 자가 실시간 검색 수행
        search_context = []
        try:
            query = f"Deepwoken {b_name} {oath} build stats requirements wiki"
            with DDGS() as ddgs:
                results = list(ddgs.text(query, max_results=3))
                for r in results:
                    search_context.append(f"Title: {r.get('title')}\nSnippet: {r.get('body')}")
        except Exception as e:
            logger.warning(f"Search query failed in StatInferenceAgent: {e}")

        prompt_input = (
            f"=== Build Name: {b_name} ===\n"
            f"=== Video Title: {raw_meta.get('title', 'N/A')} ===\n"
            f"=== Oath: {oath} ===\n"
            f"=== Identified Talents: {', '.join(talents[:15])} ===\n"
            f"=== Identified Mantras: {', '.join(mantras[:10])} ===\n"
            f"=== Search Context ===\n" + "\n---\n".join(search_context)
        )

        for m_name in [self.model_name, "gemini-2.5-flash", "gemini-3.5-flash"]:
            try:
                response = self.client.models.generate_content(
                    model=m_name,
                    contents=prompt_input,
                    config=types.GenerateContentConfig(
                        system_instruction=STAT_INFERENCE_PROMPT,
                        temperature=0.1,
                        response_mime_type="application/json"
                    )
                )
                text = response.text.strip()
                return json.loads(text)
            except Exception as e:
                logger.warning(f"Model {m_name} failed in StatInferenceAgent: {e}")
        return None
