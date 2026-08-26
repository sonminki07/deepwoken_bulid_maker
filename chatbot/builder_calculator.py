from typing import Dict, Any, Tuple

# 12대 Deepwoken 공식 종족 (Races) 및 고유 보너스
DEEPWOKEN_RACES = {
    "Celtor": {"stats": {"Charisma": 2, "Intelligence": 2}, "desc": "지능 2, 매력 2 / 항해 및 은신 특화"},
    "Adret": {"stats": {"Charisma": 2, "Willpower": 2}, "desc": "매력 2, 의지 2 / 빠른 학습(Fast Learner)"},
    "Canor": {"stats": {"Strength": 2, "Fortitude": 2}, "desc": "근력 2, 인내 2 / 아군 사기 진작"},
    "Capra": {"stats": {"Willpower": 2, "Intelligence": 2}, "desc": "의지 2, 지능 2 / 치료 및 허기 회복 마크"},
    "Castellan": {"stats": {"Fortitude": 2, "Charisma": 2}, "desc": "인내 2, 매력 2 / 추가 에테르 +5"},
    "Chrysid": {"stats": {"Agility": 2, "Fortitude": 2}, "desc": "민첩 2, 인내 2 / 곤충 날개 활공"},
    "Etrean": {"stats": {"Agility": 2, "Intelligence": 2}, "desc": "민첩 2, 지능 2 / 산도 및 출혈 저항"},
    "Felinor": {"stats": {"Agility": 2, "Charisma": 2}, "desc": "민첩 2, 매력 2 / 나무 및 벽타기 특화"},
    "Gremor": {"stats": {"Strength": 2, "Fortitude": 2}, "desc": "근력 2, 인내 2 / 나침반 및 허기 감소 완화"},
    "Khan": {"stats": {"Strength": 2, "Agility": 2}, "desc": "근력 2, 민첩 2 / 장비 요구 스탯 -3 감소"},
    "Tiran": {"stats": {"Agility": 2, "Willpower": 2}, "desc": "민첩 2, 의지 2 / 낙하 피해 면역 및 활공"},
    "Vesperian": {"stats": {"Fortitude": 2, "Willpower": 2}, "desc": "인내 2, 의지 2 / 천연 가면 방어구 +10% 물리 저항"},
}

# 인기 방어구(Armor/Outfit) 템플릿
OUTFIT_PRESETS = {
    "Black Diver (엔드게임 방어구)": {"hp": 45, "phys_resist": 28, "elem_resist": 25, "dve": 10},
    "Ignition Centurion (초중장갑 극탱)": {"hp": 55, "phys_resist": 35, "elem_resist": 15, "dve": 15},
    "Prophet Cloak (에테르 마법사)": {"hp": 30, "phys_resist": 18, "elem_resist": 30, "dve": 20},
    "Ferryman Coat (민첩/기동성)": {"hp": 35, "phys_resist": 22, "elem_resist": 28, "dve": 15},
    "Master's Armor (균형형)": {"hp": 40, "phys_resist": 25, "elem_resist": 20, "dve": 10},
    "기본 방어구 (Starter Armor)": {"hp": 15, "phys_resist": 10, "elem_resist": 5, "dve": 0},
}

class DeepwokenCalculator:
    """Deepwoken Builder (deepwoken.co) 공식 수치 및 스탯/저항력 실시간 계산 엔진"""

    @staticmethod
    def calculate_character_sheet(
        race: str,
        stats: Dict[str, int],
        traits: Dict[str, int],
        equipment: Dict[str, Any],
        talents_str: str = ""
    ) -> Dict[str, Any]:
        """기본 스탯, 4대 Traits, 장비, 탤런트를 종합하여 STATS 및 RESISTANCES 계산"""
        
        # 1. 6대 스탯 값 추출
        strength = stats.get("Strength", 0)
        fortitude = stats.get("Fortitude", 0)
        agility = stats.get("Agility", 0)
        intelligence = stats.get("Intelligence", 0)
        willpower = stats.get("Willpower", 0)
        charisma = stats.get("Charisma", 0)
        heavy_wep = stats.get("Heavy Wep", 0)
        med_wep = stats.get("Medium Wep", 0)
        light_wep = stats.get("Light Wep", 0)
        max_wep = max(heavy_wep, med_wep, light_wep)

        # 2. 4대 Traits (각 특성당 0~6pt, 총합 최대 12pt 투자 - Deepwoken Wiki 공식 룰)
        vitality = min(6, max(0, traits.get("Vitality", 0)))
        erudition = min(6, max(0, traits.get("Erudition", 0)))
        proficiency = min(6, max(0, traits.get("Proficiency", 0)))
        songchant = min(6, max(0, traits.get("Songchant", 0)))

        # 3. 장비 옵션 추출
        outfit_name = equipment.get("outfit", "Black Diver (엔드게임 방어구)")
        outfit_data = OUTFIT_PRESETS.get(outfit_name, OUTFIT_PRESETS["Black Diver (엔드게임 방어구)"])
        
        extra_hp = equipment.get("extra_hp", 0) + outfit_data["hp"]
        extra_phys_resist = outfit_data["phys_resist"]
        extra_elem_resist = outfit_data["elem_resist"]
        extra_dve = equipment.get("extra_dve", 0)  # Dmg vs Monsters

        # 4. 탤런트 패시브 계산
        has_exoskeleton = "exoskeleton" in talents_str.lower() or fortitude >= 40
        has_reinforced = "reinforced armor" in talents_str.lower() or fortitude >= 90
        has_to_the_finish = "to the finish" in talents_str.lower() or fortitude >= 40
        has_giant_slayer = "giant slayer" in talents_str.lower() or willpower >= 50
        has_tough_love = "tough love" in talents_str.lower() or charisma >= 25
        has_speed_demon = "speed demon" in talents_str.lower() or agility >= 25
        has_brick_wall = "brick wall" in talents_str.lower() or (fortitude >= 100 and willpower >= 100)

        # 5. ❤️ Max Health (체력) 산출 (Wiki: Vitality 포인트당 +10 HP)
        # 기본 200 + (Fortitude * 0.5) + (Vitality * 10) + 장비 HP + 탤런트(Exo +5, To the Finish +10, Reinforced +15)
        talent_hp_bonus = (5 if has_exoskeleton else 0) + (10 if has_to_the_finish else 0) + (15 if has_reinforced else 0)
        total_hp = int(200 + (fortitude * 0.5) + (vitality * 10) + extra_hp + talent_hp_bonus)

        # 6. 🛡️ Posture (자세)
        # 기본 20 + (Strength * 0.25) + (Fortitude * 0.25)
        total_posture = int(20 + (strength * 0.25) + (fortitude * 0.25) + (10 if has_brick_wall else 0))

        # 7. 💠 Ether (에테르) & ⏩ Tempo (템포) (Wiki: Erudition 포인트당 +25 Ether, +5 Tempo)
        total_ether = int(100 + (intelligence * 0.5) + (erudition * 25) + (5 if race == "Castellan" else 0))
        total_tempo = int(100 + (willpower * 0.5) + (erudition * 5))

        # 8. 🧠 Sanity & 🏃 Movement Speed %
        total_sanity = int(100 + (willpower * 0.5))
        move_speed_pct = round(100.0 + (agility * 0.1) + (5.0 if has_speed_demon else 0.0), 1)

        # 9. 🗡️ Damage vs Monsters (PvE 보스전 딜증 %)
        pve_dmg_pct = round(
            (proficiency * 2.5) + 
            (15.0 if has_giant_slayer else 0.0) + 
            (10.0 if has_tough_love else 0.0) + 
            extra_dve, 
            1
        )

        # 10. 🛡️ Resistances (물리 및 속성 저항력 %)
        vesperian_bonus = 10.0 if race == "Vesperian" else 0.0
        exo_bonus = 5.0 if has_exoskeleton else 0.0
        reinf_bonus = 10.0 if has_reinforced else 0.0

        slash_resist = round(extra_phys_resist + vesperian_bonus + exo_bonus + reinf_bonus, 1)
        blunt_resist = round(extra_phys_resist + vesperian_bonus + exo_bonus + reinf_bonus, 1)
        pierce_resist = round(extra_phys_resist + vesperian_bonus + exo_bonus + reinf_bonus, 1)

        flame_resist = round(extra_elem_resist + (5.0 if fortitude >= 50 else 0.0), 1)
        frost_resist = round(extra_elem_resist + (5.0 if fortitude >= 50 else 0.0), 1)
        thunder_resist = round(extra_elem_resist + (5.0 if fortitude >= 50 else 0.0), 1)
        gale_resist = round(extra_elem_resist + (5.0 if fortitude >= 50 else 0.0), 1)
        shadow_resist = round(extra_elem_resist + (5.0 if willpower >= 50 else 0.0), 1)

        return {
            "stats": {
                "health": total_hp,
                "posture": total_posture,
                "ether": total_ether,
                "tempo": total_tempo,
                "sanity": total_sanity,
                "speed_pct": move_speed_pct,
                "pve_dmg_pct": pve_dmg_pct,
            },
            "resistances": {
                "slash": slash_resist,
                "blunt": blunt_resist,
                "pierce": pierce_resist,
                "flame": flame_resist,
                "frost": frost_resist,
                "thunder": thunder_resist,
                "gale": gale_resist,
                "shadow": shadow_resist,
            },
            "traits": {
                "vitality": vitality,
                "erudition": erudition,
                "proficiency": proficiency,
                "songchant": songchant,
                "total_trait_points": vitality + erudition + proficiency + songchant,
            },
            "talents_summary": {
                "exoskeleton": has_exoskeleton,
                "reinforced_armor": has_reinforced,
                "brick_wall": has_brick_wall,
                "giant_slayer": has_giant_slayer,
                "tough_love": has_tough_love,
            }
        }
