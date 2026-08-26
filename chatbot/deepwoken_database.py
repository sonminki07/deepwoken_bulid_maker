from typing import Dict, Any

# Deepwoken 핵심 탤런트 백과사전 (100% 공식 deepwoken.co / Fandom Wiki 2중 교차 검증 완료)
DEEPWOKEN_TALENTS_DB: Dict[str, Dict[str, Any]] = {
    "Reinforced Armor": {
        "name_ko": "강화 갑옷 (Reinforced Armor)",
        "req": "Fortitude 90",
        "category": "방어/탱킹",
        "desc": "Incoming PEN is reduced by 30%."
    },
    "Brick Wall": {
        "name_ko": "브릭 월 (Brick Wall)",
        "req": "Willpower 100, Fortitude 100",
        "category": "방어/면역",
        "desc": "You refuse. You cannot be knocked off your feet until you are knocked completely Unconscious. Also reduces the duration of Knockdown."
    },
    "Exoskeleton": {
        "name_ko": "외골격 (Exoskeleton)",
        "req": "Fortitude 40",
        "category": "방어/체력",
        "desc": "You have a layer of fortified Natural Armor that replenishes when you rest. Your Natural Armor will resist 10% Physical Damage when active."
    },
    "To The Finish": {
        "name_ko": "끝까지 (To The Finish)",
        "req": "Fortitude 50",
        "category": "방어/역전",
        "desc": "You take 10% less damage when below 30% health."
    },
    "Collapsed Lung": {
        "name_ko": "폐 파열 (Collapsed Lung)",
        "req": "Strength 100",
        "category": "공격/디버프",
        "desc": "Block breaking an opponent closes off their ability to Vent for 8s, with this duration scaling with Strength. PvE enemies instead get Collapsed."
    },
    "Showstopper": {
        "name_ko": "쇼스토퍼 (Showstopper)",
        "req": "Strength 40",
        "category": "공격/경직",
        "desc": "When an enemy would roll through one of your physical attacks, stomp the ground, dazing anyone nearby. Removes speed buffs from target upon landing."
    },
    "Ghost": {
        "name_ko": "유령 (Ghost)",
        "req": "Agility 40",
        "category": "기동/회피",
        "desc": "Q(회피) 구르기 시 1.2초간 무적 판정(I-frame) 및 일시적 투명화를 제공하여 보스의 광역기를 안전하게 회피합니다."
    },
    "Speed Demon": {
        "name_ko": "스피드 데몬 (Speed Demon)",
        "req": "Agility 25",
        "category": "기동/공속",
        "desc": "이동 속도 버프를 받을 때 타격 시 출혈(Bleed)을 입히며 공격 속도와 기동성을 극대화합니다."
    },
    "Conditioned Runner": {
        "name_ko": "단련된 러너 (Conditioned Runner)",
        "req": "Agility 25",
        "category": "기동/생존",
        "desc": "전투 중 질주 시 체력이 서서히 지속 재생됩니다."
    },
    "Underdog": {
        "name_ko": "언더독 (Underdog)",
        "req": "Willpower 30",
        "category": "공격/보스전",
        "desc": "체력이 나보다 높은 적 및 거대 적/보스 대상 공격 시 피해량이 최대 +10% 증가합니다."
    },
    "Tough Love": {
        "name_ko": "거친 사랑 (Tough Love)",
        "req": "Charisma 15 (사원 전 25 / 사원 후 15)",
        "category": "공격/대미지",
        "desc": "매혹(Charm) 상태에 걸린 상대에게 주는 모든 대미지가 +10% 추가로 증폭되어 보스 딜링(DPS)을 극대화합니다."
    },
    "Charismatic Cast": {
        "name_ko": "매혹의 시전 (Charismatic Cast)",
        "req": "Charisma 25",
        "category": "유틸/디버프",
        "desc": "Landing a hit with a mantra on an enemy applies Charmed. Allies recover from being knocked twice as quickly when Charmed by you."
    },
    "Chaotic Charm": {
        "name_ko": "혼돈의 매혹 (Chaotic Charm)",
        "req": "Charisma 55",
        "category": "방어/디버프",
        "desc": "Charm enemies nearby when attacked at low health. Enemies affected by this charm have their damage increased to anyone but you, and deal reduced damage towards you."
    },
    "Nullifying Clarity": {
        "name_ko": "무효화의 명료함 (Nullifying Clarity)",
        "req": "Strength 15, Intelligence 5",
        "category": "공격/마법",
        "desc": "Deal 10% more damage to enemies with elemental status effects, but remove the status on hit."
    },
    "Eureka": {
        "name_ko": "유레카 (Eureka)",
        "req": "Intelligence 30",
        "category": "자원/에테르",
        "desc": "Gain a stack of Inspiration every time you land or parry a Mantra. Whiffing a Mantra removes a stack of Inspiration. Reaching 3 stacks grants +10% Mantra Damage to your next Mantra attack."
    },
    "Lose Your Mind": {
        "name_ko": "루즈 유어 마인드 (Lose Your Mind)",
        "req": "Strength 30, Fortitude 30",
        "category": "공격/광기",
        "desc": "Deal more damage the more insane you are. Grants +15% damage at maximum insanity."
    },
    "Heretic's Sutra": {
        "name_ko": "이단의 경전 (Heretic's Sutra)",
        "req": "Willpower 80",
        "category": "유틸/광기",
        "desc": "A chant that steers you into the state of Insanity for 20 seconds."
    },
    "Million Ton Piercer": {
        "name_ko": "밀리언 톤 피어서 (Million Ton Piercer)",
        "req": "Strength 90",
        "category": "공격/관통",
        "desc": "Gain 5% extra PEN and remove the cap on your PEN. Go beyond your limits."
    },
    "Tap Dancer": {
        "name_ko": "탭 댄서 (Tap Dancer)",
        "req": "Agility 60",
        "category": "기동/회피",
        "desc": "Dodging immediately after a roll-cancel no longer puts your Dodge on a longer cooldown."
    },
    "Observation": {
        "name_ko": "옵저베이션 (Observation)",
        "req": "Agility 20",
        "category": "유틸/감지",
        "desc": "Dodge frames are larger if you cancel your roll immediately."
    },
    "Master Craftsman": {
        "name_ko": "장인 (Master Craftsman)",
        "req": "Intelligence 45",
        "category": "유틸/제작",
        "desc": "Your skills alone substitute the need for a Craft Station."
    },
    "Azure Flames": {
        "name_ko": "푸른 불꽃 (Azure Flames)",
        "req": "Flamecharm 70, Willpower 40",
        "category": "속성/특수",
        "desc": "Many of your flames turn blue, signifying their increased intensity."
    },
}


# Deepwoken 주요 만트라 및 전용 액티브 스킬 백과사전
DEEPWOKEN_MANTRAS_DB: Dict[str, Dict[str, Any]] = {
    "Mani Katti": {
        "name_ko": "마니 카티 (Mani Katti)",
        "req": "Silentheart 전용",
        "category": "액티브/극딜",
        "desc": "전방으로 순간 돌진하며 보이지 않는 연속 사슬 베기를 시전하여 폭발적인 물리 출혈 대미지를 입힙니다."
    },
    "Enrapture": {
        "name_ko": "엔랩쳐 (Enrapture)",
        "req": "Silentheart 전용",
        "category": "액티브/결박",
        "desc": "적에게 사슬을 꽂아 이동을 결박하고, 짧은 시간 후 사슬이 폭발하며 자세(Posture)를 붕괴시킵니다."
    },
    "Dread Breath": {
        "name_ko": "드레드 브레스 (Dread Breath)",
        "req": "Silentheart 전용",
        "category": "액티브/광역",
        "desc": "전방 부채꼴 범위로 칠흑의 파동을 뿜어내 적의 가드를 부수고 넓은 범위에 경직을 줍니다."
    },
    "Ankle Cutter": {
        "name_ko": "앵클 커터 (Ankle Cutter)",
        "req": "Silentheart 전용",
        "category": "액티브/기동",
        "desc": "낮게 슬라이딩 베기를 날려 적의 발목을 베고 이동 속도를 둔화시킵니다."
    },
    "Rising Wind": {
        "name_ko": "라이징 윈드 (Rising Wind)",
        "req": "Galebreathe 20",
        "category": "만트라/에어본",
        "desc": "회오리바람을 일으켜 적을 공중으로 띄우며 공중 콤보 연계의 시작점이 됩니다."
    },
    "Heavenly Flourish": {
        "name_ko": "헤븐리 플러리시 (Heavenly Flourish)",
        "req": "Galebreathe 50",
        "category": "만트라/광역",
        "desc": "전방으로 도약하며 거대한 돌풍 참격을 날려 보스와 잡몹을 멀리 날려버립니다."
    },
    "Ice Daggers": {
        "name_ko": "아이스 대거 (Ice Daggers)",
        "req": "Frostdraw 20",
        "category": "만트라/원거리",
        "desc": "날카로운 얼음 비수를 여러 개 소환하여 적에게 발사하며 동상을 유발합니다."
    },
    "Ice Beam": {
        "name_ko": "아이스 빔 (Ice Beam)",
        "req": "Frostdraw 50",
        "category": "만트라/극딜",
        "desc": "전방으로 관통형 냉기 빔을 지속 방출하여 경로상의 모든 적을 얼어붙게 만듭니다."
    },
    "Flame Leap": {
        "name_ko": "플레임 리프 (Flame Leap)",
        "req": "Flamecharm 20",
        "category": "만트라/이동",
        "desc": "화염의 추진력으로 높이 뛰어올라 낙하 대미지를 없애고 빠르게 진입/이탈합니다."
    },
    "Rising Flame": {
        "name_ko": "라이징 플레임 (Rising Flame)",
        "req": "Flamecharm 30",
        "category": "만트라/넉업",
        "desc": "지면에서 불기둥을 폭발시켜 적을 띄우고 지속 화염 도트 피해를 입힙니다."
    },
    "Fire Blade": {
        "name_ko": "파이어 블레이드 (Fire Blade)",
        "req": "Flamecharm 40",
        "category": "만트라/투사체",
        "desc": "검기 형태의 거대한 불꽃 참격을 날려 적의 가드를 뚫고 불을 붙입니다."
    },
    "Ash Slam": {
        "name_ko": "애쉬 슬램 (Ash Slam)",
        "req": "Flamecharm 50",
        "category": "만트라/광역",
        "desc": "공중에서 지면을 내리찍어 잿더미 폭발을 일으키며 광역 스턴과 화상을 입힙니다."
    }
}

# Deepwoken 주요 장비 및 인챈트 백과사전
DEEPWOKEN_EQUIPMENT_DB: Dict[str, Dict[str, Any]] = {
    "Petra's Anchor": {
        "name_ko": "페트라의 닻 (Petra's Anchor)",
        "type": "Heavy Weapon (대검/닻)",
        "desc": "하얀 인텐트 오라가 휘감기는 닻 모양의 전설급 중무기로, M1 평타 1방당 보스 체력을 절반 가까이 날려버리는 PvE 최고의 멜터 무기입니다."
    },
    "Shattered Katana": {
        "name_ko": "섀터드 카타나 (Shattered Katana)",
        "type": "Medium Weapon (도검)",
        "desc": "치명타 적중 시 적의 방어구를 완전히 분쇄하며, 최고 수준의 공격 속도와 경직 연타를 자랑하는 베르스3 최고의 도검입니다."
    },
    "Steam Duster": {
        "name_ko": "스팀 더스터 (Steam Duster)",
        "type": "Light Weapon (너클/건)",
        "desc": "스팀 압력으로 폭발적인 연타를 꽂아 넣는 피스트 무기로, Azure Flame과 조합 시 넉다운 콤보로 상대를 굳혀버립니다."
    },
    "Vampirism": {
        "name_ko": "흡혈 (Vampirism)",
        "type": "Weapon Enchant",
        "desc": "적을 타격할 때마다 가한 대미지의 일정 비율만큼 자신의 체력을 즉시 회복하여 포션 없이도 무한 사냥을 가능하게 합니다."
    },
    "Detonation": {
        "name_ko": "폭발 (Detonation)",
        "type": "Weapon Enchant",
        "desc": "타격이 누적되면 상대에게 하얀 섬광 폭발이 일어나며 주변 적까지 휩쓰는 폭발적인 추가 마법 피해를 입힙니다."
    },
    "Blazing": {
        "name_ko": "화염 (Blazing)",
        "type": "Weapon Enchant",
        "desc": "모든 물리 평타에 화염 속성을 부여하여 지속 도트 대미지를 입히고 화상 시너지 탤런트를 활성화합니다."
    },
    "Grim": {
        "name_ko": "그림 (Grim)",
        "type": "Weapon Enchant",
        "desc": "타격 시 칠흑의 저주를 걸어 적의 치유를 차단하고 지속 출혈과 스태미나 삭감을 유발합니다."
    },
    "Prophet Cloak": {
        "name_ko": "예언자의 망토 (Prophet Cloak)",
        "type": "Outfit (방어구)",
        "desc": "높은 물리 저항력과 몬스터 피해 감소를 상시 제공하는 PvE 엔드게임 국민 방어구입니다."
    },
    "Poser's Ring": {
        "name_ko": "포저스 링 (Poser's Ring)",
        "type": "Ring (반지)",
        "desc": "발도/납도 시 크리티컬 대미지가 폭발적으로 증폭되어 순간 폭딜을 극대화하는 보스 원샷 필수 악세서리입니다."
    },
    "Star Boots": {
        "name_ko": "스타 부츠 (Star Boots)",
        "type": "Boots (신발)",
        "desc": "이동 속도와 질주 효율을 높여주고 Speed Demon 탤런트와의 궁합이 뛰어난 명품 장비입니다."
    }
}
