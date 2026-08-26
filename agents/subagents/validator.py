import logging
from typing import Dict, Any
from agents.web_scraper import ScrapedWebContent

logger = logging.getLogger(__name__)

KNOWN_OATHS = [
    "Arcwarder", "Blindseer", "Contractor", "Dawnwalker", "Jetstriker",
    "Linkstrider", "Oathless", "Starkindred", "Voidwalker", "Saltchemist",
    "Bladeharper", "Silentheart", "Fadethorn"
]

class CrossValidatorAgent:
    """Agent 4: 서브 에이전트 결과 병합, Deepwoken 규칙 검증 및 최종 스키마 정제기"""

    def validate_and_merge(
        self,
        scraped: ScrapedWebContent,
        build_mechanics: Dict[str, Any],
        context_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        logger.info(f"[CrossValidatorAgent] Merging and validating data for {scraped.url}...")

        # 1. 메타데이터 구성
        source_meta = {
            "title": context_data.get("build_name") or scraped.title,
            "channel": context_data.get("author") or "Web Source",
            "url": scraped.url,
            "upload_date": "N/A",
            "estimated_patch": context_data.get("estimated_patch") or "Current Patch"
        }

        # 2. 빌드 요약 구성
        build_summary = {
            "build_name": context_data.get("build_name") or scraped.title,
            "build_type": self._normalize_build_type(context_data.get("build_type")),
            "difficulty": self._normalize_difficulty(context_data.get("difficulty")),
            "overview": context_data.get("overview") or scraped.meta_description or "웹에서 수집된 딥위큰 가이드 정보입니다.",
            "key_mechanics": context_data.get("key_mechanics") or "기본 시스템 메커니즘이 수록되어 있습니다.",
            "build_role_and_usage": context_data.get("build_role_and_usage") or "빌드 내 핵심 요소 및 스킬 연계 지원",
            "recommended_synergies": context_data.get("recommended_synergies") or "다양한 속성 및 Oath와 범용적 연계 가능",
            "creator_opinion": context_data.get("overview") or context_data.get("creator_opinion") or scraped.meta_description or "웹에서 수집된 정보입니다.",
            "strengths": context_data.get("strengths", []),
            "weaknesses": context_data.get("weaknesses", [])
        }

        # 3. 스탯 정제
        raw_stats = build_mechanics.get("stats", {})
        cleaned_stats = {
            "strength": self._clean_int(raw_stats.get("strength")),
            "fortitude": self._clean_int(raw_stats.get("fortitude")),
            "agility": self._clean_int(raw_stats.get("agility")),
            "intelligence": self._clean_int(raw_stats.get("intelligence")),
            "willpower": self._clean_int(raw_stats.get("willpower")),
            "charisma": self._clean_int(raw_stats.get("charisma")),
            "heavy_wep": self._clean_int(raw_stats.get("heavy_wep")),
            "medium_wep": self._clean_int(raw_stats.get("medium_wep")),
            "light_wep": self._clean_int(raw_stats.get("light_wep")),
        }

        # 4. 속성(Attunement) 정제
        raw_att = build_mechanics.get("attunements", {})
        cleaned_att = {
            "flamecharm": self._clean_int(raw_att.get("flamecharm")),
            "frostdraw": self._clean_int(raw_att.get("frostdraw")),
            "galebreathe": self._clean_int(raw_att.get("galebreathe")),
            "thundercall": self._clean_int(raw_att.get("thundercall")),
            "shadowcast": self._clean_int(raw_att.get("shadowcast")),
            "ironsing": self._clean_int(raw_att.get("ironsing")),
        }

        # 5. Oath 정제
        raw_oath = str(build_mechanics.get("oath", "Oathless")).strip()
        matched_oath = "Oathless"
        for known in KNOWN_OATHS:
            if known.lower() in raw_oath.lower():
                matched_oath = known
                break

        # 6. 최종 통합 딕셔너리 생성
        merged_build = {
            "video_meta": source_meta,
            "build_summary": build_summary,
            "race": str(build_mechanics.get("race", "N/A")),
            "origin": str(build_mechanics.get("origin", "N/A")),
            "oath": matched_oath,
            "resonance": str(build_mechanics.get("resonance", "N/A")),
            "murmur": str(build_mechanics.get("murmur", "N/A")),
            "stats": cleaned_stats,
            "attunements": cleaned_att,
            "weapons": build_mechanics.get("weapons", []),
            "talents": build_mechanics.get("talents", []),
            "mantras": build_mechanics.get("mantras", []),
            "shrine_of_order_path": build_mechanics.get("shrine_of_order_path", ""),
            "equipment": build_mechanics.get("equipment", []),
            "combo_guide": context_data.get("combo_guide", "")
        }

        logger.info(f"CrossValidatorAgent validation complete: '{build_summary['build_name']}'")
        return merged_build

    def _clean_int(self, val: Any) -> int:
        if val is None:
            return 0
        try:
            v = int(val)
            return max(0, min(v, 1024))
        except (ValueError, TypeError):
            return 0

    def _normalize_build_type(self, b_type: Any) -> str:
        valid = ["PvP", "PvE", "Hybrid", "Meme/Fun", "Boss Raid"]
        if isinstance(b_type, str):
            for v in valid:
                if v.lower() == b_type.strip().lower():
                    return v
        return "Hybrid"

    def _normalize_difficulty(self, diff: Any) -> str:
        valid = ["Beginner", "Intermediate", "Advanced", "Expert"]
        if isinstance(diff, str):
            for v in valid:
                if v.lower() == diff.strip().lower():
                    return v
        return "Intermediate"
