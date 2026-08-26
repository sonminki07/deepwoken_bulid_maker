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

ADVISOR_SYSTEM_PROMPT = """당신은 세계 최고 실력의 베테랑 Roblox Deepwoken 전문 AI 코치이자 데이터 분석가입니다.
사용자와 자연스럽게 1:1 대화를 나누며, 로컬 빌드 지식 베이스(RAG)와 실시간 위키 검색 결과를 바탕으로 맞춤형 피드백을 제공합니다.

[🚨 핵심 대화 및 답변 원칙]
1. **대화 맥락과 사용자 캐릭터 정보 완벽 기억 (Multi-Turn Context)**:
   - 사용자가 이전에 언급한 캐릭터 스탯, 무기, 속성(Attunement), 상황을 반드시 기억하고 이어서 대화하세요.
   - 예: 사용자가 "나 프로스트드로 대검 빌드야"라고 한 뒤 "듀크 그로기 때 무슨 콤보 써?"라고 물으면, 듀크 빌드를 새로 읊지 말고 "사용자님의 프로스트드로 대검 빌드를 기준으로 듀크 그로기 타이밍 극딜 사이클"을 바로 콕 집어서 코칭하세요.

2. **질문 유형에 따른 유연하고 직관적인 답변 (천편일률적인 6단계 템플릿 금지!)**:
   - **타입 A. 특정 질문 / 상황별 딜 사이클 / 보스 공략 / 탤런트 질문 / 콤보 질문**:
     • 불필요하게 1번부터 6번까지의 전체 스탯표와 장비 템플릿을 처음부터 끝까지 다 나열하지 마세요!
     • 사용자가 궁금해하는 질문에 대해 즉시 명확하고 구체적인 **실전 행동 요령, 만트라 연계 순서, 회피/패링 타이밍 팁**만 깔끔하게 답변하세요.
   - **타입 B. 전체 빌드 추천 / 신규 빌드 설계 요청 (예: "초보자용 PvE 빌드 짜줘", "새로운 빌드 추천해줘")**:
     • 이때만 스탯, 장비, 탤런트, 만트라, 사냥법이 포함된 체계적인 종합 빌드 가이드를 제공하세요.

3. **100% 자연스럽고 친절한 한국어 (게임 고유명사는 인게임 영문 유지)**:
   - 본문에 지저분한 `[[1](...)]` 인용구는 넣지 마세요.
   - 탤런트명, 만트라명, 무기명, Oath명 등 게임 고유명칭은 인게임 영문명을 유지하세요.
   - 이해하기 쉬운 이모지와 가독성 높은 마크다운 소제목/글머리 기호를 활용하세요.
"""

class BuildAdvisor:
    """5단계: RAG + 실시간 웹 검색(DDGS) 하이브리드 Deepwoken AI 빌드 어드바이저 (대화 맥락 기억 지원)"""

    def __init__(
        self,
        api_key: Optional[str] = None,
        model_name: str = "gemini-3.7-flash",
        db_path: str = "data/chromadb",
        collection_name: str = "deepwoken_builds",
        top_k: int = 4
    ):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self.model_name = model_name
        self.top_k = top_k
        self.kb = KnowledgeBuilder(db_path=db_path, collection_name=collection_name, api_key=self.api_key, use_gemini_embedding=False)

    def search_web(self, query: str, max_results: int = 3) -> str:
        """실시간 웹 검색 (Deepwoken Wiki, Reddit, 빌더 등 - 최대 3초 타임아웃)"""
        # 멀티라인 및 특수문자 제거하여 핵심 키워드만 추출
        clean_q = re.sub(r'\[.*?\]', '', query).replace('\n', ' ').strip()
        clean_q = ' '.join(clean_q.split()[:8])  # 최대 8단어
        if not clean_q:
            return ""

        search_query = f"Deepwoken {clean_q}"
        try:
            with DDGS(timeout=3) as ddgs:
                results = list(ddgs.text(search_query, max_results=max_results))
                if not results:
                    return ""
                snippets = []
                for r in results:
                    snippets.append(f"- **{r.get('title')}**: {r.get('body')}")
                return "\n".join(snippets)
        except Exception as e:
            logger.warning(f"Web search skipped: {e}")
            return ""

    def ask(self, user_query: str, history: Optional[List[Dict[str, str]]] = None) -> str:
        """사용자 질문에 대해 대화 히스토리 + RAG 검색 + 실시간 웹 검색을 통합하여 유연한 맞춤형 답변 생성"""
        # 1. 로컬 RAG 검색
        rag_context = ""
        try:
            results = self.kb.query(query_text=user_query, n_results=self.top_k)
            if results:
                chunks = []
                for doc in results:
                    meta = doc.get("metadata", {})
                    chunks.append(f"- [{meta.get('build_type', 'build')}] {meta.get('build_name', '')}:\n{doc.get('document', '')[:400]}")
                rag_context = "\n".join(chunks)
        except Exception as e:
            logger.warning(f"RAG search warning: {e}")

        # 2. 실시간 웹 검색 (Wiki / Reddit)
        web_context = self.search_web(user_query, max_results=3)

        # 3. 대화 맥락(History) 포맷팅
        history_text = ""
        if history:
            history_text = "=== [이전 대화 맥락 (기억)] ===\n"
            for turn in history[-6:]:
                role_label = "사용자" if turn.get("role") == "user" else "AI 코치"
                history_text += f"{role_label}: {turn.get('content', '')}\n"
            history_text += "\n"

        # 4. 통합 프롬프트 생성
        prompt = (
            f"{history_text}"
            f"=== [사용자의 현재 질문] ===\n{user_query}\n\n"
            f"=== [참고 1: 로컬 저장소 빌드 데이터베이스 (RAG)] ===\n"
            f"{rag_context if rag_context else '로컬에 직접 매칭된 빌드 없음'}\n\n"
            f"=== [참고 2: 실시간 위키/웹 검색 결과] ===\n"
            f"{web_context if web_context else '웹 검색 결과 없음'}\n\n"
            f"위 대화 맥락과 참고 자료를 바탕으로, 사용자의 질문 의도에 딱 맞게 불필요한 전체 템플릿 나열 없이 직관적이고 전문적인 한국어로 답변하세요."
        )

        def _call_model(client: genai.Client) -> str:
            last_err = None
            # 최고 성능 고지능/고추론 플래그십 모델 우선 호출
            for m_name in [
                "gemini-3.7-flash",
                "gemini-3.6-flash",
                "gemini-pro-latest",
                "gemini-3.1-pro-preview",
                "gemini-flash-latest",
                "gemini-flash-lite-latest",
            ]:
                try:
                    response = client.models.generate_content(
                        model=m_name,
                        contents=prompt,
                        config=types.GenerateContentConfig(
                            system_instruction=ADVISOR_SYSTEM_PROMPT,
                            temperature=0.3
                        )
                    )
                    return response.text
                except Exception as model_err:
                    last_err = model_err
                    logger.warning(f"Advisor model {m_name} failed ({model_err}), trying next high-tier model...")
            if last_err:
                raise last_err
            raise RuntimeError("All advisor reasoning models failed")

        try:
            return global_key_manager.execute_with_failover(_call_model)
        except Exception as e:
            logger.error(f"Advisor generation error: {e}")
            return f"⚠️ 답변 생성 중 오류가 발생했습니다: {e}"

    def answer_query(self, user_query: str, history: Optional[List[Dict[str, str]]] = None) -> str:
        return self.ask(user_query, history=history)

DeepwokenBuildAdvisor = BuildAdvisor
