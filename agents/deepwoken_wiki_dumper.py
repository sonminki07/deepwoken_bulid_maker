import os
import logging
import urllib.request
import re
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
    ("boon", "Boons", "긍정적특성 (전체)"),
    ("flaw", "Flaws", "결함/디버프 (전체)"),
    ("enemy", "Enemies", "몬스터/보스 (전체)"),
    ("location", "Locations", "지역/포인트 (전체)"),
    ("attack", "Attacks", "보스 공격 패턴 (전체)")
]

class DeepwokenWikiDumper:
    """deepwoken.co/wiki 를 크롤링할 때 억지로 JSON으로 파싱하지 않고, 단순하고 정확하게 원본 텍스트만 긁어옵니다."""

    def __init__(self, output_dir: str = "data/wiki", kb_dir: str = "data/knowledge_base/wiki"):
        self.output_dir = Path(output_dir)
        self.kb_dir = Path(kb_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.kb_dir.mkdir(parents=True, exist_ok=True)
        self.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"

    def fetch_category_text(self, cat_slug: str) -> str:
        """단순 무식하게 HTML 본문 텍스트만 추출합니다 (Nuxt 파싱 시도 삭제)."""
        url = f"https://deepwoken.co/wiki/{cat_slug}"
        req = urllib.request.Request(url, headers={"User-Agent": self.user_agent})
        
        try:
            with urllib.request.urlopen(req, timeout=20) as response:
                html = response.read().decode("utf-8", errors="ignore")
        except Exception as e:
            logger.error(f"Failed to fetch {url}: {e}")
            return ""

        soup = BeautifulSoup(html, "html.parser")
        
        for tag in soup(["script", "style", "nav", "footer", "header", "aside", "noscript", "svg"]):
            tag.decompose()
            
        main_content = soup.find("main") or soup.find("div", class_="container") or soup.body
        if not main_content:
            text = soup.get_text(separator="\n", strip=True)
        else:
            text = main_content.get_text(separator="\n", strip=True)
            
        cleaned_text = re.sub(r"\n{3,}", "\n\n", text)
        return cleaned_text

    def dump_all(self) -> Dict[str, int]:
        """어설픈 JSON 분석 없이 텍스트(마크다운)만 정확히 스크랩하여 저장합니다."""
        console = Console()
        console.print("[bold cyan]🔥 Deepwoken Wiki 단순 텍스트 스크랩 시작...[/bold cyan]\n")

        summary = {}

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            console=console
        ) as progress:
            task = progress.add_task("[yellow]전체 위키 텍스트 스크랩 중..", total=len(WIKI_CATEGORIES))

            for slug, eng_name, kor_desc in WIKI_CATEGORIES:
                progress.update(task, description=f"[cyan]수집 중:[/ ] {eng_name}")
                text_content = self.fetch_category_text(slug)
                
                md_lines = [
                    f"# 📜 Deepwoken Wiki: {eng_name} ({kor_desc})",
                    f"> **출처**: https://deepwoken.co/wiki/{slug}",
                    "",
                    "---",
                    "",
                    text_content
                ]
                
                md_path = self.kb_dir / f"{slug}.md"
                md_path.write_text("\n".join(md_lines), encoding="utf-8")
                
                summary[slug] = len(text_content)
                progress.advance(task)

        console.print("[bold green]✅ 텍스트 스크랩 완료! (어설픈 JSON 파싱 삭제)[/bold green]")
        return summary