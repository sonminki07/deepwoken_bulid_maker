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
            "build_name": bs.get("build_name", "Unnamed Build"),
            "build_type": bs.get("build_type", "PvE"),
            "difficulty": bs.get("difficulty", "Intermediate"),
            "creator_opinion": bs.get("creator_opinion", "No summary provided."),
            "strengths": bs.get("strengths", []),
            "weaknesses": bs.get("weaknesses", [])
        }

        # 3. stats & attunements 정규화
        stats_raw = sanitized.get("stats", {})
        att_raw = sanitized.get("attunements", {})
        if "stats_and_attunements" in sanitized:
            saa = sanitized["stats_and_attunements"]
            base = saa.get("base_stats", {})
            wep = saa.get("weapon_stats", {})
            stats_raw = {**base, **wep}
            att_raw = saa.get("attunements", {})

        sanitized["stats"] = stats_raw
        sanitized["attunements"] = att_raw

        # 4. character details 정규화
        cd = sanitized.get("character_details", {})
        if cd:
            sanitized["oath"] = cd.get("oath", sanitized.get("oath", "Oathless"))
            sanitized["race"] = cd.get("race", sanitized.get("race", "N/A"))
            sanitized["origin"] = cd.get("origin", sanitized.get("origin", "N/A"))
            sanitized["murmur"] = cd.get("murmur", sanitized.get("murmur", "N/A"))
            sanitized["resonance"] = cd.get("resonance_bell") or cd.get("resonance", sanitized.get("resonance", "N/A"))

        # 5. talents & mantras 정규화
        tm = sanitized.get("talents_and_mantras", {})
        if tm:
            if "core_talents" in tm and not sanitized.get("talents"):
                sanitized["talents"] = [{"name": t, "is_core": True} if isinstance(t, str) else t for t in tm["core_talents"]]
            if "mantras" in tm and not sanitized.get("mantras"):
                sanitized["mantras"] = tm["mantras"]

        # 6. equipment & weapons 정규화
        eq_raw = sanitized.get("equipment", [])
        if isinstance(eq_raw, dict):
            if "weapons" in eq_raw and not sanitized.get("weapons"):
                sanitized["weapons"] = eq_raw["weapons"]
            sanitized["equipment"] = eq_raw.get("armor", [])
        else:
            sanitized["equipment"] = eq_raw

        # 7. shrine & combo
        sop = sanitized.get("shrine_of_order_progression", {})
        if sop and not sanitized.get("shrine_of_order_path"):
            pre = sop.get("pre_shrine_stats", {})
            post = sop.get("post_shrine_priority", [])
            sanitized["shrine_of_order_path"] = f"**Pre-Shrine**: `{pre}`\n**Post-Shrine 우선순위**:\n" + "\n".join([f"- {p}" for p in post])

        cp = sanitized.get("combo_and_playstyle", {})
        if cp and not sanitized.get("combo_guide"):
            rot = cp.get("damage_rotation", "")
            tips = cp.get("tips", "")
            sanitized["combo_guide"] = f"**딜 사이클**:\n{rot}\n\n**운용 팁**:\n{tips}"

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
            f"> **패치 버전**: `{meta.get('estimated_patch', 'Unknown')}` | **타입**: `{build_type}` | **난이도**: `{difficulty}`",
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

        # 스탯 분배 표
        lines.extend([
            "## 📊 스탯 분배 (Stats)",
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
                    w_type = w.get("type", "")
                    enchant = w.get("enchant", "None")
                    stars = w.get("stars", 0)
                    star_str = f" ⭐x{stars}" if stars else ""
                    lines.append(f"- **{w_name}** ({w_type}) — 인챈트: `{enchant}`{star_str}")
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

        # 콤보 & 교전 가이드
        combo = build_data.get("combo_guide")
        if combo:
            lines.extend([
                "## 🥊 콤보 & 전투 운용 가이드",
                f"{combo}",
                ""
            ])

        return "\n".join(lines)

    def process_and_save(self, raw_json: Dict[str, Any], video_id: str) -> Dict[str, Path]:
        """JSON 검증, 보정, 저장 및 Markdown 변환/저장 일괄 실행"""
        self.validate(raw_json)
        sanitized = self.sanitize(raw_json)

        # JSON 저장
        json_path = self.analysis_dir / f"{video_id}.json"
        json_path.write_text(json.dumps(sanitized, ensure_ascii=False, indent=2), encoding="utf-8")
        logger.info(f"Saved JSON analysis to: {json_path}")

        # Markdown 저장
        md_content = self.to_markdown(sanitized)
        md_path = self.knowledge_base_dir / f"{video_id}.md"
        md_path.write_text(md_content, encoding="utf-8")
        logger.info(f"Saved Markdown knowledge to: {md_path}")

        return {
            "json_path": json_path,
            "md_path": md_path
        }
