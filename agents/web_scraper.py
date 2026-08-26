import re
import json
import logging
import hashlib
import urllib.request
import urllib.error
import urllib.parse
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
from bs4 import BeautifulSoup
from duckduckgo_search import DDGS

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

    def __init__(self, user_agent: str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36", max_depth: int = 2, max_sub_links: int = 7):
        self.user_agent = user_agent
        self.max_depth = max_depth
        self.max_sub_links = max_sub_links

        # 1차: URL 패턴 블랙리스트 (위키 네비게이션, 편집, 히스토리 차단)
        self.blacklist_pattern = re.compile(
            r"(action=history|action=edit|Special:|File:|Talk:|User:|Category:|Template:|Help:|diff=|oldid=|#|signin|login|facebook|twitter|discord|youtube|reddit|instagram)",
            re.IGNORECASE
        )

        # 2차: 텍스트 제외 블랙리스트
        self.noise_texts = {
            "home", "main page", "recent changes", "community", "saved", "history", "edit",
            "donate", "terms of use", "privacy policy", "explore", "random page", "view source",
            "log in", "sign up", "fandom", "contact", "about"
        }

        # 3차: 딥위큰 게임 전문 용어 화이트리스트 (우선순위 가중치)
        self.game_keywords = [
            "talent", "mantra", "oath", "attunement", "weapon", "shrine", "boss", "bell",
            "enchant", "armor", "outfit", "build", "stats", "quest", "progression", "shadowcast",
            "flamecharm", "frostdraw", "galebreath", "thundercall", "ironsing", "bloodrend",
            "layer 2", "chaser", "scion", "duke", "ferryman", "maestro", "murmur"
        ]

    def _filter_and_rank_sub_links(self, soup: BeautifulSoup, base_url: str) -> List[str]:
        """본문 내 하위 링크 중 3중 필터를 통과한 최상위 딥위큰 연관 링크 선별"""
        parsed_base = urllib.parse.urlparse(base_url)
        base_domain = parsed_base.netloc
        base_path_prefix = "/".join(parsed_base.path.split("/")[:-1])

        candidates = []
        seen_urls = {base_url}

        for a_tag in soup.find_all("a", href=True):
            href = a_tag.get("href", "").strip()
            text = a_tag.get_text(strip=True).lower()

            if not href or href.startswith(("#", "javascript:", "mailto:")):
                continue

            # 절대 URL 변환
            full_url = urllib.parse.urljoin(base_url, href)
            parsed_full = urllib.parse.urlparse(full_url)

            # 도메인 일치 검사 (같은 위키/사이트 내의 문서만)
            if parsed_full.netloc != base_domain:
                continue

            # 블랙리스트 URL 검사
            if self.blacklist_pattern.search(full_url):
                continue

            # 블랙리스트 텍스트 검사
            if text in self.noise_texts or len(text) < 2:
                continue

            # 중복 검사
            clean_full_url = full_url.split("#")[0].split("?")[0]
            if clean_full_url in seen_urls:
                continue
            seen_urls.add(clean_full_url)

            # 점수 계산 (화이트리스트 매칭)
            score = 0
            url_lower = clean_full_url.lower()
            for kw in self.game_keywords:
                if kw in text:
                    score += 3
                if kw in url_lower:
                    score += 2

            if score > 0 or "/wiki/" in url_lower:
                candidates.append((score, clean_full_url, text))

        # 점수 높은 순으로 정렬 후 상위 링크만 반환
        candidates.sort(key=lambda x: x[0], reverse=True)
        top_links = [item[1] for item in candidates[:self.max_sub_links]]
        logger.info(f"🔗 [Depth 2] Found {len(top_links)} relevant sub-links to crawl: {top_links}")
        return top_links

    def _scrape_single_sub_page(self, sub_url: str, timeout: int = 8) -> Optional[str]:
        """Depth 2: 하위 페이지 1개의 본문 및 표 데이터 고속 수집"""
        try:
            req = urllib.request.Request(
                sub_url,
                headers={"User-Agent": self.user_agent, "Accept": "text/html"}
            )
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                sub_html = resp.read().decode("utf-8", errors="replace")

            sub_soup = BeautifulSoup(sub_html, "html.parser")
            for tag in sub_soup(["script", "style", "nav", "footer", "header", "aside", "noscript", "svg"]):
                tag.decompose()

            sub_title = sub_soup.title.string.strip() if sub_soup.title and sub_soup.title.string else sub_url.split("/")[-1]
            sub_text = re.sub(r"\n{3,}", "\n\n", sub_soup.get_text(separator="\n", strip=True))

            return f"\n\n### 📖 [하위 상세 문서: {sub_title}]\n- URL: {sub_url}\n{sub_text[:3500]}"
        except Exception as e:
            logger.warning(f"Failed to scrape sub-page {sub_url}: {e}")
            return None

    def _scrape_fandom_api(self, url: str) -> Optional[ScrapedWebContent]:
        """Fandom/MediaWiki 위키 API를 사용하여 403 차단 없이 초고속 정밀 데이터 + Depth 2 하위 링크 수집"""
        try:
            parsed = urllib.parse.urlparse(url)
            domain = parsed.netloc
            page_name = parsed.path.split("/wiki/")[-1]
            if not page_name:
                return None

            api_url = f"https://{domain}/api.php?action=parse&page={page_name}&format=json&prop=text|links"
            req = urllib.request.Request(api_url, headers={"User-Agent": "Mozilla/5.0 (DeepwokenBuildAnalyzer/2.0)"})
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read().decode("utf-8"))

            parse_data = data.get("parse")
            if not parse_data:
                return None

            title = parse_data.get("title", page_name)
            raw_html = parse_data.get("text", {}).get("*", "")
            raw_links = [l["*"] for l in parse_data.get("links", []) if l.get("ns") == 0]

            soup = BeautifulSoup(raw_html, "html.parser")
            for tag in soup(["script", "style", "nav", "footer", "header", "aside", "noscript", "svg"]):
                tag.decompose()

            # 표(Table) 추출
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

            # 본문 정제
            text = soup.get_text(separator="\n", strip=True)
            cleaned_text = re.sub(r"\n{3,}", "\n\n", text)[:15000]

            # Depth 2: 하위 연관 위키 문서 선별 수집
            if self.max_depth >= 2 and raw_links:
                candidates = []
                for link_title in raw_links:
                    l_lower = link_title.lower()
                    if l_lower in self.noise_texts or self.blacklist_pattern.search(link_title):
                        continue
                    score = 0
                    for kw in self.game_keywords:
                        if kw in l_lower:
                            score += 3
                    if score > 0:
                        candidates.append((score, link_title))

                candidates.sort(key=lambda x: x[0], reverse=True)
                top_sub_pages = [c[1] for c in candidates[:self.max_sub_links]]

                sub_docs = []
                for sub_title in top_sub_pages:
                    try:
                        sub_api = f"https://{domain}/api.php?action=parse&page={urllib.parse.quote(sub_title)}&format=json&prop=text"
                        s_req = urllib.request.Request(sub_api, headers={"User-Agent": "Mozilla/5.0 (DeepwokenBuildAnalyzer/2.0)"})
                        with urllib.request.urlopen(s_req, timeout=6) as s_resp:
                            s_data = json.loads(s_resp.read().decode("utf-8"))
                        s_html = s_data.get("parse", {}).get("text", {}).get("*", "")
                        if s_html:
                            s_soup = BeautifulSoup(s_html, "html.parser")
                            for tag in s_soup(["script", "style", "nav", "footer", "aside"]):
                                tag.decompose()
                            s_text = re.sub(r"\n{3,}", "\n\n", s_soup.get_text(separator="\n", strip=True))[:3000]
                            sub_docs.append(f"\n\n### 📖 [하위 연관 위키: {sub_title}]\n{s_text}")
                    except Exception as ex:
                        logger.warning(f"Sub-wiki fetch failed for {sub_title}: {ex}")

                if sub_docs:
                    cleaned_text += "\n\n" + "="*50 + "\n📚 [심층 분석 연관 하위 위키 문서 모음]\n" + "".join(sub_docs)

            doc_id = "web_" + hashlib.md5(url.encode("utf-8")).hexdigest()[:12]
            headings = [h.get_text(strip=True) for h in soup.find_all(["h1", "h2", "h3", "h4"]) if h.get_text(strip=True)]

            return ScrapedWebContent(
                url=url,
                title=f"Deepwoken Wiki: {title}",
                doc_id=doc_id,
                meta_description=f"Official Fandom Wiki document for {title}",
                cleaned_text=cleaned_text[:30000],
                tables_text=tables_text,
                headings=headings,
                raw_html=raw_html[:50000]
            )
        except Exception as e:
            logger.warning(f"Fandom API scrape failed: {e}")
            return None

    def scrape(self, url: str, timeout: int = 15) -> ScrapedWebContent:
        """주어진 URL에서 HTML 또는 구글 닥스를 가져와 파싱 및 텍스트 정제 (Depth 2 재귀 수집)"""
        logger.info(f"Scraping web page: {url}")
        
        # Case 0: Fandom 위키인 경우 전용 초고속 API 엔진 사용
        if "fandom.com/wiki/" in url.lower():
            fandom_result = self._scrape_fandom_api(url)
            if fandom_result:
                return fandom_result
        
        # 구글 닥스(Google Docs) URL 자동 감지 및 텍스트 내보내기 변환
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

        html = ""
        try:
            with urllib.request.urlopen(req, timeout=timeout) as response:
                html = response.read().decode("utf-8", errors="replace")
        except Exception as e:
            logger.warning(f"Direct fetch failed ({e}) for {url}. Falling back to Search Grounding...")
            slug = urllib.parse.unquote(url.split("/")[-1])
            search_query = f"Deepwoken {slug} guide wiki details"
            fallback_texts = []
            title = f"Deepwoken Guide: {slug}"
            try:
                with DDGS() as ddgs:
                    results = list(ddgs.text(search_query, max_results=5))
                    for r in results:
                        fallback_texts.append(f"### {r.get('title')}\n{r.get('body')}")
            except Exception as se:
                logger.error(f"Search fallback also failed: {se}")

            if fallback_texts:
                cleaned_text = "\n\n".join(fallback_texts)
                doc_id = "web_" + hashlib.md5(url.encode("utf-8")).hexdigest()[:12]
                return ScrapedWebContent(
                    url=url,
                    title=title,
                    doc_id=doc_id,
                    meta_description=f"Auto-extracted guide for {slug}",
                    cleaned_text=cleaned_text,
                    tables_text="",
                    headings=[slug],
                    raw_html=""
                )
            else:
                raise RuntimeError(f"웹페이지 접근 실패 및 검색 대체 불가: {e}")

        soup = BeautifulSoup(html, "html.parser")

        # 1단계: 본문 내 하위 연관 링크 추출 (태그 제거 전 수행)
        sub_links = []
        if self.max_depth >= 2:
            sub_links = self._filter_and_rank_sub_links(soup, url)

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
        cleaned_text = re.sub(r"\n{3,}", "\n\n", text)[:15000]

        # 2단계: Depth 2 하위 링크 심층 수집 및 본문에 병합
        if sub_links:
            import time
            sub_contents = []
            for s_url in sub_links:
                sub_data = self._scrape_single_sub_page(s_url)
                if sub_data:
                    sub_contents.append(sub_data)
                time.sleep(0.15)  # 서버 부하 방지용 짧은 휴식

            if sub_contents:
                cleaned_text += "\n\n" + "="*50 + "\n📚 [심층 분석 연관 하위 위키 문서 모음]\n" + "".join(sub_contents)

        # URL 기반 유니크 ID 생성
        doc_id = "web_" + hashlib.md5(url.encode("utf-8")).hexdigest()[:12]

        return ScrapedWebContent(
            url=url,
            title=title,
            doc_id=doc_id,
            meta_description=meta_desc,
            cleaned_text=cleaned_text[:30000],  # 상위 30,000자
            tables_text=tables_text,
            headings=headings,
            raw_html=html[:50000]
        )
