import os
import logging
from typing import Optional, List, Dict, Any
from google import genai
from google.genai import types
from rich.console import Console
from rich.markdown import Markdown
from rich.prompt import Prompt
from duckduckgo_search import DDGS

from agents.knowledge_builder import KnowledgeBuilder
from agents.key_manager import global_key_manager

logger = logging.getLogger(__name__)

ADVISOR_SYSTEM_PROMPT = """당신은 세계 최고의 Deepwoken 전문 AI 코치이자 데이터 분석가입니다.
사용자의 질문에 대해 로컬 빌드 데이터베이스(RAG)와 실시간 웹 검색(Wiki, Reddit) 결과를 종합하여 심층적이고 전문적인 분석 보고서를 제공합니다.

[답변 작성 가이드라인]
1. **정확한 수치와 팩트 기반**: 스탯 분배(Pre-Shrine, Post-Shrine), 필수 탤런트, 만트라(Mantra), 추천 무기/아웃핏/인챈트, 콤보 메커니즘을 구체적인 수치와 함께 상세히 설명하세요.
2. **원리와 메커니즘 심층 분석**: 왜 이 빌드가 강력한지, 어떤 특성/패시브가 상호작용(시너지)을 일으키는지 상세한 작동 원리를 단계별로 정리하세요.
3. **구조화된 마크다운 보고서 형식**:
   - ⚔️ **1. 핵심 작동 원리 및 메커니즘**
   - 📊 **2. 상세 스탯 분배 및 육성 (Pre/Post Shrine of Order)**
   - 🛡️ **3. 추천 장비, 아웃핏 및 최적 인챈트 (Equipment & Outfit)**
   - 🌟 **4. 핵심 탤런트(Talents) 및 주요 만트라(Mantras)**
   - 🥊 **5. 실전 운용법, 콤보 팁 및 주의점**
4. 출처 링크나 정보가 있으면 친절하게 명시하세요.
"""

class BuildAdvisor:
    """5단계: RAG + 실시간 웹 검색(DDGS) 하이브리드 Deepwoken AI 빌드 어드바이저"""

    def __init__(
        self,
        api_key: Optional[str] = None,
        model_name: str = "gemini-3.6-flash",
        db_path: str = "data/chromadb",
        collection_name: str = "deepwoken_builds",
        top_k: int = 4
    ):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self.model_name = model_name
        self.top_k = top_k
        self.kb = KnowledgeBuilder(db_path=db_path, collection_name=collection_name, api_key=self.api_key, use_gemini_embedding=False)

    def search_web(self, query: str, max_results: int = 4) -> str:
        """실시간 웹 검색 (Deepwoken Wiki, Reddit, 빌더 등)"""
        search_query = f"Deepwoken {query}"
        try:
            with DDGS() as ddgs:
                results = list(ddgs.text(search_query, max_results=max_results))
                if not results:
                    return ""
                snippets = []
                for r in results:
                    snippets.append(f"- **{r.get('title')}**: {r.get('body')} (출처: {r.get('href')})")
                return "\n".join(snippets)
        except Exception as e:
            logger.warning(f"Web search error: {e}")
            return ""

    def ask(self, user_query: str) -> str:
        """RAG 검색 + 실시간 웹 검색 + Gemini AI 통합 답변 생성"""
        # 1. RAG 지식 검색
        rag_context = ""
        try:
            search_results = self.kb.query(query_text=user_query, n_results=self.top_k)
            if search_results:
                blocks = []
                for idx, res in enumerate(search_results, 1):
                    meta = res["metadata"]
                    blocks.append(
                        f"[로컬 인덱스 빌드 {idx}: {meta.get('build_name', 'Unknown')}]\n"
                        f"타입: {meta.get('build_type')} | Oath: {meta.get('oath')} | 출처: {meta.get('url')}\n"
                        f"{res['document']}\n"
                    )
                rag_context = "\n\n".join(blocks)
        except Exception as e:
            logger.warning(f"RAG search warning: {e}")

        # 2. 실시간 웹 검색 (Wiki / Reddit)
        web_context = self.search_web(user_query, max_results=4)

        # 3. 통합 프롬프트 생성
        prompt = (
            f"[사용자 질문]\n{user_query}\n\n"
            f"[참고 1: 로컬 저장소 분석 빌드 데이터 (RAG)]\n"
            f"{rag_context if rag_context else '로컬에 직접 매칭된 빌드 없음'}\n\n"
            f"[참고 2: 실시간 웹/위키 검색 결과]\n"
            f"{web_context if web_context else '웹 검색 결과 없음'}\n\n"
            f"위 참고 자료들을 종합하여 질문에 대해 수치, 탤런트, 메커니즘, 장비/아웃핏 추천이 포함된 상세하고 전문적인 분석 보고서 마크다운을 작성하세요."
        )

        def _call_model(client: genai.Client) -> str:
            response = client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=ADVISOR_SYSTEM_PROMPT,
                    temperature=0.2
                )
            )
            return response.text

        try:
            return global_key_manager.execute_with_failover(_call_model)
        except Exception as e:
            logger.error(f"Advisor generation error: {e}")
            return f"⚠️ 답변 생성 중 오류가 발생했습니다: {e}"

    def answer_query(self, user_query: str) -> str:
        return self.ask(user_query)

    def interactive_cli(self):
        console = Console()
        console.print("[bold cyan]════════════════════════════════════════════════════[/bold cyan]")
        console.print("[bold green]⚔️ Deepwoken AI Search-Augmented Advisor 가동 완료[/bold green]")
        console.print("[dim]종료: 'exit' 또는 'q'[/dim]")
        console.print("[bold cyan]════════════════════════════════════════════════════[/bold cyan]\n")

        while True:
            try:
                user_input = Prompt.ask("[bold yellow]질문 입력[/bold yellow]")
                if not user_input or user_input.strip().lower() in ["exit", "quit", "q"]:
                    break
                with console.status("[bold blue]RAG 지식 검색 + 실시간 웹 검색 + AI 분석 중...[/bold blue]"):
                    answer = self.ask(user_input.strip())
                console.print(Markdown(answer))
            except Exception as e:
                console.print(f"[bold red]오류:[/bold red] {e}")

DeepwokenBuildAdvisor = BuildAdvisor
