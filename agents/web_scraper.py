import re
import logging
import hashlib
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
import urllib.request
import urllib.error
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

@dataclass
class ScrapedWebContent:
    url: str
    title: str
    doc_id: str
    meta_description: str
    cleaned_text: str
    tables_text: str
    headings: List[str] = field(default_factory=list)
    raw_html: str = ""

class WebScraperAgent:
    """Agent 1: 웹페이지 텍스트, 구조, 테이블 정밀 스크래퍼"""

    def __init__(self, user_agent: str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"):
        self.user_agent = user_agent

    def scrape(self, url: str, timeout: int = 15) -> ScrapedWebContent:
        """주어진 URL에서 HTML 또는 구글 닥스를 가져와 파싱 및 텍스트 정제"""
        logger.info(f"Scraping web page: {url}")
        
        # 구글 닥스(Google Docs) URL 자동 감지 및 텍스트 내보내기 변환
        import re
        gdoc_match = re.search(r'docs\.google\.com/document/d/([a-zA-Z0-9_\-]+)', url)
        if gdoc_match:
            doc_key = gdoc_match.group(1)
            export_url = f"https://docs.google.com/document/d/{doc_key}/export?format=txt"
            try:
                req = urllib.request.Request(export_url, headers={"User-Agent": self.user_agent})
                with urllib.request.urlopen(req, timeout=timeout) as resp:
                    raw_text = resp.read().decode("utf-8", errors="replace").lstrip("\ufeff")
                    
                first_line = raw_text.splitlines()[0] if raw_text.splitlines() else "Google Doc"
                return ScrapedWebContent(
                    url=url,
                    title=f"Google Docs: {first_line[:50]}",
                    doc_id=doc_key,
                    meta_description="Imported from Google Docs",
                    cleaned_text=raw_text,
                    tables_text="",
                    headings=[line.strip() for line in raw_text.splitlines() if line.strip() and len(line.strip()) < 40][:15],
                    raw_html=""
                )
            except Exception as e:
                logger.warning(f"Google Docs export failed ({e}), falling back to HTML scrape.")

        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": self.user_agent,
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.9,ko;q=0.8"
            }
        )

        try:
            with urllib.request.urlopen(req, timeout=timeout) as response:
                html = response.read().decode("utf-8", errors="replace")
        except urllib.error.HTTPError as e:
            raise RuntimeError(f"HTTP Error {e.code} while fetching {url}: {e.reason}")
        except Exception as e:
            raise RuntimeError(f"Failed to fetch {url}: {e}")

        soup = BeautifulSoup(html, "html.parser")

        # 불필요한 태그 제거
        for tag in soup(["script", "style", "nav", "footer", "header", "aside", "noscript", "svg"]):
            tag.decompose()

        # 메타데이터 추출
        title = soup.title.string.strip() if soup.title and soup.title.string else "Untitled Web Page"
        meta_desc = ""
        meta_tag = soup.find("meta", attrs={"name": "description"}) or soup.find("meta", attrs={"property": "og:description"})
        if meta_tag and meta_tag.get("content"):
            meta_desc = meta_tag["content"].strip()

        # 헤딩 태그 수집
        headings = [h.get_text(strip=True) for h in soup.find_all(["h1", "h2", "h3", "h4"]) if h.get_text(strip=True)]

        # 표(Table) 데이터 텍스트화
        tables_text_list = []
        for idx, table in enumerate(soup.find_all("table"), 1):
            rows = []
            for tr in table.find_all("tr"):
                cells = [td.get_text(strip=True) for td in tr.find_all(["td", "th"])]
                if cells:
                    rows.append(" | ".join(cells))
            if rows:
                tables_text_list.append(f"[Table {idx}]\n" + "\n".join(rows))

        tables_text = "\n\n".join(tables_text_list)

        # 본문 텍스트 정제
        text = soup.get_text(separator="\n", strip=True)
        # 연속된 빈 줄 제거
        cleaned_text = re.sub(r"\n{3,}", "\n\n", text)

        # URL 기반 유니크 ID 생성
        doc_id = "web_" + hashlib.md5(url.encode("utf-8")).hexdigest()[:12]

        return ScrapedWebContent(
            url=url,
            title=title,
            doc_id=doc_id,
            meta_description=meta_desc,
            cleaned_text=cleaned_text[:15000],  # 상위 15,000자
            tables_text=tables_text,
            headings=headings,
            raw_html=html[:50000]
        )
