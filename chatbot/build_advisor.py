import os
import logging
from typing import Optional, List, Dict, Any
import google.generativeai as genai
from rich.console import Console
from rich.markdown import Markdown
from rich.prompt import Prompt

from agents.knowledge_builder import KnowledgeBuilder

logger = logging.getLogger(__name__)

ADVISOR_SYSTEM_PROMPT = """당신은 Deepwoken 전문가이자 AI 빌드 어드바이저(Build Advisor)입니다.
사용자가 원하는 플레이 스타일, 속성, PvP/PvE 선호도, 스탯 요구사항에 맞춰 데이터베이스에서 검색된 빌드 지식을 바탕으로 가장 적합한 빌드를 추천하고 운용법을 조언합니다.

[답변 원칙]
1. 반드시 제공된 [참고 빌드 지식]의 정보를 우선적으로 인용하여 답변하세요.
2. 각 빌드의 핵심 스탯, Oath, 필수 탤런트, 주요 만트라, 콤보 팁을 일목요연하게 정리해 주세요.
3. 사용자의 조건(초보자용, 고인물용, 특정 무기 등)에 따라 장단점을 비교해 주세요.
4. 출처 영상 URL이 있는 경우 출처를 명시해 주세요.
5. 검색된 지식에 없는 내용이나 질문일 경우 솔직하게 안내하고 일반적인 딥워큰 지식 기반으로 보완해 주세요.
"""

class BuildAdvisor:
    """5단계: RAG 기반 Deepwoken 빌드 추천 어드바이저 챗봇"""

    def __init__(
        self,
        api_key: Optional[str] = None,
        model_name: str = "gemini-3.7-flash",
        db_path: str = "data/chromadb",
        collection_name: str = "deepwoken_builds",
        top_k: int = 4
    ):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY is not set.")
        
        genai.configure(api_key=self.api_key)
        self.model_name = model_name
        self.top_k = top_k
        self.kb = KnowledgeBuilder(db_path=db_path, collection_name=collection_name, api_key=self.api_key)
        self.chat_session = None
        self._init_chat()

    def _init_chat(self):
        model = genai.GenerativeModel(
            model_name=self.model_name,
            system_instruction=ADVISOR_SYSTEM_PROMPT
        )
        self.chat_session = model.start_chat(history=[])

    def ask(self, user_query: str) -> str:
        """사용자 질문에 대해 RAG 검색 후 Gemini 응답 생성"""
        # 1. RAG 검색
        search_results = self.kb.query(query_text=user_query, n_results=self.top_k)
        
        context_blocks = []
        if search_results:
            for idx, res in enumerate(search_results, 1):
                meta = res["metadata"]
                context_blocks.append(
                    f"--- [빌드 {idx}: {meta.get('build_name', 'Unknown')}] ---\n"
                    f"타입: {meta.get('build_type')} | Oath: {meta.get('oath')} | 출처: {meta.get('url')}\n"
                    f"상세 내용:\n{res['document']}\n"
                )
            context_text = "\n\n".join(context_blocks)
        else:
            context_text = "현재 지식 베이스에 인덱싱된 빌드가 없습니다."

        # 2. 프롬프트 구성
        prompt = (
            f"[사용자 질문]\n{user_query}\n\n"
            f"[참고 빌드 지식 (RAG 검색 결과)]\n{context_text}\n\n"
            f"위 참고 빌드 지식을 바탕으로 사용자에게 최적의 빌드 추천 및 가이드를 친절하고 전문적인 마크다운 형식으로 제공하세요."
        )

        models_to_try = ["gemini-flash-latest", "gemini-3.7-flash", "gemini-3.6-flash", "gemini-pro-latest"]
        for m_name in dict.fromkeys(models_to_try):
            try:
                m = genai.GenerativeModel(m_name, system_instruction=ADVISOR_SYSTEM_PROMPT)
                res = m.generate_content(prompt)
                return res.text
            except Exception as e:
                logger.warning(f"Advisor model {m_name} failed: {e}")

        return "⚠️ 답변 생성 중 오류가 발생했습니다. API 키를 확인해 주세요."

    def answer_query(self, user_query: str) -> str:
        return self.ask(user_query)

DeepwokenBuildAdvisor = BuildAdvisor

    def interactive_cli(self):
        """터미널 대화형 인터페이스 실행"""
        console = Console()
        console.print("[bold cyan]════════════════════════════════════════════════════[/bold cyan]")
        console.print("[bold green]⚔️ Deepwoken AI Build Advisor 에 오신 것을 환영합니다![/bold green]")
        console.print("[dim]원하는 빌드(예: 'Thundercall 대검 PvP 빌드', '초보자용 PvE')를 물어보세요. (종료: 'exit' 또는 'q')[/dim]")
        console.print("[bold cyan]════════════════════════════════════════════════════[/bold cyan]\n")

        while True:
            try:
                user_input = Prompt.ask("[bold yellow]질문 입력[/bold yellow]")
                if not user_input or user_input.strip().lower() in ["exit", "quit", "q"]:
                    console.print("[bold magenta]대화를 종료합니다. Safe sailing, Voyager![/bold magenta]")
                    break

                with console.status("[bold blue]빌드 지식 검색 및 AI 답변 생성 중...[/bold blue]"):
                    answer = self.ask(user_input.strip())

                console.print("\n[bold green]💡 어드바이저 추천 답변:[/bold green]")
                console.print(Markdown(answer))
                console.print("\n" + "─" * 50 + "\n")
            except KeyboardInterrupt:
                console.print("\n[bold magenta]대화를 종료합니다.[/bold magenta]")
                break
            except Exception as e:
                console.print(f"[bold red]오류 발생:[/bold red] {e}")
