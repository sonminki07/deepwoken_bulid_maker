import os
import json
import logging
import urllib.request
from pathlib import Path
from typing import Dict, Any, List
from bs4 import BeautifulSoup
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn

logger = logging.getLogger(__name__)

WIKI_CATEGORIES = [
    ("talent", "Talents", "탤런트 (전체)"),
    ("weapon", "Weapons", "무기 (전체)"),
    ("mantra", "Mantras", "만트라/스킬 (전체)"),
    ("equipment", "Equipment", "장비/방어구 (전체)"),
    ("outfit", "Outfits", "의상/아웃핏 (전체)"),
    ("enchantment", "Enchantments", "인챈트 (전체)"),
    ("oath", "Oaths", "오스/서약 (전체)"),
    ("attunement", "Attunements", "속성 (전체)"),
    ("aspect", "Races", "종족/특성 (전체)"),
    ("boon", "Boons", "분/특전 (전체)"),
    ("flaw", "Flaws", "결함/디버프 (전체)"),
    ("enemy", "Enemies", "몬스터/보스 (전체)"),
    ("location", "Locations", "지역/포인트 (전체)"),
    ("attack", "Attacks", "보스 공격 패턴 (전체)")
]

class DeepwokenWikiDumper:
    """deepwoken.co/wiki 의 14개 전 카테고리를 Nuxt payload로부터 100% 전수 덤프하는 고속 크롤러"""

    def __init__(self, output_dir: str = "data/wiki", kb_dir: str = "data/knowledge_base/wiki"):
        self.output_dir = Path(output_dir)
        self.kb_dir = Path(kb_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.kb_dir.mkdir(parents=True, exist_ok=True)
        self.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"

    def fetch_category(self, cat_slug: str) -> List[Dict[str, Any]]:
        """단일 카테고리 Nuxt 데이터 추출 및 파싱"""
        url = f"https://deepwoken.co/wiki/{cat_slug}"
        req = urllib.request.Request(url, headers={"User-Agent": self.user_agent})
        
        try:
            with urllib.request.urlopen(req, timeout=20) as response:
                html = response.read().decode("utf-8", errors="replace")
        except Exception as e:
            logger.error(f"Failed to fetch {url}: {e}")
            return []

        soup = BeautifulSoup(html, "html.parser")
        script = soup.find("script", id="__NUXT_DATA__")
        if not script or not script.string:
            logger.warning(f"No __NUXT_DATA__ found for {cat_slug}")
            return []

        raw = json.loads(script.string)
        
        def resolve(val, depth=0):
            if depth > 4:
                return val
            if isinstance(val, int) and 0 <= val < len(raw):
                target = raw[val]
                if isinstance(target, (str, int, float, bool)) or target is None:
                    return target
                elif isinstance(target, dict):
                    return {k: resolve(v, depth + 1) for k, v in target.items()}
                elif isinstance(target, list):
                    return [resolve(x, depth + 1) for x in target]
                return target
            return val

        items = []
        for elem in raw:
            if isinstance(elem, dict) and "name" in elem:
                name_val = resolve(elem["name"])
                if isinstance(name_val, str) and name_val.strip():
                    item_dict = {
                        "name": name_val.strip(),
                        "category": cat_slug,
                        "description": resolve(elem.get("description", "")),
                        "rarity": resolve(elem.get("rarity", "")),
                        "requirements": resolve(elem.get("requirements", {})),
                        "stats": resolve(elem.get("stats", {})),
                        "additionalInfo": resolve(elem.get("additionalInfo", "")),
                    }
                    items.append(item_dict)

        # 중복 제거 (name 기준)
        unique_items = {}
        for it in items:
            if it["name"] not in unique_items:
                unique_items[it["name"]] = it

        return list(unique_items.values())

    def dump_all(self) -> Dict[str, int]:
        """14개 전 카테고리 크롤링 및 JSON / Markdown 저장"""
        console = Console()
        console.print("[bold cyan]🚀 Deepwoken Wiki 전 카테고리 데이터베이스 전수 수집 시작...[/bold cyan]\n")

        summary = {}
        total_items_count = 0

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            console=console
        ) as progress:
            task = progress.add_task("[yellow]전체 위키 카테고리 수집 중...", total=len(WIKI_CATEGORIES))

            for slug, eng_name, kor_desc in WIKI_CATEGORIES:
                progress.update(task, description=f"[cyan]수집 중:[/] {eng_name} ({kor_desc})")
                items = self.fetch_category(slug)
                summary[slug] = len(items)
                total_items_count += len(items)

                # JSON 저장
                json_path = self.output_dir / f"{slug}.json"
                json_path.write_text(json.dumps(items, ensure_ascii=False, indent=2), encoding="utf-8")

                # Markdown 지식 파일 저장
                md_lines = [
                    f"# 📚 Deepwoken Wiki: {eng_name} ({kor_desc})",
                    f"> **총 항목 수**: {len(items)}개 | **출처**: https://deepwoken.co/wiki/{slug}",
                    "",
                    "---",
                    ""
                ]

                for it in items:
                    req_str = ""
                    if it.get("requirements"):
                        req_str = f" | **요구조건**: `{it.get('requirements')}`"
                    rarity_str = f" `[{it.get('rarity')}]`" if it.get("rarity") else ""
                    
                    md_lines.extend([
                        f"### {it['name']}{rarity_str}",
                        f"- **설명**: {it.get('description') or '설명 없음'}{req_str}",
                    ])
                    if it.get("additionalInfo"):
                        md_lines.append(f"- **추가 정보**: {it.get('additionalInfo')}")
                    md_lines.append("")

                md_path = self.kb_dir / f"{slug}.md"
                md_path.write_text("\n".join(md_lines), encoding="utf-8")

                progress.advance(task)

        console.print(f"\n[bold green]✅ 전수 수집 완료! 총 {total_items_count}개의 위키 데이터베이스가 구축되었습니다.[/bold green]")
        return summary
