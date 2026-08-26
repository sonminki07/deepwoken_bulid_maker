import os
import re
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
        """실시간 웹 검색 (Deepwoken Wiki, Reddit 등 심층 검색)"""
        # 사용자 질문 본문만 추출하여 검색 쿼리 구성
        if "[사용자 질문]" in query:
            clean_q = query.split("[사용자 질문]")[-1].strip()
        else:
            clean_q = re.sub(r'\[.*?\]', '', query).replace('\n', ' ').strip()
            
        clean_q = ' '.join(clean_q.split()[:10])
        if not clean_q:
            return ""

        search_query = f"Deepwoken {clean_q}"
        try:
            with DDGS(timeout=4) as ddgs:
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
        """사용자 질문에 대해 은어 보정 + 대화 히스토리 + RAG 지식 베이스 + 실시간 웹 검색을 융합하여 정밀 답변 생성"""
        # 0. 한국어 은어/음성 오타 지능형 보정 & 강제 팩트체크 주석 추가
        from chatbot.slang_normalizer import DeepwokenSlangResolver
        enriched_query = DeepwokenSlangResolver.enrich_prompt_with_deep_knowledge(user_query)

        # 1. 로컬 RAG 검색 (지식 베이스 + 노트북LM 노트)
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
        web_context = self.search_web(user_query, max_results=4)

        # 3. 대화 맥락(History) 포맷팅
        history_text = ""
        if history:
            history_text = "=== [이전 대화 맥락 (기억)] ===\n"
            for turn in history[-6:]:
                role_label = "사용자" if turn.get("role") == "user" else "AI 코치"
                history_text += f"{role_label}: {turn.get('content', '')}\n"
            history_text += "\n"

        # /build 또는 /bulid 명령어 감지 시 전수 감사 모드(Full Audit Mode) 가동
        is_build_audit = "/build" in user_query.lower() or "/bulid" in user_query.lower()
        audit_instruction = ""
        if is_build_audit:
            audit_instruction = (
                "\n\n[🔥 /build 전수 감사(Full Audit) 모드 활성화]\n"
                "사용자가 '/build' 명령어를 호출했습니다. 아래 8개 항목을 하나하나 빠짐없이 전수 점검하여, "
                "현재 설정값의 이상한 점, 스탯 낭비, 누락된 선행 탤런트, 장비/인챈트 시너지, 보완책을 조목조목 완벽한 전수 감사 리포트로 출력하세요:\n"
                "1. 종족(Race) 및 4대 특성(Traits 12pt) 분배의 타당성\n"
                "2. ⛩️ 사원 전(Pre-Shrine) 필수 탤런트 해금 스탯 유효성\n"
                "3. 📊 사원 후(Post-Shrine) 330pt 분배 및 스탯 초과/누락 여부\n"
                "4. ⚔️ Oath 요구 조건 및 속성(Attunement) 충돌 여부 (예: Silentheart 무속성 0pt 필수)\n"
                "5. ⭐ 핵심 탤런트(Reinforced Armor, Collapsed Lung, Ghost 등) 선행 스탯 충족 여부\n"
                "6. 🔮 만트라 및 스킬 콤보 연계성\n"
                "7. 🛡️ 11대 장비(방어구, 악세사리, 무기, 인챈트, 벨) 세팅 최적화\n"
                "8. 💡 최종 EHP(실질 체력) 및 보스전(Duke/Primadon/Chaser) 극딜을 위한 종합 개선안"
            )

        # 4. 통합 프롬프트 생성 (4중 지식 융합)
        prompt = (
            f"{history_text}"
            f"=== [사용자의 현재 질문 및 딥위큰 룰 분석] ===\n{enriched_query}\n\n"
            f"=== [참고 1: 로컬 깃허브 & 노트북LM 지식 데이터베이스] ===\n"
            f"{rag_context if rag_context else '로컬에 직접 매칭된 빌드 없음'}\n\n"
            f"=== [참고 2: 실시간 Deepwoken 위키 및 빌더 검색 데이터] ===\n"
            f"{web_context if web_context else '웹 검색 결과 없음'}\n"
            f"{audit_instruction}\n\n"
            f"위 대화 맥락과 딥위큰 시스템 룰을 엄격히 준수하여, 사용자가 의도한 정확한 빌드(예: 사일런트하트 평타, 브릭월 극탱 등)로 실전 전술과 정확한 330pt 분배를 한국어로 명확히 제시하세요."
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
