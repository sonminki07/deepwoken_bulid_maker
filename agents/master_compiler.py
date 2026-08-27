import json
import logging
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)

def compile_master_notebooklm_source(project_dir: Optional[Path] = None) -> Path:
    """모든 검증된 빌드, 웹 문서, 위키 데이터를 하나의 마스터 NotebookLM 소스 파일로 병합 및 재생성합니다."""
    if project_dir is None:
        project_dir = Path(__file__).resolve().parent.parent

    data_dir = project_dir / "data"
    kb_dir = data_dir / "knowledge_base"
    kb_builds_dir = kb_dir / "builds"
    kb_web_dir = kb_dir / "web_docs"

    lines = []
    lines.append("# 📚 Deepwoken Ultimate Master Knowledge Base (NotebookLM 통합 소스)")
    lines.append("> 본 문서는 Roblox Deepwoken의 공식 인게임 룰, 질서의 성소(Shrine of Order) 공식, 그리고 유튜브 및 위키에서 수집/분석된 모든 실전 캐릭터 빌드와 몬스터 만트라/가이드 데이터를 100% 통합한 단일 마스터 지식 소스입니다.\n")

    # 1. 질서의 성소 & 종족 기본 룰
    lines.append("## 🏛️ 제1장: 종족 기본 스탯 및 질서의 성소 (Shrine of Order) 공식 룰")
    lines.append("""
### 1. 12대 종족 고유 기본 스탯 (Innate Racial Starting Stats)
- **Canor**: Strength +3, Charisma +2
- **Vesperian**: Fortitude +3, Willpower +2
- **Capra**: Intelligence +3, Willpower +2
- **Chrysid**: Charisma +3, Agility +2
- **Felinor**: Agility +3, Charisma +2
- **Gremor**: Fortitude +3, Strength +2
- **Adret**: Charisma +3, Willpower +2
- **Khan**: Strength +2, Agility +2
- **Etrean**: Intelligence +3, Agility +2
- **Celtor**: Intelligence +2, Charisma +2
- **Tiran**: Agility +3, Willpower +2
- **Castellan**: Intelligence +2, Willpower +2

### 2. 질서의 성소 (Shrine of Order) 핵심 메커니즘
1. **투자 포인트 균등 분배**: 수동 투자한 능력치(포인트 >= 1)들을 평균치로 맞추어 분배합니다. (단일 능력치 최대 삭감폭: -25pt)
2. **종족 기본치 보존**: 종족 고유 스탯(예: Canor Str 3, Cha 2)은 성소로 깎이지 않습니다.
3. **사원 전(Pre-Shrine) 탤런트 영구 보존**: 성소 전에 획득한 상위 탤런트(Reinforced Armor, Collapsed Lung, Million Ton Piercer, Showstopper 등)는 성소 후 스탯이 깎여도 영구히 100% 활성 상태를 유지합니다.
4. **만렙 순수 투자 한도**: 플레이어가 직접 찍을 수 있는 총 투자 포인트는 **327 포인트**입니다.
""")

    # 2. 모든 실전 유튜브 빌드 목록 병합
    lines.append("## ⚔️ 제2장: 유튜브 검증 실전 캐릭터 빌드 데이터베이스 (전수 집계)")
    build_count = 0
    if kb_builds_dir.exists():
        for md_file in sorted(kb_builds_dir.glob("*.md")):
            try:
                content = md_file.read_text(encoding="utf-8", errors="ignore").strip()
                if content:
                    lines.append(f"\n---\n\n### 🛡️ [빌드 {build_count+1}] {md_file.stem}\n")
                    lines.append(content)
                    build_count += 1
            except Exception as e:
                logger.warning(f"Error reading build md {md_file}: {e}")

    # 3. 추가 분석된 웹 및 위키 문서 병합 (Monster Mantras 등)
    web_count = 0
    if kb_web_dir.exists():
        lines.append("\n\n## 📖 제3장: 웹 & 위키 추가 분석 문서 및 시스템 가이드")
        for doc_file in sorted(kb_web_dir.glob("*.*")):
            try:
                content = doc_file.read_text(encoding="utf-8", errors="ignore").strip()
                if content:
                    lines.append(f"\n---\n\n### 🌐 [웹/위키 문서 {web_count+1}] {doc_file.stem}\n")
                    lines.append(content)
                    web_count += 1
            except Exception as e:
                logger.warning(f"Error reading web doc {doc_file}: {e}")

    # 4. 유저 뱅크 인벤토리 및 보유 인챈트 데이터 병합
    kb_user_dir = kb_dir / "user_inventory"
    if kb_user_dir.exists():
        lines.append("\n\n## 🎒 제4장: 유저 실제 인게임 뱅크 인벤토리 및 보유 인챈트 명세서")
        for u_file in sorted(kb_user_dir.glob("*.md")):
            try:
                content = u_file.read_text(encoding="utf-8", errors="ignore").strip()
                if content:
                    lines.append(f"\n---\n\n{content}\n")
            except Exception as e:
                logger.warning(f"Error reading user inv {u_file}: {e}")

    master_text = "\n".join(lines)
    
    out_md = data_dir / "Deepwoken_Master_NotebookLM_Source.md"
    out_txt = data_dir / "Deepwoken_Master_NotebookLM_Source.txt"
    
    out_md.write_text(master_text, encoding="utf-8")
    out_txt.write_text(master_text, encoding="utf-8")
    
    logger.info(f"Master NotebookLM source re-compiled with {build_count} builds and {web_count} web docs.")
    return out_txt

if __name__ == "__main__":
    out = compile_master_notebooklm_source()
    print("Master NotebookLM Source compiled successfully at:", out)