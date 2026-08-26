import re
from typing import Dict, Tuple, List

# Deepwoken 한국어 은어, 음성 오타, 커뮤니티 용어 사전
DEEPWOKEN_SLANG_MAP = {
    # Oath (서약) 계열
    r"(살로트\s*하트|사일런\s*하트|사일하트|사하|살하)": "사일런트하트(Silentheart: 만트라 완전 봉인, 순수 물리 M1 평타 극딜)",
    r"(블라인드\s*시어|블시|블라인드시어)": "블라인드시어(Blindseer: 정신력 40+, 시야 빔 및 광역 서포트)",
    r"(스타\s*킨드레드|스타킨|스타킨드)": "스타킨드레드(Starkindred: 신의 날개, 천공 강타)",
    r"(던\s*워커|던워커|돈워커)": "던워커(Dawnwalker: 레이어 2 보스 에시론 토벌 광휘 서약)",
    r"(아크\s*와더|아크워더|아크와더)": "아크와더(Arcwarder: 인내 50+ 듀얼속성 레이어2 수트)",
    r"(제트\s*스트라이커|젯스|젯스트라이커)": "제트스트라이커(Jetstriker: 민첩 50+ 최고속 기동성)",
    r"(비전\s*셰이퍼|비전쉐이퍼|비전)": "비전셰이퍼(Visionshaper: 매력 50+ 환영 분신)",
    r"(링크\s*스트라이더|링크)": "링크스트라이더(Linkstrider: 아군 연결 및 영혼 흡수)",
    r"(컨트랙터|컨트)": "컨트랙터(Contractor: 의지 50+ 사슬 구속)",
    r"(오슬리스|무서약)": "오슬리스(Oathless: 자유 슬롯, 2개 추가 와일드카드 만트라)",

    # 특수 스킬 / 메커니즘
    r"(줄\s*터지는\s*거|선\s*터지는\s*거|사슬\s*터지는\s*거|줄터짐)": "Mani Katti (사일런트하트 전방 사슬 다단베기 폭딜) 및 Enrapture (사슬 결박 폭발)",
    r"(하얀\s*인텐트|하얀색\s*인텐트|하얀\s*무기\s*인텐트|흰색\s*인텐트)": "Heavy Intent (무기 흰색 아우라 및 자세 파괴력 극대화) / Petra's Anchor (하얀 닻 평타 폭딜) / Blind Aura",
    r"(피흡\s*빌드|뱀파|뱀파이어)": "Vampirism Enchant + Pale Briar + Grand Feast 피흡 메커니즘",
    r"(벽돌\s*벽|브릭월|벽돌)": "Brick Wall (인내 100 + 의지 100: 모든 넉백/기절/래그돌 완전 면역)",
    r"(강화\s*아머|리인포스드|단단한\s*아머)": "Reinforced Armor (인내 90: 관통 데미지 50% 삭감, 체력 450+ 필수)",
    r"(신전|오더\s*신전|샤인\s*오브\s*오더|샤인)": "Shrine of Order (스탯 재분배 신전: 탤런트 선행 스탯 획득 후 주스탯으로 최적화)",
}

class DeepwokenSlangResolver:
    """사용자의 은어, 음성 인식 오타, 커뮤니티 약어를 공식 Deepwoken 메커니즘으로 실시간 자동 변환"""

    @staticmethod
    def resolve_slang(text: str) -> Tuple[str, List[str]]:
        resolved_text = text
        detected_terms = []

        for pattern, replacement in DEEPWOKEN_SLANG_MAP.items():
            if re.search(pattern, resolved_text, re.IGNORECASE):
                detected_terms.append(replacement)
                resolved_text = re.sub(pattern, f"[{replacement}]", resolved_text, flags=re.IGNORECASE)

        return resolved_text, detected_terms

    @staticmethod
    def enrich_prompt_with_deep_knowledge(user_query: str) -> str:
        """사용자 질문에 내포된 딥위큰 시스템 메커니즘을 상세 주석으로 프롬프트에 보강"""
        resolved, detected = DeepwokenSlangResolver.resolve_slang(user_query)
        
        enrichment = []
        if any("사일런트하트" in d or "Silentheart" in d for d in detected):
            enrichment.append(
                "⚠️ [시스템 강제 팩트체크: Silentheart 룰]\n"
                "- Silentheart는 모든 마법 속성(Frostdraw, Flamecharm 등) 투자가 0pt이어야 합니다.\n"
                "- 만트라를 사용하지 않으며, 전용 액티브 스킬(Mani Katti, Dread Breath, Ankle Cutter, Enrapture)을 사용합니다.\n"
                "- 주무기(Heavy Wep 등) 75+ 투자가 필수이며 평타(M1)와 크리티컬이 주력 딜링입니다."
            )
        if any("Brick Wall" in d for d in detected):
            enrichment.append(
                "⚠️ [시스템 강제 팩트체크: Brick Wall 룰]\n"
                "- Pre-Shrine에서 Fortitude 100, Willpower 100을 찍어 탤런트를 획득한 후 Shrine of Order를 진행해야 합니다."
            )
        if any("Reinforced Armor" in d for d in detected):
            enrichment.append(
                "⚠️ [시스템 강제 팩트체크: Reinforced Armor 룰]\n"
                "- Fortitude 90, Willpower 30 선행 조건을 만족해야 체력 450+ 단단한 세팅이 완성됩니다."
            )

        if enrichment:
            return f"{resolved}\n\n" + "\n".join(enrichment)
        return resolved
