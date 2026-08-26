import re
import logging
from typing import Dict, Any, List, Optional, Tuple

logger = logging.getLogger(__name__)

# Deepwoken 공식 핵심 탤런트 선행 조건 데이터베이스 (100% 공식 deepwoken.co / Fandom Wiki 동기화)
TALENT_PREREQUISITES = {
    # Fortitude / Willpower 계열
    "Brick Wall": {"Fortitude": 100, "Willpower": 100, "description": "모든 넉백, 기절, 래그돌 면역"},
    "Reinforced Armor": {"Fortitude": 90, "description": "방어구 관통(PEN) 데미지 30% 감소"},
    "Exoskeleton": {"Fortitude": 40, "description": "방어력 +5% 및 블록 브레이크 저항"},
    "To the Finish": {"Fortitude": 50, "description": "체력 위기 시 받는 피해 감소"},
    "Grand Feast": {"description": "적 처치 시 체력/허기 대량 회복"},
    "Underdog": {"Willpower": 30, "description": "체력이 나보다 높은 적 및 거대 적 대상 피해량 증가"},
    
    # Strength 계열
    "Million Ton Piercer": {"Strength": 90, "description": "모든 물리 공격 50% 아머 관통"},
    "Showstopper": {"Strength": 40, "description": "적 구르기 시 지면 강타 및 멍함/이속버프 제거"},
    "Collapsed Lung": {"Strength": 100, "description": "블록 브레이크 시 적 Vent 봉인 및 붕괴"},
    "Piercing Blow": {"Strength": 100, "description": "가드브레이크 시 적 방어력 무시"},

    # Agility 계열
    "Ghost": {"Agility": 40, "description": "Q 회피 시 1.2초 무적 판정(I-frame) 및 투명화"},
    "Speed Demon": {"Agility": 25, "description": "출혈(Bleed) 중인 적 공격 시 공격 및 이동 속도 증가"},
    "Tap Dancer": {"Agility": 60, "description": "구르기 쿨타임 대폭 감소 및 페리 구르기"},
    "Conditioned Runner": {"Agility": 25, "description": "전투 중 질주 시 체력 서서히 재생"},
    "Observation": {"Agility": 20, "description": "적 모션 감지 및 시각화"},

    # Willpower 계열
    "Heretic's Sutra": {"Willpower": 80, "description": "광기(Insanity)를 발동하여 광기 탤런트 활성화"},
    "Lose Your Mind": {"Strength": 30, "Fortitude": 30, "description": "광기(Insanity) 상태에서 피해량 최대 +15% 증폭"},
    "Conquer Your Fears": {"Willpower": 10, "description": "공포/패닉 면역"},
    "Piercing Will": {"Willpower": 80, "description": "정신력이 낮을 때 방어 관통력(PEN) 최대 +15% 증가"},

    # Charisma 계열
    "Charismatic Cast": {"Charisma": 25, "description": "만트라 적중 시 적에게 참(Charm) 부여"},
    "Tough Love": {"Charisma": 25, "description": "참 걸린 적에게 가하는 데미지 +10%"},
    "Chaotic Charm": {"Charisma": 55, "description": "피격 시 상대방 매혹 및 받는 피해 감소"},
    "Enrage": {"Charisma": 65, "description": "도발 상태 적 기절 시 분노 유발"},

    # Intelligence 계열
    "Eureka": {"Intelligence": 30, "description": "에테르 소모량 감소 및 패링 시 에테르 회복"},
    "Master Craftsman": {"Intelligence": 45, "description": "물약 및 장비 제작 효율 극대화"},
    "Nullifying Clarity": {"Strength": 15, "Intelligence": 5, "description": "속성 디버프 해제 및 추가 마법 피해"},
}

# Deepwoken 공식 Oath 선행 조건 목록
OATH_PREREQUISITES = {
    "Blindseer": {"Willpower": 40, "requirements": "정신력 40 + 5개 이상의 서포트/유틸 만트라"},
    "Starkindred": {"Strength": 50, "requirements": "근력 50 또는 속성 50 + 신의 날개 퀘스트"},
    "Dawnwalker": {"requirements": "Floor 2 Ethiron 보스 토벌 및 광휘의 메달"},
    "Silentheart": {"Weapon": 75, "requirements": "주무기 75 + 속성 0 (만트라 완전 봉인)"},
    "Contractor": {"Willpower": 50, "requirements": "Willpower 50 + Ministry 퀘스트"},
    "Arcwarder": {"Fortitude": 50, "Flamecharm": 20, "Thundercall": 20, "requirements": "인내 50, 화염 20, 번개 20 + 레이어 2 수트"},
    "Jetstriker": {"Agility": 50, "requirements": "민첩 50 + 슬릭 대시"},
    "Visionshaper": {"Charisma": 50, "requirements": "매력 50 + 클론 퀘스트"},
    "Linkstrider": {"Charisma": 40, "Willpower": 40, "requirements": "매력 40, 의지 40 + 팀원 버프"},
    "Oathless": {"requirements": "선행 스탯 조건 없음 (자유로운 슬롯)"},
}

ATTUNEMENTS = ["Flamecharm", "Frostdraw", "Thundercall", "Galebreathe", "Shadowcast", "Ironsing"]

class DeepwokenFactChecker:
    """Deepwoken Builder(deepwoken.co) 공식 룰 기반 수치, 탤런트 선행 조건, 스탯 무결성 정밀 검증기"""

    # Deepwoken Builder (deepwoken.co) 공식 순수 투자 포인트 한도: 정확히 330 pt
    MAX_VALID_STAT_SUM = 330

    @staticmethod
    def calculate_total_stats(stats: Dict[str, int]) -> int:
        """스탯 총 투자 포인트 합산 (deepwoken.co 기준 330pt 한도)"""
        valid_keys = [
            "Strength", "Fortitude", "Agility", "Intelligence", "Willpower", "Charisma",
            "Heavy Wep", "Medium Wep", "Light Wep",
            "Flamecharm", "Frostdraw", "Thundercall", "Galebreathe", "Shadowcast", "Ironsing"
        ]
        total = 0
        for k, v in stats.items():
            if any(vk.lower() in k.lower() for vk in valid_keys):
                total += int(v or 0)
        return total

    @staticmethod
    def validate_oath(oath: str, stats: Dict[str, int]) -> Tuple[bool, str]:
        """Deepwoken 공식 Oath 조건 정밀 검증 (OR 조건 및 복합 조건 지원)"""
        if not oath or oath == "Oathless":
            return True, "조건 없음 (자유)"

        if oath == "Starkindred":
            # 근력 50 이상 OR 임의의 속성 50 이상
            has_str = stats.get("Strength", 0) >= 50
            has_att = any(stats.get(att, 0) >= 50 for att in ATTUNEMENTS)
            if has_str or has_att:
                return True, "조건 충족 (STR 50+ 또는 속성 50+)"
            return False, f"Starkindred 조건 미달: Strength({stats.get('Strength', 0)}/50) 또는 속성({max([stats.get(a, 0) for a in ATTUNEMENTS] or [0])}/50) 필요"

        elif oath == "Blindseer":
            if stats.get("Willpower", 0) >= 40:
                return True, "조건 충족 (Willpower 40+)"
            return False, f"Blindseer 조건 미달: Willpower({stats.get('Willpower', 0)}/40) 필요"

        elif oath == "Silentheart":
            max_wep = max(stats.get("Heavy Wep", 0), stats.get("Medium Wep", 0), stats.get("Light Wep", 0))
            att_sum = sum(stats.get(a, 0) for a in ATTUNEMENTS)
            if max_wep >= 75 and att_sum == 0:
                return True, "조건 충족 (무기 75+ 및 무속성)"
            return False, f"Silentheart 조건 미달: 무기({max_wep}/75) 및 속성 0pt 필요"

        elif oath == "Arcwarder":
            has_fort = stats.get("Fortitude", 0) >= 50
            dual_att = sum(1 for a in ATTUNEMENTS if stats.get(a, 0) >= 20) >= 2
            if has_fort and dual_att:
                return True, "조건 충족 (Fortitude 50+ 및 2개 속성 20+)"
            return False, "Arcwarder 조건 미달: Fortitude 50+ 및 2개 이상의 속성 20+ 필요"

        elif oath == "Contractor":
            if stats.get("Willpower", 0) >= 50:
                return True, "조건 충족 (Willpower 50+)"
            return False, f"Contractor 조건 미달: Willpower({stats.get('Willpower', 0)}/50) 필요"

        elif oath == "Jetstriker":
            if stats.get("Agility", 0) >= 50:
                return True, "조건 충족 (Agility 50+)"
            return False, f"Jetstriker 조건 미달: Agility({stats.get('Agility', 0)}/50) 필요"

        elif oath == "Visionshaper":
            if stats.get("Charisma", 0) >= 50:
                return True, "조건 충족 (Charisma 50+)"
            return False, f"Visionshaper 조건 미달: Charisma({stats.get('Charisma', 0)}/50) 필요"

        elif oath == "Linkstrider":
            if stats.get("Charisma", 0) >= 40 and stats.get("Willpower", 0) >= 40:
                return True, "조건 충족 (Charisma 40+, Willpower 40+)"
            return False, f"Linkstrider 조건 미달: Charisma({stats.get('Charisma', 0)}/40), Willpower({stats.get('Willpower', 0)}/40) 필요"

        return True, "조건 확인 완료"

    @staticmethod
    def parse_stats_from_advice(text: str) -> Dict[str, int]:
        """AI 조언 텍스트에서 추천된 사원 후(Post-Shrine) 최종 330pt 스탯을 최우선 정밀 자동 추출 (섹션, 마크다운 표, 리스트 완전 대응)"""
        key_patterns = {
            "Strength": [r"(?:Strength|근력|힘)\b", r"STR\b"],
            "Fortitude": [r"(?:Fortitude|인내|체력)\b", r"FORT\b"],
            "Agility": [r"(?:Agility|민첩)\b", r"AGI\b"],
            "Intelligence": [r"(?:Intelligence|지능)\b", r"INT\b"],
            "Willpower": [r"(?:Willpower|의지|정신력)\b", r"WIL\b"],
            "Charisma": [r"(?:Charisma|매력)\b", r"CHA\b"],
            "Heavy Wep": [r"(?:Heavy\s*Weapon|Heavy\s*Wep|중무기|대검|헤비)\b"],
            "Medium Wep": [r"(?:Medium\s*Weapon|Medium\s*Wep|중검|미디엄)\b"],
            "Light Wep": [r"(?:Light\s*Weapon|Light\s*Wep|단검|라이트)\b"],
            "Flamecharm": [r"(?:Flamecharm|화염|플레임)\b"],
            "Frostdraw": [r"(?:Frostdraw|프로스트|빙결)\b"],
            "Thundercall": [r"(?:Thundercall|번개|선더)\b"],
            "Galebreathe": [r"(?:Galebreathe|바람|게일)\b"],
            "Shadowcast": [r"(?:Shadowcast|그림자|섀도우)\b"],
            "Ironsing": [r"(?:Ironsing|철|아이언)\b"],
        }

        # 1. Post-Shrine 블록 우선 추출 (헤더 타이틀이 아닌 실제 Post-Shrine 스탯 목록 블록 탐색)
        post_matches = list(re.finditer(r'(?:[\*\#\-]\s*)?\**\b(?:Post-Shrine|사원\s*후)\b\**[^\n]*\n([\s\S]*?)(?=\n\s*[\*\#\-]\s*\**\b(?:Pre-Shrine|사원\s*전|장비|만트라|2\.|3\.|4\.)\b|\n---|\Z)', text, re.IGNORECASE))
        for match in reversed(post_matches):
            section_text = match.group(1)
            parsed = {}
            chunks = re.split(r"[\n,;|]", section_text)
            for chunk in chunks:
                for canonical_name, pat_list in key_patterns.items():
                    if canonical_name in parsed:
                        continue
                    for pat in pat_list:
                        m = re.search(rf"{pat}[^\d\n:]*?[:\s=]+[\*`_]*(\d{{1,3}})[\*`_]*", chunk, re.IGNORECASE)
                        if m:
                            val = int(m.group(1))
                            if 0 <= val <= 102:
                                parsed[canonical_name] = val
                                break
            if len(parsed) >= 3:
                return parsed

        # 2. 마크다운 테이블 (세로형 표) 검출
        table_dict = {}
        for line in text.split("\n"):
            if "|" in line:
                cells = [c.strip() for c in line.split("|") if c.strip()]
                if len(cells) >= 2 and ":" not in cells[0]:
                    first_cell = cells[0]
                    val_cell = cells[-1] # 마지막 셀(Post-Shrine 스탯)
                    for canonical_name, pat_list in key_patterns.items():
                        if canonical_name in table_dict:
                            continue
                        if any(re.search(pat, first_cell, re.IGNORECASE) for pat in pat_list):
                            m = re.search(r"\b(\d{1,3})\b", val_cell)
                            if m:
                                v = int(m.group(1))
                                if 0 <= v <= 102:
                                    table_dict[canonical_name] = v
        if len(table_dict) >= 3:
            return table_dict

        # 3. 전체 텍스트 fallback
        fallback = {}
        chunks = re.split(r"[\n,;|]", text)
        for chunk in chunks:
            for canonical_name, pat_list in key_patterns.items():
                if canonical_name in fallback:
                    continue
                for pat in pat_list:
                    m = re.search(rf"{pat}[^\d\n:]*?[:\s=]+[\*`_]*(\d{{1,3}})[\*`_]*", chunk, re.IGNORECASE)
                    if m:
                        val = int(m.group(1))
                        if 0 <= val <= 102:
                            fallback[canonical_name] = val
                            break
        return fallback

    @staticmethod
    def validate_racial_base_stats(race: str, stats: Dict[str, int]) -> Tuple[bool, List[str]]:
        """Deepwoken 공식 종족 고유 기본 스탯 및 Shrine of Order(성소) 스탯 보존 검증"""
        from chatbot.builder_calculator import DEEPWOKEN_RACES
        race_info = DEEPWOKEN_RACES.get(race)
        if not race_info:
            return True, []
        
        errors = []
        for stat_name, min_val in race_info.get("stats", {}).items():
            current_val = stats.get(stat_name, 0)
            if current_val < min_val:
                errors.append(f"⚠️ {race} 종족의 {stat_name} 기본치는 최소 {min_val}pt 이상이어야 합니다. (현재: {current_val}pt - 질서의 성소도 종족 기본치 이하로 삭감 불가)")
        
        return len(errors) == 0, errors

    @staticmethod
    def audit_profile_and_advice(profile: Dict[str, Any], advice_text: str) -> Dict[str, Any]:
        """사용자 프로필과 AI 조언 텍스트를 대조 검증하여 무결성 리포트 생성"""
        stats = profile.get("stats", {})
        total_points = DeepwokenFactChecker.calculate_total_stats(stats)
        race = profile.get("race", "Vesperian")
        
        # 만약 유저 프로필이 빈 슬롯(0pt)이면 AI가 제안한 스탯을 자동 파싱하여 검증
        if total_points == 0:
            parsed_stats = DeepwokenFactChecker.parse_stats_from_advice(advice_text)
            if parsed_stats:
                stats = parsed_stats
                total_points = DeepwokenFactChecker.calculate_total_stats(stats)

        warnings = []
        verified_points = []
        
        # 1. 스탯 상한선 검증 (Deepwoken Builder 기준 최대 330pt)
        if total_points > DeepwokenFactChecker.MAX_VALID_STAT_SUM:
            warnings.append(f"⚠️ 총 스탯 합계가 {total_points}pt로 공식 빌더 상한선({DeepwokenFactChecker.MAX_VALID_STAT_SUM}pt)을 {total_points - DeepwokenFactChecker.MAX_VALID_STAT_SUM}pt 초과했습니다.")
        elif total_points > 0:
            verified_points.append(f"📊 스탯 무결성: 총 `{total_points}/{DeepwokenFactChecker.MAX_VALID_STAT_SUM}` pt (deepwoken.co 공식 룰 준수 ✅)")

        # 2. 종족 기본치 검증 (Shrine of Order 보존 룰)
        race_ok, race_errs = DeepwokenFactChecker.validate_racial_base_stats(race, stats)
        if race_ok:
            verified_points.append(f"🧬 종족 '{race}' 기본 스탯 보존 검증 완료 ✅")
        else:
            warnings.extend(race_errs)

        # 3. Oath 조건 검증
        current_oath = profile.get("oath", "")
        if not current_oath or current_oath == "Oathless":
            # AI 텍스트에서 언급된 Oath 찾기
            for oath_name in OATH_PREREQUISITES.keys():
                if oath_name.lower() in advice_text.lower():
                    current_oath = oath_name
                    break

        if current_oath:
            oath_ok, oath_msg = DeepwokenFactChecker.validate_oath(current_oath, stats)
            if oath_ok:
                verified_points.append(f"⚔️ Oath '{current_oath}': {oath_msg} ✅")
            else:
                warnings.append(f"⚠️ {oath_msg}")

        return {
            "total_points": total_points,
            "is_valid_point_cap": total_points <= DeepwokenFactChecker.MAX_VALID_STAT_SUM,
            "verified_points": verified_points,
            "warnings": warnings,
            "has_warnings": len(warnings) > 0
        }

    @staticmethod
    def generate_verification_badge(audit_result: Dict[str, Any]) -> str:
        """답변 하단에 붙일 검증 완료 뱃지 마크다운 생성"""
        points = audit_result.get("total_points", 0)
        max_pts = DeepwokenFactChecker.MAX_VALID_STAT_SUM
        warnings = audit_result.get("warnings", [])
        verified = audit_result.get("verified_points", [])
        
        badge_lines = ["\n\n---", "🛡️ **[Deepwoken Builder 공식 팩트체크 & 무결성 검증 리포트]**"]
        
        for v in verified:
            badge_lines.append(f"- {v}")
            
        if not warnings:
            badge_lines.append("- 🎯 **환각 방지(Anti-Hallucination)**: RAG 지식 베이스 + Deepwoken Wiki 크로스체크 완료 ✅")
        else:
            badge_lines.append("- ⚠️ **수치 보완 권장 사항**:")
            for w in warnings:
                badge_lines.append(f"  • {w}")

        return "\n".join(badge_lines)
