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
    """누락되거나 불명확한 스탯/장비 데이터를 설명란 링크(deepwoken.co) 스크래핑 및 Google 실시간 검색으로 100% 보강하는 에이전트"""

    def __init__(self, api_key: Optional[str] = None, model_name: str = "gemini-3.6-flash"):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY is not set.")
        from agents.key_manager import global_key_manager
        self.client = global_key_manager.get_client()
        self.model_name = model_name

    def enrich_if_missing(self, build_data: Dict[str, Any], raw_meta: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """엄격한 신뢰도 판정(Strict Confidence Gate)을 거쳐 스탯이 불완전할 경우 설명란 크롤링 및 구글 검색으로 자동 보강"""
        stats = build_data.get("stats", {}) or build_data.get("stats_and_attunements", {}).get("stats", {})
        attunements = build_data.get("attunements", {}) or build_data.get("stats_and_attunements", {}).get("attunements", {})
        
        stat_points = sum([v for v in stats.values() if isinstance(v, (int, float))])
        att_points = sum([v for v in attunements.values() if isinstance(v, (int, float))])
        total_points = stat_points + att_points

        # [엄격한 신뢰도 판정]: 총합이 200pt 미만이거나 0스탯 환각인 경우
        is_unreliable = total_points < 200 or stat_points == 0

        if not is_unreliable:
            return build_data

        logger.info(f"⚠️ [StatInferenceAgent] Unreliable/missing stats detected (Total: {total_points}pt). Launching deep search and builder grounding...")
        
        raw_meta = raw_meta or {}
        builder_url = raw_meta.get("extra", {}).get("builder_url") or self._find_builder_url(raw_meta.get("description", ""))
        
        # 1. 설명란 deepwoken.co 빌더 링크가 있으면 직통 크롤링
        if builder_url:
            scraped = self._scrape_builder_url(builder_url)
            if scraped and "stats" in scraped:
                logger.info(f"🎯 [StatInferenceAgent] Successfully scraped exact stats from deepwoken.co: {builder_url}")
                build_data["stats"] = scraped["stats"]
                if "attunements" in scraped:
                    build_data["attunements"] = scraped["attunements"]
                return build_data

        # 2. 설명란 링크가 없거나 실패 시 Google/DDG 실시간 검색 + Gemini 추론 보강
        inferred = self._self_query_and_infer(build_data, raw_meta)
        if inferred:
            if "stats" in inferred and inferred["stats"]:
                build_data["stats"] = inferred["stats"]
            if "attunements" in inferred and inferred["attunements"]:
                build_data["attunements"] = inferred["attunements"]
            if "shrine_of_order_progression" in inferred:
                build_data["shrine_of_order_progression"] = inferred["shrine_of_order_progression"]
            logger.info("✅ [StatInferenceAgent] Successfully enriched missing stats via autonomous web search!")
            
        return build_data

    def _find_builder_url(self, text: str) -> Optional[str]:
        import re
        matches = re.findall(r'(https?://(?:www\.)?deepwoken\.co/builder\S*)', text)
        return matches[0] if matches else None

    def _scrape_builder_url(self, builder_url: str) -> Optional[Dict[str, Any]]:
        """deepwoken.co/builder 링크에서 스탯 데이터를 직접 추출"""
        try:
            import urllib.request
            from bs4 import BeautifulSoup
            req = urllib.request.Request(builder_url, headers={'User-Agent': 'Mozilla/5.0'})
            html = urllib.request.urlopen(req, timeout=5).read().decode('utf-8')
            soup = BeautifulSoup(html, 'html.parser')
            
            # 페이지 텍스트 내에서 스탯 및 탤런트 파싱
            page_text = soup.get_text()
            logger.debug(f"Scraped {len(page_text)} chars from {builder_url}")
            
            prompt = f"""
다음은 deepwoken.co/builder 페이지의 텍스트입니다.
스탯(Strength, Fortitude, Agility, Intelligence, Willpower, Charisma, Heavy/Medium/Light Weapon) 및
속성(Shadowcast, Flamecharm, Frostdraw, Thundercall, Galebreathe, Ironsing)을 JSON으로 추출하세요:
=== Page Text ===
{page_text[:4000]}
===
반드시 순수 JSON만 반환하세요.
"""
            resp = self.client.models.generate_content(
                model=self.model_name,
                contents=[prompt],
                config=types.GenerateContentConfig(temperature=0.0, response_mime_type="application/json")
            )
            return json.loads(resp.text.strip())
        except Exception as e:
            logger.warning(f"Builder scrape failed for {builder_url}: {e}")
            return None

    def _self_query_and_infer(self, build_data: Dict[str, Any], raw_meta: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        channel = raw_meta.get("channel", "")
        b_name = build_data.get("build_summary", {}).get("build_name") or raw_meta.get("title", "Deepwoken Build")
        oath = build_data.get("oath") or "None"
        talents = [t.get("name") if isinstance(t, dict) else str(t) for t in build_data.get("talents", [])]
        
        # Google/DDG 실시간 검색 수행
        search_context = []
        try:
            query = f"Deepwoken {channel} {b_name} build stats requirements wiki"
            with DDGS() as ddgs:
                results = list(ddgs.text(query, max_results=4))
                for r in results:
                    search_context.append(f"Title: {r.get('title')}\nSnippet: {r.get('body')}")
        except Exception as e:
            logger.warning(f"Search query failed in StatInferenceAgent: {e}")

        prompt_input = (
            f"=== Video & Creator ===\n"
            f"Creator: {channel}\n"
            f"Title: {raw_meta.get('title')}\n"
            f"Build Name: {b_name}\n"
            f"Oath: {oath}\n"
            f"Talents: {', '.join(talents[:15])}\n"
            f"Description Snippet: {raw_meta.get('description', '')[:500]}\n"
            f"=== Web Search Results ===\n"
            + "\n---\n".join(search_context)
        )

        from agents.key_manager import global_key_manager
        
        def _call_inferrer(client: genai.Client):
            for m_name in ["gemini-3.5-flash", "gemini-flash-lite-latest", "gemini-3.1-flash-lite"]:
                try:
                    response = client.models.generate_content(
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
                    err_str = str(e).lower()
                    if "429" in err_str or "quota" in err_str:
                        raise e
                    logger.warning(f"Model {m_name} failed in StatInferenceAgent: {e}")
            return None

        try:
            return global_key_manager.execute_with_failover(_call_inferrer)
        except Exception as e:
            logger.error(f"StatInferenceAgent failover exhausted: {e}")
            return None
