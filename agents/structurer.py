import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional
try:
    import jsonschema
    JSONSCHEMA_AVAILABLE = True
except ImportError:
    JSONSCHEMA_AVAILABLE = False

logger = logging.getLogger(__name__)

class BuildStructurer:
    """3단계: JSON 스키마 검증 및 Markdown 지식 문서 변환기"""

    def __init__(
        self,
        schema_path: str = "config/build_schema.json",
        analysis_dir: str = "data/analysis",
        knowledge_base_dir: str = "data/knowledge_base"
    ):
        self.schema_path = Path(schema_path)
        self.analysis_dir = Path(analysis_dir)
        self.knowledge_base_dir = Path(knowledge_base_dir)

        self.analysis_dir.mkdir(parents=True, exist_ok=True)
        self.knowledge_base_dir.mkdir(parents=True, exist_ok=True)

        if self.schema_path.exists():
            self.schema = json.loads(self.schema_path.read_text(encoding="utf-8"))
        else:
            self.schema = None
            logger.warning(f"Schema file not found at {schema_path}. Validation will be skipped.")

    def validate(self, build_data: Dict[str, Any]) -> bool:
        """JSON 데이터 스키마 유효성 검증"""
        if not self.schema or not JSONSCHEMA_AVAILABLE:
            return True
        try:
            jsonschema.validate(instance=build_data, schema=self.schema)
            logger.info("JSON Schema validation passed.")
            return True
        except Exception as e:
            logger.warning(f"JSON Schema validation warning: {e}")
            return False

    def sanitize(self, build_data: Dict[str, Any]) -> Dict[str, Any]:
        """누락 필드 보정 및 중첩 구조의 표준 정규화"""
        sanitized = dict(build_data)
        
        # 1. video_meta 정규화
        vm = sanitized.get("video_meta") or sanitized.get("video_metadata") or {}
        sanitized["video_meta"] = {
            "title": vm.get("title", "Unknown Title"),
            "channel": vm.get("channel", "Unknown Channel"),
            "url": vm.get("url", ""),
            "upload_date": vm.get("upload_date", "N/A"),
            "estimated_patch": vm.get("patch_version") or vm.get("estimated_patch", "Unknown")
        }
        
        # 2. build_summary 정규화
        bs = sanitized.get("build_summary", {})
        sanitized["build_summary"] = {
            "build_name": bs.get("build_name") or sanitized.get("build_name", "Unnamed Build"),
            "build_type": bs.get("build_type", "PvE"),
            "difficulty": bs.get("difficulty", "Intermediate"),
            "creator_opinion": bs.get("creator_opinion", "No summary provided."),
            "strengths": bs.get("strengths", []),
            "weaknesses": bs.get("weaknesses", [])
        }

        # 3. stats & attunements 정규화
        stats_raw = dict(sanitized.get("stats", {}))
        att_raw = dict(sanitized.get("attunements", {}))
        
        if "stats_and_attunements" in sanitized:
            saa = sanitized["stats_and_attunements"]
            if isinstance(saa, dict):
                if "stats" in saa and isinstance(saa["stats"], dict):
                    stats_raw.update(saa["stats"])
                if "base_stats" in saa and isinstance(saa["base_stats"], dict):
                    stats_raw.update(saa["base_stats"])
                if "weapon_stats" in saa and isinstance(saa["weapon_stats"], dict):
                    stats_raw.update(saa["weapon_stats"])
                if "attunements" in saa and isinstance(saa["attunements"], dict):
                    att_raw.update(saa["attunements"])

        # 스탯 키 표준화
        normalized_stats = {}
        key_map = {
            "strength": "strength", "fortitude": "fortitude", "agility": "agility",
            "intelligence": "intelligence", "willpower": "willpower", "charisma": "charisma",
            "heavy_wep": "heavy_wep", "heavy_weapon": "heavy_wep", "heavy": "heavy_wep",
            "medium_wep": "medium_wep", "medium_weapon": "medium_wep", "medium": "medium_wep",
            "light_wep": "light_wep", "light_weapon": "light_wep", "light": "light_wep"
        }
        for k, v in stats_raw.items():
            k_lower = k.lower().replace(" ", "_")
            if k_lower in key_map and isinstance(v, (int, float)):
                normalized_stats[key_map[k_lower]] = int(v)

        sanitized["stats"] = normalized_stats
        sanitized["attunements"] = {k: int(v) for k, v in att_raw.items() if isinstance(v, (int, float))}

        # 4. character details 정규화 (character_setup 및 character_details 지원)
        cd = sanitized.get("character_details") or sanitized.get("character_setup") or {}
        if isinstance(cd, dict):
            sanitized["oath"] = cd.get("oath", sanitized.get("oath", "Oathless"))
            sanitized["race"] = cd.get("race", sanitized.get("race", "N/A"))
            sanitized["origin"] = cd.get("origin", sanitized.get("origin", "N/A"))
            sanitized["murmur"] = cd.get("murmur", sanitized.get("murmur", "N/A"))
            sanitized["resonance"] = cd.get("resonance_bell") or cd.get("resonance", sanitized.get("resonance", "N/A"))

        # 5. talents & mantras 정규화
        tm = sanitized.get("talents_and_mantras", {})
        if isinstance(tm, dict):
            if "talents" in tm and not sanitized.get("talents"):
                sanitized["talents"] = tm["talents"]
            elif "core_talents" in tm and not sanitized.get("talents"):
                sanitized["talents"] = [{"name": t, "is_core": True} if isinstance(t, str) else t for t in tm["core_talents"]]
            if "mantras" in tm and not sanitized.get("mantras"):
                sanitized["mantras"] = tm["mantras"]

        # 6. weapons & equipment 정규화
        we = sanitized.get("weapons_and_equipment", {})
        if isinstance(we, dict) and we:
            if "weapon" in we and not sanitized.get("weapons"):
                w_str = we["weapon"]
                w_type = we.get("weapon_type", "")
                w_enc = we.get("weapon_enchant", "None")
                sanitized["weapons"] = [{"name": w_str, "type": w_type, "enchant": w_enc}]
            if not sanitized.get("equipment"):
                eq_list = []
                if "outfit" in we:
                    eq_list.append({"slot": "Outfit", "name": we["outfit"]})
                if "accessories" in we:
                    acc = we["accessories"]
                    if isinstance(acc, list):
                        for a in acc:
                            eq_list.append({"slot": "Accessory", "name": str(a)})
                    elif isinstance(acc, str):
                        eq_list.append({"slot": "Accessories", "name": acc})
                sanitized["equipment"] = eq_list
        else:
            eq_raw = sanitized.get("equipment", [])
            if isinstance(eq_raw, dict):
                if "weapons" in eq_raw and not sanitized.get("weapons"):
                    sanitized["weapons"] = eq_raw["weapons"]
                sanitized["equipment"] = eq_raw.get("armor", [])
            else:
                sanitized["equipment"] = eq_raw

        # 7. shrine_of_order
        sop = sanitized.get("shrine_of_order_progression", {})
        if isinstance(sop, dict) and sop and not sanitized.get("shrine_of_order_path"):
            pre = sop.get("pre_shrine") or sop.get("pre_shrine_stats") or {}
            post = sop.get("post_shrine_priority", [])
            pre_str = ", ".join([f"{k.capitalize()} {v}" for k, v in pre.items()]) if isinstance(pre, dict) and pre else str(pre)
            sanitized["shrine_of_order_path"] = f"**Pre-Shrine**: `{pre_str}`\n**Post-Shrine 우선순위**:\n" + "\n".join([f"- {p}" for p in post])

        # 8. combo & playstyle
        cp = sanitized.get("combo_and_playstyle") or sanitized.get("combo_and_playstyle_guide") or {}
        if isinstance(cp, dict) and cp and not sanitized.get("combo_guide"):
            c_guide = cp.get("combo_guide") or cp.get("damage_rotation", "")
            tips = cp.get("tips", "")
            if c_guide or tips:
                sanitized["combo_guide"] = f"{c_guide}\n\n{tips}".strip()

        cg_raw = sanitized.get("combo_guide")
        if isinstance(cg_raw, dict):
            sanitized["combo_guide"] = str(cg_raw.get("combo_guide") or cg_raw.get("damage_rotation") or cg_raw)
        elif isinstance(cg_raw, list):
            sanitized["combo_guide"] = "\n".join([str(x) for x in cg_raw])

        # 10. traits, combat_stats, resistances 정규화
        tr = sanitized.get("traits") or (cd.get("traits") if isinstance(cd, dict) else {}) or {}
        if isinstance(tr, dict):
            sanitized["traits"] = {k: int(v) for k, v in tr.items() if isinstance(v, (int, float))}

        cs = sanitized.get("combat_stats") or {}
        if isinstance(cs, dict):
            sanitized["combat_stats"] = cs

        res = sanitized.get("resistances") or {}
        if isinstance(res, dict):
            sanitized["resistances"] = res

        # 11. weapons 정제 (Astral Enchant 등 괄호 중복 제거)
        clean_weapons = []
        import re
        raw_weps = sanitized.get("weapons", [])
        if isinstance(raw_weps, dict):
            raw_weps = [raw_weps]
        for w in raw_weps:
            if isinstance(w, str):
                m_enc = re.search(r'\(([^)]*enchant[^)]*)\)', w, re.IGNORECASE)
                enc_val = m_enc.group(1).replace("Enchant", "").strip() if m_enc else "None"
                clean_name = re.sub(r'\([^)]*\)', '', w).strip()
                clean_weapons.append({"name": clean_name, "type": "Weapon", "enchant": enc_val})
            elif isinstance(w, dict):
                w_name = str(w.get("name", "Unknown"))
                m_enc = re.search(r'\(([^)]*enchant[^)]*)\)', w_name, re.IGNORECASE)
                enc_val = str(w.get("enchant") or (m_enc.group(1).replace("Enchant", "").strip() if m_enc else "None"))
                clean_name = re.sub(r'\([^)]*\)', '', w_name).strip()
                w_type = str(w.get("type", "Weapon")).strip(" ()")
                clean_weapons.append({
                    "name": clean_name,
                    "type": w_type,
                    "enchant": enc_val,
                    "stars": w.get("stars", 0) if isinstance(w.get("stars"), int) else 0
                })
        sanitized["weapons"] = clean_weapons

        # 12. patch version 추정 보정
        if sanitized["video_meta"].get("estimated_patch") in ["Unknown", "N/A", None]:
            u_date = sanitized["video_meta"].get("upload_date", "")
            if u_date and len(u_date) >= 4:
                year = int(u_date[:4]) if u_date[:4].isdigit() else 2024
                if year >= 2025:
                    sanitized["video_meta"]["estimated_patch"] = "Verse 3 (Latest / Diluvian Era)"
                elif year >= 2024:
                    sanitized["video_meta"]["estimated_patch"] = "Verse 2 (Layer 2 Floor 2 Era)"
                else:
                    sanitized["video_meta"]["estimated_patch"] = "Verse 2"

        return sanitized

    def to_markdown(self, build_data: Dict[str, Any]) -> str:
        """구조화된 JSON 데이터를 가독성 높은 Markdown 문서로 변환"""
        meta = build_data.get("video_meta", {})
        summary = build_data.get("build_summary", {})
        stats = build_data.get("stats", {})
        attunements = build_data.get("attunements", {})
        weapons = build_data.get("weapons", [])
        talents = build_data.get("talents", [])
        mantras = build_data.get("mantras", [])
        equipment = build_data.get("equipment", [])
        traits = build_data.get("traits", {})
        combat_stats = build_data.get("combat_stats", {})
        resistances = build_data.get("resistances", {})

        title = summary.get("build_name") or meta.get("title", "Deepwoken Build")
        build_type = summary.get("build_type", "Hybrid")
        difficulty = summary.get("difficulty", "Intermediate")
        oath = build_data.get("oath", "Oathless")
        race = build_data.get("race", "N/A")
        origin = build_data.get("origin", "N/A")
        murmur = build_data.get("murmur", "N/A")
        resonance = build_data.get("resonance", "N/A")

        lines = [
            f"# ⚔️ {title}",
            "",
            f"> **출처 영상**: [{meta.get('title', 'YouTube Link')}]({meta.get('url', '#')}) by `{meta.get('channel', 'Unknown')}`",
            f"> **패치 버전**: `{meta.get('estimated_patch', 'Verse 3')}` | **타입**: `{build_type}` | **난이도**: `{difficulty}`",
            f"> **종족/출신**: `{race}` / `{origin}` | **Oath**: `{oath}` | **Murmur/Bell**: `{murmur}` / `{resonance}`",
            "",
            "---",
            "",
            "## 📝 빌드 개요 및 총평",
            f"{summary.get('creator_opinion', '설명 없음')}",
            ""
        ]

        # 장점 / 단점
        strengths = summary.get("strengths", [])
        weaknesses = summary.get("weaknesses", [])
        if strengths or weaknesses:
            lines.append("### ⚖️ 장점 및 단점")
            if strengths:
                lines.append("**장점**:")
                for s in strengths:
                    lines.append(f"- ✅ {s}")
            if weaknesses:
                lines.append("**단점**:")
                for w in weaknesses:
                    lines.append(f"- ⚠️ {w}")
            lines.append("")

        # 4대 특성 (Traits) 표
        if traits:
            lines.extend([
                "## 🧬 4대 고유 특성 (Traits)",
                "| Vitality (생명력) | Erudition (학식) | Proficiency (숙련) | Songchant (영창) |",
                "| :---: | :---: | :---: | :---: |",
                f"| `{traits.get('vitality', 0)}` | `{traits.get('erudition', 0)}` | `{traits.get('proficiency', 0)}` | `{traits.get('songchant', 0)}` |",
                ""
            ])

        # 스탯 및 Shrine of Order 분배 표
        sop = build_data.get("shrine_progression") or build_data.get("shrine_of_order_progression") or {}
        pre_stats = sop.get("pre_shrine") if isinstance(sop, dict) else {}
        post_prio = sop.get("post_shrine_priority") or sop.get("post_shrine_priorities") or []
        pre_talents = sop.get("pre_shrine_talents", [])

        lines.append("## 📊 스탯 분배 및 육성 경로 (Stats & Build Progression)")
        
        # 1. Pre-Shrine 스탯이 존재하는 경우 2단계 표로 분리 렌더링
        if isinstance(pre_stats, dict) and pre_stats:
            lines.extend([
                "### ⛩️ 1단계: 질서의 성소 전 (Pre-Shrine 육성 목표 스탯)",
                "| 스탯 항목 (Attribute) | 성소 전 수치 (Pre-Shrine) |",
                "| :--- | :---: |",
                f"| Strength (근력) | `{pre_stats.get('strength', stats.get('strength', 0))}` |",
                f"| Fortitude (인내) | `{pre_stats.get('fortitude', stats.get('fortitude', 0))}` |",
                f"| Agility (민첩) | `{pre_stats.get('agility', stats.get('agility', 0))}` |",
                f"| Intelligence (지능) | `{pre_stats.get('intelligence', stats.get('intelligence', 0))}` |",
                f"| Willpower (의지) | `{pre_stats.get('willpower', stats.get('willpower', 0))}` |",
                f"| Charisma (매력) | `{pre_stats.get('charisma', stats.get('charisma', 0))}` |",
            ])
            if "bloodrend" in pre_stats or "heavy_wep" in pre_stats or "light_wep" in pre_stats:
                for k, v in pre_stats.items():
                    if k not in ["strength", "fortitude", "agility", "intelligence", "willpower", "charisma"]:
                        lines.append(f"| {k.capitalize()} | `{v}` |")
            lines.append("")
            
            if pre_talents:
                lines.append("**성소 전 선행 필수 탤런트**:")
                for pt in pre_talents:
                    lines.append(f"- 🌟 {pt}")
                lines.append("")

            lines.extend([
                "### ⚡ 2단계: 질서의 성소 후 / 최종 완성 스탯 (Post-Shrine Final Stats)",
                "| 스탯 항목 (Attribute) | 최종 완성 수치 (Final Points) |",
                "| :--- | :---: |",
                f"| Strength (근력) | `{stats.get('strength', 0)}` |",
                f"| Fortitude (인내) | `{stats.get('fortitude', 0)}` |",
                f"| Agility (민첩) | `{stats.get('agility', 0)}` |",
                f"| Intelligence (지능) | `{stats.get('intelligence', 0)}` |",
                f"| Willpower (의지) | `{stats.get('willpower', 0)}` |",
                f"| Charisma (매력) | `{stats.get('charisma', 0)}` |",
                f"| Heavy Wep (중화기) | `{stats.get('heavy_wep', 0)}` |",
                f"| Medium Wep (중형무기) | `{stats.get('medium_wep', 0)}` |",
                f"| Light Wep (경화기) | `{stats.get('light_wep', 0)}` |",
                ""
            ])
            
            if post_prio:
                lines.append("**성소 후 육성 우선순위 (Post-Shrine Priority)**:")
                for pp in post_prio:
                    lines.append(f"- 🎯 {pp}")
                lines.append("")
        else:
            # 단일 스탯 표
            lines.extend([
                "| 스탯 항목 (Attribute) | 수치 (Points) |",
                "| :--- | :--- |",
                f"| Strength (근력) | `{stats.get('strength', 0)}` |",
                f"| Fortitude (인내) | `{stats.get('fortitude', 0)}` |",
                f"| Agility (민첩) | `{stats.get('agility', 0)}` |",
                f"| Intelligence (지능) | `{stats.get('intelligence', 0)}` |",
                f"| Willpower (의지) | `{stats.get('willpower', 0)}` |",
                f"| Charisma (매력) | `{stats.get('charisma', 0)}` |",
                f"| Heavy Wep (중화기) | `{stats.get('heavy_wep', 0)}` |",
                f"| Medium Wep (중형무기) | `{stats.get('medium_wep', 0)}` |",
                f"| Light Wep (경화기) | `{stats.get('light_wep', 0)}` |",
                ""
            ])

        # 속성 (Attunements)
        active_attunements = {k: v for k, v in attunements.items() if v and v > 0}
        if active_attunements:
            lines.append("## ⚡ 속성 투자 (Attunements)")
            for name, val in active_attunements.items():
                lines.append(f"- **{name.capitalize()}**: `{val}`")
            lines.append("")

        # 실전 종합 전투 수치 (Combat Stats)
        # 실전 종합 전투 수치 (Combat Stats)
        spd = str(combat_stats.get("move_speed_pct", "100%"))
        if not spd.endswith("%"):
            spd = f"{spd}%"
        pve = str(combat_stats.get("pve_dmg_pct") or combat_stats.get("pve_monster_dmg_pct") or "0%")
        if not pve.endswith("%") and not pve.startswith("+") and not pve.startswith("-"):
            pve = f"+{pve}%"
        elif not pve.endswith("%"):
            pve = f"{pve}%"

        if combat_stats:
            lines.extend([
                "## 🩺 실전 종합 전투 수치 (Combat Stats)",
                "| Max HP (❤️ 체력) | Posture (🛡️ 자세) | Ether (💧 에테르) | Tempo (⚡ 템포) | Sanity (🧠 정신력) | Move Speed (👟 이속) | PvE Dmg vs Monsters (💀 몬스터 피해) |",
                "| :---: | :---: | :---: | :---: | :---: | :---: | :---: |",
                f"| `{combat_stats.get('hp', 'N/A')}` | `{combat_stats.get('posture', 'N/A')}` | `{combat_stats.get('ether', 'N/A')}` | `{combat_stats.get('tempo', 'N/A')}` | `{combat_stats.get('sanity', 'N/A')}` | `{spd}` | `{pve}` |",
                "",
                "> 💡 **이속(Move Speed)**: 중갑(Heavy Armor/Outfits) 착용 시 방어력 상승에 따른 장비 무게 페널티로 인게임에 음수(예: `-15.0%`)로 표기되는 정상 실측치입니다.",
                ""
            ])

        # 저항력 (Resistances - 10 Icons Mapping)
        if resistances:
            blunt = resistances.get('physical_blunt', 'N/A')
            slash = resistances.get('physical_slash', 'N/A')
            bleed = resistances.get('bleed') or resistances.get('physical_pierce', 'N/A')
            fire = resistances.get('fire', 'N/A')
            ice = resistances.get('ice', 'N/A')
            lightning = resistances.get('lightning', 'N/A')
            wind = resistances.get('wind', 'N/A')
            shadow = resistances.get('shadow', 'N/A')
            iron = resistances.get('iron', 'N/A')
            blood = resistances.get('blood', 'N/A')

            lines.extend([
                "## 🛡️ 방어 및 저항력 명세 (Resistances)",
                "| 물리 저항 (Physical) | 원소 저항 (Elemental) | 특수/혈액 저항 (Special & Blood) |",
                "| :--- | :--- | :--- |",
                f"| 🔨타격: `{blunt}`<br>🗡️베기: `{slash}`<br>🩸관통/출혈: `{bleed}` | 🔥화염: `{fire}`<br>❄️빙결: `{ice}`<br>⚡번개: `{lightning}`<br>💨바람: `{wind}` | 🌌암흑: `{shadow}`<br>⚙️철(Metal): `{iron}`<br>🩸혈액(Blood): `{blood}` |",
                ""
            ])

        # Shrine of Order
        shrine = build_data.get("shrine_of_order_path")
        if shrine:
            lines.extend([
                "## ⛩️ Shrine of Order 진행 경로",
                f"{shrine}",
                ""
            ])

        # 무기 & 장비
        if weapons:
            lines.append("## 🗡️ 추천 무기 (Weapons)")
            for w in weapons:
                if isinstance(w, str):
                    lines.append(f"- **{w}**")
                elif isinstance(w, dict):
                    w_name = w.get("name", "Unknown")
                    w_type = f" ({w.get('type')})" if w.get('type') and w.get('type') != 'Weapon' else ""
                    enchant = w.get("enchant", "None")
                    stars = w.get("stars", 0)
                    star_str = f" ⭐x{stars}" if stars else ""
                    lines.append(f"- **{w_name}**{w_type} — 인챈트: `{enchant}`{star_str}")
            lines.append("")

        if equipment:
            lines.append("## 🛡️ 주요 장비 (Equipment)")
            for eq in equipment:
                if isinstance(eq, str):
                    lines.append(f"- {eq}")
                elif isinstance(eq, dict):
                    eq_name = eq.get("name", "Unknown")
                    slot = eq.get("slot", "Slot")
                    pip = eq.get("pip_summary", "")
                    pip_str = f" ({pip})" if pip else ""
                    lines.append(f"- **[{slot}]** {eq_name}{pip_str}")
            lines.append("")

        # 핵심 탤런트
        if talents:
            lines.append("## ⭐ 주요 탤런트 (Talents)")
            core_talents = [t for t in talents if isinstance(t, dict) and t.get("is_core")]
            other_talents = [t for t in talents if not (isinstance(t, dict) and t.get("is_core"))]

            if core_talents:
                lines.append("### 🌟 필수 핵심 탤런트")
                for t in core_talents:
                    cat = f" `[{t.get('category')}]`" if t.get('category') else ""
                    lines.append(f"- **{t.get('name')}**{cat}")

            if other_talents:
                lines.append("### 📜 보조 및 추천 탤런트")
                for t in other_talents:
                    if isinstance(t, str):
                        lines.append(f"- {t}")
                    elif isinstance(t, dict):
                        cat = f" `[{t.get('category')}]`" if t.get('category') else ""
                        lines.append(f"- {t.get('name')}{cat}")
            lines.append("")

        # 만트라
        if mantras:
            lines.append("## 🔮 주문 목록 (Mantras)")
            for m in mantras:
                if isinstance(m, str):
                    lines.append(f"- **{m}**")
                elif isinstance(m, dict):
                    m_name = m.get("name", "Unknown")
                    att = f" ({m.get('attunement')})" if m.get('attunement') else ""
                    core_badge = " `[CORE]`" if m.get('is_core') else ""
                    mod = f" — 수정체: {m.get('modifications')}" if m.get('modifications') else ""
                    lines.append(f"- **{m_name}**{att}{core_badge}{mod}")
            lines.append("")

        # 주요 타겟 몬스터 및 보스 공략
        tms = build_data.get("target_mobs_and_strategy") or {}
        if isinstance(tms, dict) and tms:
            mobs = tms.get("target_mobs", [])
            strat = tms.get("mob_strategy", "")
            if mobs or strat:
                lines.append("## 🐉 주요 타겟 몬스터 및 보스 공략 (Target Mobs & Boss Strategy)")
                if mobs:
                    mobs_str = ", ".join(mobs) if isinstance(mobs, list) else str(mobs)
                    lines.append(f"**추천 사냥 대상**: `{mobs_str}`\n")
                if strat:
                    lines.append(f"{strat}\n")

        # 콤보 & 교전 가이드
        combo = build_data.get("combo_guide")
        if combo:
            lines.extend([
                "## 🥊 콤보 & 전투 운용 가이드",
                f"{combo}",
                ""
            ])

        # 100% 실측 원시 데이터 부록 (Raw Visual Ground Truth Appendix)
        lines.extend([
            "## 🔬 100% 실측 원시 데이터 (Raw Visual Ground Truth)",
            "> 본 섹션은 인게임 캐릭터 창(Stat Sheet)에서 OpenCV 고해상도 전처리 및 Vision AI가 픽셀 단위로 직접 추출한 무가공 실측 데이터입니다.",
            "",
            "| 실측 분류 | 세부 실측 데이터 항목 |",
            "| :--- | :--- |",
            f"| **캐릭터 기본 정보** | Power: `{build_data.get('power', 20)}` / Origin: `{build_data.get('origin', 'N/A')}` / Oath: `{build_data.get('oath', 'N/A')}` / Race/Aspect: `{build_data.get('race', 'N/A')}` |",
            f"| **4대 특성 (Traits)** | Vitality: `{traits.get('vitality', 0)}` / Erudition: `{traits.get('erudition', 0)}` / Proficiency: `{traits.get('proficiency', 0)}` / Songchant: `{traits.get('songchant', 0)}` |",
            f"| **6대 기본 스탯** | STR: `{stats.get('strength', 0)}` / FTD: `{stats.get('fortitude', 0)}` / AGL: `{stats.get('agility', 0)}` / INT: `{stats.get('intelligence', 0)}` / WLL: `{stats.get('willpower', 0)}` / CHA: `{stats.get('charisma', 0)}` |",
            f"| **무기/속성 수치** | LHT: `{stats.get('light_wep', 0)}` / MED: `{stats.get('medium_wep', 0)}` / HVY: `{stats.get('heavy_wep', 0)}` / Elements: `{active_attunements if active_attunements else 'Attunementless (0)'}` |",
            f"| **실전 전투 수치** | ❤️HP: `{combat_stats.get('hp', 'N/A')}` / 🛡️Posture: `{combat_stats.get('posture', 'N/A')}` / 💧Ether: `{combat_stats.get('ether', 'N/A')}` / ⚡Tempo: `{combat_stats.get('tempo', 'N/A')}` / 🧠Sanity: `{combat_stats.get('sanity', 'N/A')}` / 👟Speed: `{spd}` / 💀Monster Dmg: `{pve}` |",
            f"| **방어 저항력 (물리)** | 🔨타격(Blunt): `{blunt}` / 🗡️베기(Slash): `{slash}` / 🩸관통·출혈(Bleed): `{bleed}` |",
            f"| **방어 저항력 (원소·특수)** | 🔥화염: `{fire}` / ❄️빙결: `{ice}` / ⚡번개: `{lightning}` / 💨바람: `{wind}` / 🌌암흑: `{shadow}` / ⚙️철: `{iron}` / 🩸혈액: `{blood}` |",
            ""
        ])

        return "\n".join(lines)

    def classify_category(self, build_data: Dict[str, Any], url: str = "") -> str:
        """Deepwoken Fandom Wiki 스타일 5대 카테고리 자동 분류"""
        name = (build_data.get("build_summary", {}).get("build_name") or "").lower()
        b_type = (build_data.get("build_summary", {}).get("build_type") or "").lower()
        url_lower = url.lower()
        
        # 1. Bosses & Raids (보스 공략)
        if any(k in name or k in url_lower for k in ['boss', 'chaser', 'scion', 'ethiron', 'duke', 'ferryman', 'primadon', 'kaido', 'maestro', 'dread serpent']):
            return 'bosses'
        # 2. Attunements (속성 마법 지식)
        if any(k in name or k in url_lower for k in ['shadowcast', 'frostdraw', 'flamecharm', 'galebreath', 'thundercall', 'ironsing', 'bloodrend']) and ('wiki' in url_lower or 'guide' in b_type or 'attunement' in name):
            return 'attunements'
        # 3. Oaths (서약 가이드)
        if 'oath' in name or (any(k in name for k in ['jetstriker', 'starkindred', 'silentheart', 'blindseer', 'contractor', 'dawnwalker', 'linkstrider', 'arcwarder', 'voidwalker', 'saltchemist', 'bladeharper', 'fadethorn']) and 'wiki' in url_lower):
            return 'oaths'
        # 4. Weapons & Equipment (무기/장비)
        if any(k in name or k in url_lower for k in ['weapon', 'enchant', 'armor', 'outfit', 'bell', 'greatsword']) and ('wiki' in url_lower or 'guide' in b_type):
            return 'weapons'
        # 5. Default: Player Builds
        return 'builds'

    def rebuild_index(self):
        """지식 베이스 내 모든 문서를 분류별로 정리하여 INDEX.md 및 README.md 자동 생성"""
        categories = {
            'bosses': '👑 Bosses & Raids (보스 & 레이드 공략)',
            'attunements': '🔮 Attunements (속성 및 마법 지식)',
            'oaths': '📜 Oaths (서약 가이드)',
            'weapons': '⚔️ Weapons & Equipment (무기 및 장비)',
            'builds': '🎯 Player Builds (플레이어 PvP/PvE 빌드)'
        }
        lines = [
            '# 📖 Deepwoken AI 지식 포털 (Knowledge Portal)',
            '',
            '> 본 지식 베이스는 유튜브 영상 및 Fandom 위키, 공식 가이드로부터 AI가 자동 수집/구조화한 딥위큰 데이터베이스입니다.',
            '',
            '---',
            ''
        ]
        for cat_key, cat_title in categories.items():
            cat_folder = self.knowledge_base_dir / cat_key
            md_files = list(cat_folder.glob('*.md')) if cat_folder.exists() else []
            lines.append(f'## {cat_title} ({len(md_files)}개)')
            lines.append('')
            if not md_files:
                lines.append('*등록된 문서가 아직 없습니다.*')
                lines.append('')
                continue
            lines.append('| 문서명 / 빌드명 | 난이도 / 타입 | Oath / 속성 | 파일 링크 |')
            lines.append('| :--- | :--- | :--- | :--- |')
            for mf in sorted(md_files):
                jf = self.analysis_dir / cat_key / f'{mf.stem}.json'
                b_name = mf.stem
                b_type = 'Guide'
                oath_att = 'N/A'
                if jf.exists():
                    try:
                        data = json.loads(jf.read_text(encoding='utf-8'))
                        b_name = data.get('build_summary', {}).get('build_name') or mf.stem
                        b_type = data.get('build_summary', {}).get('build_type') or 'Guide'
                        oath = data.get('oath') or data.get('character_details', {}).get('oath') or ''
                        att_dict = data.get('attunements', {})
                        atts = [k for k, v in att_dict.items() if v and v > 0]
                        oath_att = f'{oath} / ' + (', '.join(atts) if atts else 'Attunementless')
                    except Exception:
                        pass
                rel_path = f'{cat_key}/{mf.name}'
                lines.append(f'| **{b_name[:35]}** | `{b_type}` | `{oath_att[:25]}` | [📄 문서 보기]({rel_path}) |')
            lines.append('')

        content = '\n'.join(lines)
        (self.knowledge_base_dir / 'INDEX.md').write_text(content, encoding='utf-8')
        (self.knowledge_base_dir / 'README.md').write_text(content, encoding='utf-8')

    def generate_slug(self, title: str, default_id: str) -> str:
        """빌드/문서 제목을 가독성 높은 영문/한글 슬러그 파일명으로 변환"""
        import re
        clean = re.sub(r'[^\w\s-]', '', title.lower()).strip()
        slug = re.sub(r'[-\s]+', '-', clean)[:45].strip('-')
        return slug if slug else default_id

    def process_and_save(self, raw_json: Dict[str, Any], video_id: str) -> Dict[str, Path]:
        """JSON 검증, 카테고리 분류, 가독성 높은 슬러그 파일명 저장 및 Markdown 변환/INDEX 갱신 일괄 실행"""
        self.validate(raw_json)
        sanitized = self.sanitize(raw_json)
        url = sanitized.get("video_meta", {}).get("url", "")
        b_name = sanitized.get("build_summary", {}).get("build_name") or sanitized.get("video_meta", {}).get("title") or video_id
        file_slug = self.generate_slug(b_name, video_id)

        category = self.classify_category(sanitized, url)
        target_a_dir = self.analysis_dir / category
        target_kb_dir = self.knowledge_base_dir / category
        target_a_dir.mkdir(parents=True, exist_ok=True)
        target_kb_dir.mkdir(parents=True, exist_ok=True)

        # JSON 저장 (가독성 높은 슬러그 파일명)
        json_path = target_a_dir / f"{file_slug}.json"
        json_path.write_text(json.dumps(sanitized, ensure_ascii=False, indent=2), encoding="utf-8")
        logger.info(f"Saved JSON analysis to: {json_path}")

        # Markdown 저장 (가독성 높은 슬러그 파일명)
        md_content = self.to_markdown(sanitized)
        md_path = target_kb_dir / f"{file_slug}.md"
        md_path.write_text(md_content, encoding="utf-8")
        logger.info(f"Saved Markdown knowledge to: {md_path}")

        # INDEX.md 자동 갱신
        try:
            self.rebuild_index()
        except Exception as e:
            logger.warning(f"Failed to rebuild index: {e}")

        return {
            "json_path": json_path,
            "md_path": md_path,
            "category": category,
            "file_slug": file_slug
        }
