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
사용자의 질문에 대해 로컬 빌드 데이터베이스(RAG)와 실시간 웹 검색(Wiki, Reddit) 결과를 종합하여 친절하고 심층적인 한국어 분석 보고서를 제공합니다.

[답변 작성 가이드라인]
1. **100% 자연스럽고 전문적인 한국어로 작성**: 영어 원문이 있더라도 자연스러운 한국어로 번역 및 해설하세요. (단, 탤런트명, 만트라명, 아이템/무기명, Oath명 등 인게임 고유 명칭은 영문 유지)
2. **지저분한 링크 인용구 제외**: 본문에 `[[1](...)]`, `[[2](...)]` 같은 원문 링크 번호 태그를 넣지 말고 깔끔한 텍스트로 서술하세요.
3. **사용자가 이해하기 쉬운 논리적 순서로 구성**:
   - ⚔️ **1. 핵심 작동 원리 및 시스템 배경**: 왜 이 빌드/현상이 일어나는지 (예: 과다출혈 15% 고정 퍼센트 데미지 폭발 메커니즘, 스택 누적 방식 등) 알기 쉽게 설명
   - 📊 **2. 상세 스탯 분배 및 육성 (Pre-Shrine & Post-Shrine)**: 정확한 스탯 수치와 무기/속성 분배
   - 🛡️ **3. 추천 장비, 아웃핏 및 최적 인챈트**: 무기, 방어구(Black Diver, Prophet's Cloak 등), 추천 인챈트(Grim, Vampiric 등)
   - 🌟 **4. 핵심 탤런트(Talents) 및 주요 만트라(Mantras)**: 필수 탤런트와 딜링 만트라
   - 🎯 **5. 주요 타겟 보스 / 몹 사냥법**: 어떤 만트라/스킬을 써서 어떤 주요 보스(Chaser, Scion, Duke, Maestro, Primadon 등)를 어떻게 녹이는지 구체적인 사냥 팁
   - 🥊 **6. 실전 콤보 및 장단점 / 리스크 관리**: 전투 딜링 사이클 및 피흡/스태미나 관리법
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
                    snippets.append(f"- **{r.get('title')}**: {r.get('body')}")
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
                        f"타입: {meta.get('build_type')} | Oath: {meta.get('oath')}\n"
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
            f"위 참고 자료들을 종합하여 100% 한국어로 수치, 탤런트, 메커니즘, 장비/아웃핏, 타겟 보스 사냥법이 포함된 깔끔한 마크다운 보고서를 작성하세요."
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

DeepwokenBuildAdvisor = BuildAdvisor
