"""Raw Build Data Model and Reconciliation Engine for Deepwoken Build Analyzer.

This module defines the unified raw data container (RawBuildData) and the multi-source
reconciliation engine (BuildDataReconciler) adhering to the strict priority hierarchy:
1st: Vision / OCR ground truth pixel data (Post-Shrine final & Pre-Shrine target sheets)
2nd: deepwoken.co builder scraped data
3rd: Gemini multimodal subtitles/audio/video narrative analysis
"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field, asdict
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)

# Standard Deepwoken attribute definitions
CORE_ATTRIBUTES: List[str] = [
    "strength",
    "fortitude",
    "agility",
    "intelligence",
    "willpower",
    "charisma",
]

WEAPON_ATTRIBUTES: List[str] = [
    "heavy_wep",
    "medium_wep",
    "light_wep",
]

ATTUNEMENT_KEYS: List[str] = [
    "flamecharm",
    "frostdraw",
    "thundercall",
    "galebreathe",
    "shadowcast",
    "ironsing",
    "bloodrend",
]

TRAIT_KEYS: List[str] = [
    "vitality",
    "erudition",
    "proficiency",
    "songchant",
]

STAT_ALIAS_MAP: Dict[str, str] = {
    "strength": "strength", "str": "strength",
    "fortitude": "fortitude", "ftd": "fortitude", "fort": "fortitude",
    "agility": "agility", "agl": "agility", "agi": "agility",
    "intelligence": "intelligence", "int": "intelligence", "intel": "intelligence",
    "willpower": "willpower", "wll": "willpower", "wil": "willpower",
    "charisma": "charisma", "cha": "charisma", "char": "charisma",
    "heavy_wep": "heavy_wep", "heavy_weapon": "heavy_wep", "heavy": "heavy_wep", "hvy": "heavy_wep",
    "medium_wep": "medium_wep", "medium_weapon": "medium_wep", "medium": "medium_wep", "med": "medium_wep",
    "light_wep": "light_wep", "light_weapon": "light_wep", "light": "light_wep", "lht": "light_wep",
}

ATTUNEMENT_ALIAS_MAP: Dict[str, str] = {
    "flamecharm": "flamecharm", "flame": "flamecharm", "fire": "flamecharm",
    "frostdraw": "frostdraw", "frost": "frostdraw", "ice": "frostdraw",
    "thundercall": "thundercall", "thunder": "thundercall", "lightning": "thundercall",
    "galebreathe": "galebreathe", "galebreath": "galebreathe", "gale": "galebreathe", "wind": "galebreathe",
    "shadowcast": "shadowcast", "shadow": "shadowcast",
    "ironsing": "ironsing", "iron": "ironsing", "metal": "ironsing",
    "bloodrend": "bloodrend", "blood": "bloodrend",
}

DEFAULT_TARGET_STAT_CAP: int = 330


@dataclass
class RawBuildData:
    """원시 빌드 데이터 컨테이너.
    
    비전 AI(키프레임 OCR), 빌더 스크래퍼, Gemini VLM 영상 분석으로부터
    추출된 모든 원시 데이터를 온전히 수집 및 보존합니다.
    """
    video_id: str
    video_meta: Dict[str, Any] = field(default_factory=dict)
    pre_shrine_raw: Optional[Dict[str, Any]] = None
    post_shrine_raw: Optional[Dict[str, Any]] = None
    builder_scraped: Optional[Dict[str, Any]] = None
    vlm_narrative: Optional[Dict[str, Any]] = None
    captured_keyframes: List[Dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """데이터 클래스를 딕셔너리로 직렬화"""
        return asdict(self)

    def to_json(self, indent: int = 2) -> str:
        """데이터 클래스를 JSON 문자열로 직렬화"""
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=indent)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "RawBuildData":
        """딕셔너리로부터 RawBuildData 인스턴스 복원"""
        return cls(
            video_id=str(data.get("video_id", "")),
            video_meta=dict(data.get("video_meta") or {}),
            pre_shrine_raw=data.get("pre_shrine_raw"),
            post_shrine_raw=data.get("post_shrine_raw"),
            builder_scraped=data.get("builder_scraped"),
            vlm_narrative=data.get("vlm_narrative"),
            captured_keyframes=list(data.get("captured_keyframes") or []),
        )


class BuildDataReconciler:
    """다중 소스 빌드 데이터 정합성 조정 및 정규화 엔진.
    
    우선순위 계층(Priority Hierarchy):
    1순위: 비전/OCR 실측 픽셀 데이터 (Post-Shrine 완성본 및 Pre-Shrine 목표치)
    2순위: deepwoken.co 빌더 스크래핑 데이터 (builder_scraped)
    3순위: Gemini 멀티모달 자막/오디오/VLM 서술 데이터 (vlm_narrative)
    
    주요 기능:
    - Pre-Shrine 및 Post-Shrine 스탯 분리 및 무결성 정합
    - 330pt 스탯 상한선(Deepwoken Cap) 검증 및 리포팅
    - is_shrine_build (사원 빌드 vs 단일 완성 빌드) 자동 판정
    - 원시 데이터 원본을 `_raw_source_data` 키로 100% 무손실 보존
    - structurer.py 표준 스키마와 100% 호환되는 정규화 딕셔너리 산출
    """

    def __init__(self, target_stat_cap: int = DEFAULT_TARGET_STAT_CAP):
        self.target_stat_cap = target_stat_cap

    @staticmethod
    def is_meaningful_data(data: Optional[Dict[str, Any]], threshold: float = 0.15) -> bool:
        """딕셔너리 값이 실질적으로 유효한 데이터인지 검증 (0, 0.0, '', None, N/A 제외 유효 비율 체크)"""
        if not data or not isinstance(data, dict):
            return False
        values = list(data.values())
        if not values:
            return False
        meaningful_count = sum(
            1 for v in values 
            if v not in [0, 0.0, "", None, "N/A", "n/a"]
            and not (isinstance(v, str) and v.strip() in ["", "%", "0%", "0.0%"])
        )
        return (meaningful_count / len(values)) >= threshold

    @staticmethod
    def normalize_stat_keys(raw_stats: Optional[Dict[str, Any]]) -> Dict[str, int]:
        """스탯 딕셔너리의 키를 표준화하고 정수형으로 변환"""
        normalized: Dict[str, int] = {k: 0 for k in CORE_ATTRIBUTES + WEAPON_ATTRIBUTES}
        if not raw_stats or not isinstance(raw_stats, dict):
            return normalized

        for key, val in raw_stats.items():
            if val is None:
                continue
            cleaned_key = str(key).strip().lower().replace(" ", "_").replace("-", "_")
            canonical_key = STAT_ALIAS_MAP.get(cleaned_key)
            if canonical_key and isinstance(val, (int, float, str)):
                try:
                    normalized[canonical_key] = int(float(val))
                except (ValueError, TypeError):
                    pass
        return normalized

    @staticmethod
    def normalize_attunements(raw_attunements: Optional[Dict[str, Any]]) -> Dict[str, int]:
        """어튠먼트(속성) 딕셔너리의 키를 표준화하고 정수형으로 변환"""
        normalized: Dict[str, int] = {k: 0 for k in ATTUNEMENT_KEYS}
        if not raw_attunements or not isinstance(raw_attunements, dict):
            return normalized

        for key, val in raw_attunements.items():
            if val is None:
                continue
            cleaned_key = str(key).strip().lower().replace(" ", "_").replace("-", "_")
            canonical_key = ATTUNEMENT_ALIAS_MAP.get(cleaned_key)
            if canonical_key and isinstance(val, (int, float, str)):
                try:
                    normalized[canonical_key] = int(float(val))
                except (ValueError, TypeError):
                    pass
        return normalized

    @staticmethod
    def normalize_traits(raw_traits: Optional[Dict[str, Any]]) -> Dict[str, int]:
        """4대 고유 특성(Traits) 정규화"""
        normalized: Dict[str, int] = {k: 0 for k in TRAIT_KEYS}
        if not raw_traits or not isinstance(raw_traits, dict):
            return normalized

        for key, val in raw_traits.items():
            cleaned_key = str(key).strip().lower().replace(" ", "_")
            if cleaned_key in TRAIT_KEYS and isinstance(val, (int, float, str)):
                try:
                    normalized[cleaned_key] = int(float(val))
                except (ValueError, TypeError):
                    pass
        return normalized

    def verify_330pt_integrity(
        self,
        stats: Dict[str, int],
        attunements: Dict[str, int]
    ) -> Dict[str, Any]:
        """330 포인트 무결성 정밀 검증.
        
        Deepwoken Power 20 기준 총 스탯 투자 포인트는 330pt입니다.
        (6대 기본 스탯 + 3대 무기 스탯 + 어튠먼트 스탯)
        """
        core_sum = sum(stats.get(k, 0) for k in CORE_ATTRIBUTES)
        weapon_sum = sum(stats.get(k, 0) for k in WEAPON_ATTRIBUTES)
        attunement_sum = sum(attunements.get(k, 0) for k in ATTUNEMENT_KEYS)
        total_points = core_sum + weapon_sum + attunement_sum

        difference = total_points - self.target_stat_cap
        is_exact = (total_points == self.target_stat_cap)

        if is_exact:
            status = "EXACT_330"
        elif total_points < self.target_stat_cap:
            status = "BELOW_CAP"
        else:
            status = "OVER_CAP"

        return {
            "total_points": total_points,
            "target_cap": self.target_stat_cap,
            "difference": difference,
            "is_valid_330_cap": is_exact,
            "status": status,
            "breakdown": {
                "core_attributes": core_sum,
                "weapon_attributes": weapon_sum,
                "attunements": attunement_sum,
            },
            "verified": is_exact,
        }

    def _determine_shrine_build(
        self,
        pre_stats: Optional[Dict[str, int]],
        post_stats: Optional[Dict[str, int]],
        external_progression: Optional[Dict[str, Any]] = None
    ) -> bool:
        """사원 빌드(Shrine of Order Build) 여부 판정.
        
        Pre-Shrine 스탯이 존재하고, Post-Shrine 스탯과 명확히 구분(분포 차이)되는 경우 True.
        만약 pre_stats가 비어있거나 post_stats와 완전히 동일하다면 단일 완성 빌드로 False.
        """
        pre_sum = sum(pre_stats.values()) if pre_stats else 0
        post_sum = sum(post_stats.values()) if post_stats else 0

        # Pre-Shrine 스탯이 0이면 단일 빌드
        if pre_sum <= 0:
            # 외부 진행 데이터(vlm or builder)에 명시적인 pre_shrine 스탯이 있는지 확인
            if external_progression and isinstance(external_progression, dict):
                ext_pre = external_progression.get("pre_shrine") or external_progression.get("pre_shrine_stats")
                if isinstance(ext_pre, dict) and sum([v for v in ext_pre.values() if isinstance(v, (int, float))]) > 0:
                    return True
            return False

        # Pre 스탯과 Post 스탯의 분배 비교
        if post_sum > 0 and pre_stats and post_stats:
            # 적어도 하나 이상의 스탯 항목에서 차이가 발생하는지 확인
            differences = [
                k for k in (CORE_ATTRIBUTES + WEAPON_ATTRIBUTES)
                if pre_stats.get(k, 0) != post_stats.get(k, 0)
            ]
            if len(differences) > 0:
                return True
            return False

        # pre_sum은 있지만 post_sum이 없는 경우 (드문 케이스)
        return pre_sum > 0

    def reconcile(self, raw_data: RawBuildData) -> Dict[str, Any]:
        """원시 데이터를 수집 우선순위(Vision > Builder > VLM)에 따라 병합하고 정규화합니다.
        
        Returns:
            Dict[str, Any]: structurer.py 및 downstream 모듈이 즉시 사용할 수 있는 표준화된 딕셔너리.
        """
        # 1. 원본 소스 데이터 수집
        vision_post = raw_data.post_shrine_raw or {}
        vision_pre = raw_data.pre_shrine_raw or {}
        builder = raw_data.builder_scraped or {}
        vlm = raw_data.vlm_narrative or {}

        # 2. Stats 및 Attunements 추출 (우선순위 1순위: Vision Post -> 2순위: Builder -> 3순위: VLM)
        post_stats_raw = vision_post.get("stats")
        builder_stats_raw = builder.get("stats")
        vlm_stats_raw = vlm.get("stats") or (vlm.get("stats_and_attunements", {}).get("stats") if isinstance(vlm.get("stats_and_attunements"), dict) else None)

        if post_stats_raw and isinstance(post_stats_raw, dict) and sum(float(v) for v in post_stats_raw.values() if isinstance(v, (int, float, str)) and str(v).replace('.', '', 1).isdigit()) > 0:
            final_stats_source = post_stats_raw
            stats_source_name = "vision_post_shrine"
        elif builder_stats_raw and isinstance(builder_stats_raw, dict) and sum(float(v) for v in builder_stats_raw.values() if isinstance(v, (int, float, str)) and str(v).replace('.', '', 1).isdigit()) > 0:
            final_stats_source = builder_stats_raw
            stats_source_name = "builder_scraped"
        elif vlm_stats_raw and isinstance(vlm_stats_raw, dict) and sum(float(v) for v in vlm_stats_raw.values() if isinstance(v, (int, float, str)) and str(v).replace('.', '', 1).isdigit()) > 0:
            final_stats_source = vlm_stats_raw
            stats_source_name = "vlm_narrative"
        elif vision_pre.get("stats"):
            final_stats_source = vision_pre.get("stats")
            stats_source_name = "vision_pre_shrine_fallback"
        else:
            final_stats_source = {}
            stats_source_name = "none"

        final_stats = self.normalize_stat_keys(final_stats_source)

        # Attunements 우선순위 추출
        post_att_raw = vision_post.get("attunements")
        builder_att_raw = builder.get("attunements")
        vlm_att_raw = vlm.get("attunements") or (vlm.get("stats_and_attunements", {}).get("attunements") if isinstance(vlm.get("stats_and_attunements"), dict) else None)

        if post_att_raw and isinstance(post_att_raw, dict) and self.is_meaningful_data(post_att_raw):
            final_att_source = post_att_raw
        elif builder_att_raw and isinstance(builder_att_raw, dict) and self.is_meaningful_data(builder_att_raw):
            final_att_source = builder_att_raw
        elif vlm_att_raw and isinstance(vlm_att_raw, dict) and self.is_meaningful_data(vlm_att_raw):
            final_att_source = vlm_att_raw
        elif vision_pre.get("attunements") and self.is_meaningful_data(vision_pre.get("attunements")):
            final_att_source = vision_pre.get("attunements")
        elif builder_att_raw and isinstance(builder_att_raw, dict):
            final_att_source = builder_att_raw
        else:
            final_att_source = post_att_raw or {}

        final_attunements = self.normalize_attunements(final_att_source)

        # 3. 330pt 무결성 검증 수행
        integrity_result = self.verify_330pt_integrity(final_stats, final_attunements)

        # 4. Pre-Shrine 스탯 추출 및 사원 빌드 여부 판정
        pre_stats_raw = vision_pre.get("stats") if self.is_meaningful_data(vision_pre.get("stats")) else None
        
        if not pre_stats_raw:
            # 1차 폴백: Builder의 pre_shrine 객체 직접 확인 (Nuxt 파서 반환 규격)
            b_pre = builder.get("pre_shrine")
            if isinstance(b_pre, dict):
                if "stats" in b_pre and self.is_meaningful_data(b_pre.get("stats")):
                    pre_stats_raw = b_pre["stats"]
                elif self.is_meaningful_data(b_pre):
                    pre_stats_raw = b_pre

        if not pre_stats_raw:
            # 2차 폴백: Builder 또는 VLM의 shrine progression에서 사전 스탯 확인
            ext_shrine = (
                builder.get("shrine_of_order_progression")
                or builder.get("shrine_progression")
                or vlm.get("shrine_of_order_progression")
                or vlm.get("shrine_progression")
                or {}
            )
            if isinstance(ext_shrine, dict):
                pre_stats_raw = ext_shrine.get("pre_shrine") or ext_shrine.get("pre_shrine_stats")

        normalized_pre_stats = self.normalize_stat_keys(pre_stats_raw) if pre_stats_raw else None

        # Pre-Shrine attunements (존재하는 경우)
        pre_att_raw = vision_pre.get("attunements") if self.is_meaningful_data(vision_pre.get("attunements")) else None
        if not pre_att_raw:
            b_pre = builder.get("pre_shrine")
            if isinstance(b_pre, dict) and "attunements" in b_pre and self.is_meaningful_data(b_pre.get("attunements")):
                pre_att_raw = b_pre["attunements"]

        normalized_pre_att = self.normalize_attunements(pre_att_raw) if pre_att_raw else None

        # shrine_progression 힌트 수집
        external_sop = (
            vlm.get("shrine_progression")
            or vlm.get("shrine_of_order_progression")
            or builder.get("shrine_progression")
            or builder.get("shrine_of_order_progression")
            or {}
        )

        is_shrine = self._determine_shrine_build(
            pre_stats=normalized_pre_stats,
            post_stats=final_stats,
            external_progression=external_sop
        )

        # 5. Shrine Progression 블록 구조화
        pre_talents = []
        post_priorities = []
        if isinstance(external_sop, dict):
            pre_talents = external_sop.get("pre_shrine_talents") or []
            post_priorities = external_sop.get("post_shrine_priority") or external_sop.get("post_shrine_priorities") or []

        shrine_progression: Dict[str, Any] = {
            "is_shrine_build": is_shrine,
        }
        shrine_of_order_path = ""

        if is_shrine:
            # pre_shrine 스탯이 0이 아닌 항목만 필터링한 맵도 제공
            active_pre = {k: v for k, v in (normalized_pre_stats or {}).items() if v > 0}
            if normalized_pre_att:
                for k, v in normalized_pre_att.items():
                    if v > 0:
                        active_pre[k] = v

            shrine_progression["pre_shrine"] = normalized_pre_stats or {}
            shrine_progression["pre_shrine_attunements"] = normalized_pre_att or {}
            shrine_progression["pre_shrine_talents"] = pre_talents
            shrine_progression["post_shrine_priorities"] = post_priorities
            shrine_progression["post_shrine_priority"] = post_priorities

            pre_summary = ", ".join(f"{k.capitalize()} {v}" for k, v in active_pre.items())
            prio_summary = "\n".join(f"- {p}" for p in post_priorities) if post_priorities else "- 스탯 최적화 완료"
            shrine_of_order_path = f"**Pre-Shrine**: `{pre_summary}`\n**Post-Shrine 우선순위**:\n{prio_summary}"
        else:
            shrine_progression["pre_shrine"] = {}
            shrine_progression["pre_shrine_attunements"] = {}
            shrine_progression["pre_shrine_talents"] = []
            shrine_progression["post_shrine_priorities"] = []

        # 6. 캐릭터 기본 메타 추출 (Power, Race, Origin, Oath, Murmur, Resonance)
        # 1순위 Vision Post -> Vision Pre -> Builder -> VLM
        def pick_meta(field_key: str, default: Any = "N/A") -> Any:
            for src in [vision_post, vision_pre, builder, vlm]:
                if isinstance(src, dict) and src.get(field_key) not in [None, "", "N/A"]:
                    return src[field_key]
                # vlm의 character_details / character_setup 확인
                for sub in ["character_details", "character_setup"]:
                    if isinstance(src.get(sub), dict) and src[sub].get(field_key) not in [None, "", "N/A"]:
                        return src[sub][field_key]
            return default

        char_name = pick_meta("character_name", None)
        power_val = pick_meta("power", 20)
        try:
            power = int(power_val)
        except (ValueError, TypeError):
            power = 20

        race = str(pick_meta("race", "N/A"))
        origin = str(pick_meta("origin", "N/A"))
        oath = str(pick_meta("oath", "Oathless"))
        murmur = str(pick_meta("murmur", "N/A"))
        resonance = str(pick_meta("resonance", pick_meta("resonance_bell", "N/A")))

        # 7. Traits, Combat Stats, Resistances (1순위: Vision Post -> 2순위: Pre -> 3순위: Builder -> 4순위: VLM)
        def pick_dict_source(field_name: str) -> Dict[str, Any]:
            for src in [vision_post, vision_pre, builder, vlm]:
                if isinstance(src, dict) and isinstance(src.get(field_name), dict):
                    candidate = src[field_name]
                    if self.is_meaningful_data(candidate, threshold=0.1):
                        return dict(candidate)
            return {}

        traits = self.normalize_traits(pick_dict_source("traits"))
        combat_stats = pick_dict_source("combat_stats")
        resistances = pick_dict_source("resistances")

        # 8. Talents & Mantras 수집 (Builder > VLM > Vision)
        talents = builder.get("talents") or vlm.get("talents") or (vlm.get("talents_and_mantras", {}).get("talents") if isinstance(vlm.get("talents_and_mantras"), dict) else [])
        if isinstance(talents, list):
            formatted_talents = []
            for t in talents:
                if isinstance(t, str):
                    formatted_talents.append({"name": t, "is_core": False})
                elif isinstance(t, dict) and "name" in t:
                    formatted_talents.append(t)
            talents = formatted_talents
        else:
            talents = []

        mantras = builder.get("mantras") or vlm.get("mantras") or (vlm.get("talents_and_mantras", {}).get("mantras") if isinstance(vlm.get("talents_and_mantras"), dict) else [])
        if isinstance(mantras, list):
            formatted_mantras = []
            for m in mantras:
                if isinstance(m, str):
                    formatted_mantras.append({"name": m})
                elif isinstance(m, dict) and "name" in m:
                    formatted_mantras.append(m)
            mantras = formatted_mantras
        else:
            mantras = []

        # 9. Weapons & Equipment
        weapons = builder.get("weapons") or vision_post.get("weapons") or vlm.get("weapons") or []
        equipment = builder.get("equipment") or vision_post.get("equipment") or vlm.get("equipment") or []

        # 10. Build Summary & Combo Guide
        vlm_bs = vlm.get("build_summary") or {}
        builder_bs = builder.get("build_summary") or {}
        default_title = raw_data.video_meta.get("title") or "Deepwoken Build"

        build_summary = {
            "build_name": vlm_bs.get("build_name") or builder_bs.get("build_name") or default_title,
            "build_type": vlm_bs.get("build_type") or builder_bs.get("build_type") or "PvE",
            "difficulty": vlm_bs.get("difficulty") or builder_bs.get("difficulty") or "Intermediate",
            "creator_opinion": vlm_bs.get("creator_opinion") or builder_bs.get("creator_opinion") or "No description provided.",
            "strengths": vlm_bs.get("strengths") or builder_bs.get("strengths") or [],
            "weaknesses": vlm_bs.get("weaknesses") or builder_bs.get("weaknesses") or [],
        }

        combo_guide = vlm.get("combo_guide") or builder.get("combo_guide") or ""

        # 11. 최종 통합 딕셔너리 생성
        reconciled: Dict[str, Any] = {
            "video_id": raw_data.video_id,
            "video_meta": raw_data.video_meta,
            "build_summary": build_summary,
            "character_name": char_name,
            "power": power,
            "race": race,
            "origin": origin,
            "oath": oath,
            "murmur": murmur,
            "resonance": resonance,
            "traits": traits,
            "stats": final_stats,
            "attunements": final_attunements,
            "combat_stats": combat_stats,
            "resistances": resistances,
            "weapons": weapons,
            "equipment": equipment,
            "talents": talents,
            "mantras": mantras,
            "combo_guide": combo_guide,
            "is_shrine_build": is_shrine,
            "shrine_progression": shrine_progression,
            "shrine_of_order_progression": shrine_progression,
            "shrine_of_order_path": shrine_of_order_path,
            "_stat_validation": integrity_result,
            "_stats_source": stats_source_name,
            "_raw_source_data": raw_data.to_dict(),  # 원본 데이터 100% 무손실 보존
        }

        # target_mobs_and_strategy 가 있는 경우 복사
        if "target_mobs_and_strategy" in vlm:
            reconciled["target_mobs_and_strategy"] = vlm["target_mobs_and_strategy"]

        return reconciled
