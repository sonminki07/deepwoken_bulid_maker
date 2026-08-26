from typing import Dict, Any

# Deepwoken 핵심 탤런트 백과사전 (마우스 호버 시 툴팁 표시용)
DEEPWOKEN_TALENTS_DB: Dict[str, Dict[str, Any]] = {
    "Reinforced Armor": {
        "name_ko": "강화 갑옷 (Reinforced Armor)",
        "req": "Fortitude 90, Willpower 30",
        "category": "방어/탱킹",
        "desc": "상대방의 물리 방어 관통력(Penetration)을 완전히 무효화하고 기본 방어력을 +10% 추가 증폭합니다. 체력 450+ 및 방어력 세팅의 최고 핵심 탤런트입니다."
    },
    "Brick Wall": {
        "name_ko": "브릭 월 (Brick Wall)",
        "req": "Fortitude 100, Willpower 100",
        "category": "방어/면역",
        "desc": "모든 스턴(Stun), 래그돌(Ragdoll), 넉다운, 가드브레이크 경직에 완전 면역이 됩니다. PvE 보스의 어떤 지진/강공격 패턴에도 절대 쓰러지지 않습니다."
    },
    "Exoskeleton": {
        "name_ko": "외골격 (Exoskeleton)",
        "req": "Fortitude 40",
        "category": "방어/체력",
        "desc": "최대 체력 +5 및 기본 물리 저항력 +5%를 상시 제공하는 모든 딥위큰 빌드의 국민 필수 탤런트입니다."
    },
    "To the Finish": {
        "name_ko": "끝까지 (To the Finish)",
        "req": "Fortitude 40",
        "category": "방어/역전",
        "desc": "체력이 50% 이하로 떨어지면 받는 피해량이 대폭 감소하고 이동 속도와 공격력이 상승합니다."
    },
    "Collapsed Lung": {
        "name_ko": "폐 파열 (Collapsed Lung)",
        "req": "Strength 80",
        "category": "공격/디버프",
        "desc": "강공격이나 스킬 적중 시 상대의 폐를 붕괴시켜 스태미나 회복을 차단하고 지속 출혈 피해를 입힙니다."
    },
    "Showstopper": {
        "name_ko": "쇼스토퍼 (Showstopper)",
        "req": "Strength 40",
        "category": "공격/경직",
        "desc": "치명타 공격 시 적의 자세(Posture)를 단숨에 무너뜨리고 긴 경직을 주어 확정 후속타를 꽂아 넣습니다."
    },
    "Ghost": {
        "name_ko": "유령 (Ghost)",
        "req": "Agility 40",
        "category": "기동/회피",
        "desc": "Q(회피) 구르기 모션이 유령 대시로 강화되어 긴 무적 시간(Agility 40 기준 1.2초 i-frame)과 일시적 투명화를 제공합니다. 보스의 다단히트 광역기를 안전하게 뚫고 지나가는 핵심 회피기입니다."
    },
    "Speed Demon": {
        "name_ko": "스피드 데몬 (Speed Demon)",
        "req": "Agility 25",
        "category": "기동/공속",
        "desc": "적에게 출혈(Bleed)을 입히면 이동 속도와 공격 속도가 증가합니다."
    },
    "Conditioned Runner": {
        "name_ko": "단련된 러너 (Conditioned Runner)",
        "req": "Agility 25",
        "category": "기동/생존",
        "desc": "전투 중 질주(Sprint) 시 지속적으로 체력이 회복되며 스태미나 소모량이 30% 감소합니다."
    },
    "Giant Slayer": {
        "name_ko": "거인 학살자 (Giant Slayer)",
        "req": "Willpower 50",
        "category": "PvE/보스전",
        "desc": "나보다 체력이 높은 거대 몬스터나 보스(Duke, Primadon, Chaser)에게 주는 피해량이 +15% 증가합니다."
    },
    "Underdog": {
        "name_ko": "언더독 (Underdog)",
        "req": "Fortitude 30",
        "category": "공격/버프",
        "desc": "최대 체력이 나보다 높은 적이나 보스를 공격할 때 가하는 피해량이 +10% 증가합니다."
    },
    "Tough Love": {
        "name_ko": "거친 사랑 (Tough Love)",
        "req": "Charisma 25",
        "category": "공격/대미지",
        "desc": "매혹(Charm) 상태에 걸린 상대에게 주는 모든 대미지가 +10% 추가로 증가합니다."
    },
    "Charismatic Cast": {
        "name_ko": "매혹의 시전 (Charismatic Cast)",
        "req": "Charisma 25",
        "category": "유틸/디버프",
        "desc": "만트라나 스킬을 적중시킬 때마다 상대방에게 자동으로 Charm(매혹) 디버프를 걸어 공격력을 약화시킵니다."
    },
    "Chaotic Charm (D3)": {
        "name_ko": "혼돈의 매혹 (Chaotic Charm)",
        "req": "Charisma 55",
        "category": "방어/디버프",
        "desc": "자신을 타격한 상대방이 일정 확률로 혼란 및 매혹에 걸려 받는 피해가 20% 감소합니다."
    },
    "Nullifying Clarity": {
        "name_ko": "무효화의 명료함 (Nullifying Clarity)",
        "req": "Intelligence 25",
        "category": "공격/마법",
        "desc": "속성 디버프가 걸린 적을 물리 평타나 다른 스킬로 타격 시 폭발적인 추가 마법 대미지를 입힙니다."
    },
    "Eureka": {
        "name_ko": "유레카 (Eureka)",
        "req": "Intelligence 30",
        "category": "자원/에테르",
        "desc": "적의 공격을 패링할 때마다 에테르가 대량으로 즉시 회복되어 스킬 난사가 가능해집니다."
    },
    "Grand Feast": {
        "name_ko": "위대한 만찬 (Grand Feast)",
        "req": "Fortitude 30, Willpower 30",
        "category": "생존/회복",
        "desc": "적을 처치하거나 몬스터를 쓰러뜨릴 때마다 체력과 에테르가 크게 차오릅니다."
    },
    "Azure Flames": {
        "name_ko": "푸른 불꽃 (Azure Flames)",
        "req": "Flamecharm 70, Willpower 40",
        "category": "속성/특수",
        "desc": "화염의 색상이 푸른빛으로 진화하며, 도트 화염 대미지가 2배 이상 강력해지고 힐링/서포트 불꽃 만트라를 사용할 수 있습니다."
    },
}

# Deepwoken 주요 만트라 및 전용 액티브 스킬 백과사전
DEEPWOKEN_MANTRAS_DB: Dict[str, Dict[str, Any]] = {
    "Mani Katti": {
        "name_ko": "마니 카티 (Mani Katti)",
        "req": "Silentheart 전용",
        "category": "액티브/극딜",
        "desc": "사일런트하트 전용 연속 참격 스킬. 전방의 적에게 순간적으로 사슬을 걸고 눈에 보이지 않는 초고속 다단베기를 난사합니다."
    },
    "Dread Breath": {
        "name_ko": "공포의 숨결 (Dread Breath)",
        "req": "Silentheart 전용",
        "category": "액티브/광역",
        "desc": "사일런트하트 전용 전방위 포효. 원뿔형 범위의 모든 적의 가드를 깨뜨리고 긴 스턴을 부여합니다."
    },
    "Ankle Cutter": {
        "name_ko": "발목 절단 (Ankle Cutter)",
        "req": "Silentheart 전용",
        "category": "액티브/다운",
        "desc": "하단을 강하게 베어 상대를 강제로 래그돌/넉다운시키고 이동 속도를 5초간 50% 둔화시킵니다."
    },
    "Enrapture": {
        "name_ko": "사슬 결박 (Enrapture)",
        "req": "Silentheart 전용",
        "category": "액티브/침묵",
        "desc": "타겟에게 사슬을 꽂아 마법 만트라 사용을 원천 차단하고 사슬 폭발 대미지를 가합니다."
    },
    "Flame Leap": {
        "name_ko": "플레임 리프 (Flame Leap)",
        "req": "Flamecharm",
        "category": "만트라/기동",
        "desc": "발밑에 불꽃을 폭발시켜 공중으로 높이 도약하며 착지 지점의 적을 불태웁니다. 콤보 시작 및 회피기로 탁월합니다."
    },
    "Rising Flame": {
        "name_ko": "라이징 플레임 (Rising Flame)",
        "req": "Flamecharm",
        "category": "만트라/에어본",
        "desc": "불기둥을 솟구치게 하여 적을 공중으로 띄워 올리며 확정 공중 콤보를 시작합니다."
    },
    "Crystal Impale": {
        "name_ko": "크리스탈 임페일 (Crystal Impale)",
        "req": "Frostdraw",
        "category": "만트라/스턴",
        "desc": "거대한 얼음 창을 소환하여 전방을 꿰뚫고 상대를 지면에 고정하여 행동 불능으로 만듭니다."
    },
    "Glacial Arc": {
        "name_ko": "글레이셜 아크 (Glacial Arc)",
        "req": "Frostdraw",
        "category": "만트라/동결",
        "desc": "초승달 모양의 냉기 파동을 발사하여 광범위 동결 디버프와 함께 방어구를 얼려 깨뜨립니다."
    },
    "Gale Lunge": {
        "name_ko": "게일 런지 (Gale Lunge)",
        "req": "Galebreathe",
        "category": "만트라/돌진",
        "desc": "바람의 칼날을 두르고 초고속으로 돌진하여 상대의 가드를 부수고 에어본 상태로 만듭니다."
    },
    "Rising Wind": {
        "name_ko": "라이징 윈드 (Rising Wind)",
        "req": "Galebreathe",
        "category": "만트라/기동",
        "desc": "회오리바람을 타고 솟아올라 공중에서 상대를 찍어 누르는 연속 에어 콤보를 발동합니다."
    },
    "Lightning Stream": {
        "name_ko": "라이트닝 스트림 (Lightning Stream)",
        "req": "Thundercall",
        "category": "만트라/원거리",
        "desc": "손끝에서 굵은 번개 광선을 지속 방출하여 원거리에서 쉴드를 깎고 감전 스턴을 겁니다."
    },
    "Grand Javelin": {
        "name_ko": "그랜드 자벨린 (Grand Javelin)",
        "req": "Thundercall",
        "category": "만트라/폭딜",
        "desc": "거대한 번개 투창을 투척하여 광역 폭발과 함께 대상에게 극심한 스태미나 번을 유발합니다."
    },
    "Sightless Beam": {
        "name_ko": "맹인의 광선 (Sightless Beam)",
        "req": "Blindseer 전용",
        "category": "Oath/빔",
        "desc": "눈에서 정신 공격 광선을 발사하여 상대방의 시야를 앗아가고 지속 관통 피해를 입힙니다."
    },
    "Tranquil Circle": {
        "name_ko": "평온의 결계 (Tranquil Circle)",
        "req": "Blindseer 전용",
        "category": "Oath/결계",
        "desc": "자신 주변에 성스러운 결계를 생성하여 아군의 정신력(Sanity)을 치유하고 받는 마법 피해를 감소시킵니다."
    }
}

# 11대 장비 슬롯 종합 데이터베이스
EQUIPMENT_SLOTS_DB = {
    "helmets": [
        {"name": "Hivelord Faceguard (최고 물리 방어)", "hp": 15, "phys_resist": 5, "desc": "체력 +15, 물리 저항 +5%"},
        {"name": "Star Hat (균형형)", "hp": 12, "phys_resist": 3, "desc": "체력 +12, 물리 저항 +3%"},
        {"name": "Prophet Cap (에테르 마법사)", "hp": 8, "ether": 15, "desc": "체력 +8, 에테르 +15"},
        {"name": "Diver Mask (심해 탐사)", "hp": 10, "dve": 5, "desc": "체력 +10, 몬스터 딜증 +5%"},
        {"name": "None (미착용)", "hp": 0, "desc": "장비 미착용"}
    ],
    "face": [
        {"name": "Aviator Glasses (원거리/명중)", "dve": 4, "desc": "몬스터 딜증 +4%"},
        {"name": "Blindfold (Blindseer 특화)", "sanity": 10, "desc": "정신력 저항 +10"},
        {"name": "Deepwoken Visor (방어형)", "hp": 5, "phys_resist": 2, "desc": "체력 +5, 물리 저항 +2%"},
        {"name": "None (미착용)", "hp": 0, "desc": "장비 미착용"}
    ],
    "amulets": [
        {"name": "Hallowed Amulet (체력/성소)", "hp": 15, "desc": "체력 +15"},
        {"name": "Star Amulet (만트라 딜)", "dve": 6, "desc": "몬스터 딜증 +6%"},
        {"name": "Deepwoken Amulet (방어력)", "hp": 10, "phys_resist": 3, "desc": "체력 +10, 물리 저항 +3%"},
        {"name": "None (미착용)", "hp": 0, "desc": "장비 미착용"}
    ],
    "boots": [
        {"name": "Star Boots (이동속도 극대화)", "hp": 10, "speed": 4, "desc": "체력 +10, 이동속도 +4%"},
        {"name": "Heavy Iron Boots (물리 방어)", "hp": 15, "phys_resist": 4, "desc": "체력 +15, 물리 저항 +4%"},
        {"name": "Runner Boots (스태미나)", "hp": 8, "speed": 5, "desc": "체력 +8, 이동속도 +5%"},
        {"name": "None (미착용)", "hp": 0, "desc": "장비 미착용"}
    ],
    "rings": [
        "Ring of Casters (에테르 재생)",
        "Starved Knight Ring (공격력 증폭)",
        "Poser's Ring (크리티컬 폭딜)",
        "Ferryman's Ring (이동속도/회피)",
        "Deepwoken Ring of Health (체력 +10)",
        "Hivelord Ring (자세 대미지 증폭)",
        "Ring of Blood (출혈 대미지 강화)",
        "None (미착용)"
    ],
    "weapons": [
        "Evanspear Handaxe (출혈 평타 극딜)",
        "Petra's Anchor (사일런트하트 묵직한 한방)",
        "Enforcer's Axe (가드브레이크 대검)",
        "Curved Blade of Winds (바람 속성 최고 존엄)",
        "Steel Skewered Dusters (스팀/아주르 1초 래그돌)",
        "Gran Sudaruska (빙결 프로스트 헤비)",
        "Hero Blade of Flame (화염 깡딜)",
        "Hero Blade of Frost (빙결 깡딜)",
        "Hero Blade of Thunder (번개 깡딜)",
        "Hero Blade of Wind (바람 깡딜)",
        "Kyrsblade (미디엄 연타)",
        "Alloyed Shotel (곡도/출혈)"
    ],
    "enchants": [
        "Detonation (하얀 폭발 딜 / 보스 체력 삭제)",
        "Astral (하얀 오라 / 순수 물리 대미지 증폭)",
        "Vampirism (적 타격 시 체력 흡수)",
        "Chilling (적 피격 시 빙결/슬로우)",
        "Blazing (적 피격 시 화염 도트 대미지)",
        "Grim (상대 방어력 깎고 지속 대미지)",
        "Nemesis (원거리 투사체 반격)",
        "None (노인챈트)"
    ],
    "bells": [
        "Reaper (영혼 수확 / 체력 흡수)",
        "Kamui (차원 도약 / 순간이동 무적)",
        "Wind Up (즉시 자세 회복 및 공속)",
        "Payphone (안전 텔레포트)",
        "Sacred Field (방어 결계)",
        "Smite (번개 심판 강타)"
    ]
}

def render_tooltip_badge(name: str, item_type: str = "talent") -> str:
    """CSS 툴팁 박스가 즉시 마우스 호버 시 뜨는 고품격 HTML 뱃지 렌더링 (Markdown 코드블록 오작동 방지용 단일 라인 포맷)"""
    clean = name.split("(")[0].strip()
    db = DEEPWOKEN_TALENTS_DB if item_type == "talent" else DEEPWOKEN_MANTRAS_DB
    
    info = None
    for k, v in db.items():
        if k.lower() in clean.lower() or clean.lower() in k.lower():
            info = v
            break
            
    if info:
        title_text = info.get("name_ko", clean)
        sub_text = f"📋 <b>요구치:</b> {info.get('req', '기본')}<br>🎯 <b>효과:</b> {info.get('desc', '')}" if item_type == "talent" else f"🏷️ <b>분류:</b> {info.get('category', '만트라')}<br>🎯 <b>효과:</b> {info.get('desc', '')}"
        tag_class = "talent-tag" if item_type == "talent" else "mantra-tag"
        icon = "⭐" if item_type == "talent" else "🔮"
        
        return f'<div class="deepwoken-tooltip-container"><span class="{tag_class}">{icon} {clean}</span><div class="tooltip-box"><div style="color: #e5b869; font-weight: bold; margin-bottom: 4px;">{title_text}</div><div style="color: #cbd5e1; font-size: 0.8rem;">{sub_text}</div></div></div>'
    else:
        tag_class = "talent-tag" if item_type == "talent" else "mantra-tag"
        icon = "⭐" if item_type == "talent" else "🔮"
        return f'<div class="deepwoken-tooltip-container"><span class="{tag_class}">{icon} {clean}</span><div class="tooltip-box"><div style="color: #e5b869; font-weight: bold; margin-bottom: 4px;">{clean}</div><div style="color: #cbd5e1; font-size: 0.8rem;">Deepwoken 고유 {item_type}입니다.</div></div></div>'

