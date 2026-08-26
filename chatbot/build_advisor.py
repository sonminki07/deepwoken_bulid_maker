import os
import re
import json
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

4. **절대 금지: 가짜 메커니즘 창작 및 변명 금지 (Zero Hallucination / Fact-Only)**:
   - 탤런트나 스킬 효과를 설명할 때 없는 효과(예: 수동 스킬을 '자동 회피'라고 하거나, 없는 '추가 대미지'가 있다고 지어내는 것)를 창작하는 것을 엄격히 금지합니다.
   - Ghost는 'Q키로 구를 때 투명화 및 무적 시간(I-frame 1.2초)을 부여하는 수동 회피 탤런트'이며, 자동 회피나 추가 딜이 전혀 없습니다.
   - 딜러 빌드에서 생존/유틸 탤런트(Ghost, Reinforced Armor, Exoskeleton 등)를 채용하는 진짜 실전 이유는, 딥위큰의 가드브레이크/넉백 위험을 줄이고 사원 전(Pre-Shrine) 탤런트를 보존하여 실전 생존율과 안정성을 확보하기 위함입니다.
   - 모르는 정보나 없는 효과에 대해 거짓말로 지어내지 말고, 인게임 실제 작동 원리와 공식 위키 수치에 기반해서만 정직하게 답변하세요.

5. **모든 답변 하단에 반드시 공식 출처 및 시스템 근거(Citations & Grounding) 명시**:
   - 사용자가 제공된 정보의 진위 여부를 즉시 확인하고 신뢰할 수 있도록, 모든 설명이나 빌드 가이드 맨 하단에 반드시 아래 양식으로 명확한 출처와 근거를 표기하세요:
   ```markdown
   ---
   📚 **[공식 출처 및 시스템 근거]**
   - 📖 **공식 위키**: Deepwoken Fandom Wiki (해당 탤런트/스탯/서약 문서명)
   - ⚙️ **인게임 메커니즘**: (해당 수치가 적용되는 실제 인게임 판정/시스템 룰)
   - 🎬 **참조 데이터**: (로컬 마스터 빌드 DB / 출처 유튜브 영상명)
   ```
"""

class BuildAdvisor:
    """5단계: RAG + 실시간 웹 검색(DDGS) 하이브리드 Deepwoken AI 빌드 어드바이저 (대화 맥락 기억 지원)"""

    def __init__(
        self,
        api_key: Optional[str] = None,
        model_name: str = "gemini-2.5-flash",
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

        # 1. 마스터 비디오 빌드 데이터베이스 직접 조회 및 그라운딩 (Golden Truth)
        matched_master_build_text = ""
        try:
            from pathlib import Path
            profiles_file = Path(__file__).parent.parent / "data" / "user_profiles.json"
            if profiles_file.exists():
                profiles_data = json.loads(profiles_file.read_text(encoding="utf-8"))
                query_lower = user_query.lower()
                matched_data = None
                for b_name, b_data in profiles_data.items():
                    if any(k in query_lower for k in ["silentheart", "사일런트하트", "사하", "canor", "카노르", "m1 melter", "사슬"]) and "Silentheart" in b_data.get("oath", ""):
                        matched_data = (b_name, b_data); break
                    elif any(k in query_lower for k in ["kato", "카토", "gale", "게일", "depth"]) and "Gale" in b_name:
                        matched_data = (b_name, b_data); break
                    elif any(k in query_lower for k in ["bloodrend", "블러드렌드", "vampire", "뱀파이어", "흡혈"]) and "Bloodrend" in b_name:
                        matched_data = (b_name, b_data); break
                    elif any(k in query_lower for k in ["azure", "아주르", "steam duster", "너클"]) and "Azure" in b_name:
                        matched_data = (b_name, b_data); break
                    elif any(k in query_lower for k in ["poser", "포저", "ironsing", "아이언싱", "thundercall", "썬더콜"]) and "Poser" in b_name:
                        matched_data = (b_name, b_data); break
                    elif any(k in query_lower for k in ["volcanic", "brick wall", "브릭월", "창", "spear"]) and "Brick Wall" in b_name:
                        matched_data = (b_name, b_data); break
                    elif any(k in query_lower for k in ["soul beam", "소울 빔", "blindseer", "블라인드시어"]) and "Soul Beam" in b_name:
                        matched_data = (b_name, b_data); break
                    elif any(k in query_lower for k in ["shattered", "katana", "카타나", "silent swordsman"]) and "Shattered" in b_name:
                        matched_data = (b_name, b_data); break
                    elif any(k in query_lower for k in ["shadow", "섀도우", "암흑", "그림자"]) and "Shadowcast" in b_name:
                        matched_data = (b_name, b_data); break
                    elif any(k in query_lower for k in ["ashen", "moppet", "dagger", "단검", "글래스"]) and "Dagger" in b_name:
                        matched_data = (b_name, b_data); break

                if matched_data:
                    m_name, m_val = matched_data
                    matched_master_build_text = (
                        f"=== [공식 100% 검증된 마스터 비디오 빌드 데이터: '{m_name}'] ===\n"
                        f"- 종족(Race): {m_val.get('race')} (기본치 훼손 금지)\n"
                        f"- Oath(서약): {m_val.get('oath')}\n"
                        f"- 주무기: {m_val.get('weapon_type')}, 주속성: {m_val.get('attunement')}\n"
                        f"- Pre-Shrine(사원 전) 스탯: {m_val.get('pre_shrine')}\n"
                        f"- Post-Shrine(사원 후 최종 330pt) 스탯: {m_val.get('stats')}\n"
                        f"- 11대 장비 세팅: {m_val.get('equipment')}\n"
                        f"- 만트라 및 스킬: {m_val.get('mantras')}\n"
                        f"- 핵심 탤런트: {m_val.get('talents')}\n"
                        f"- 출처 영상: {m_val.get('source_video')}\n"
                        f"⚠️ 위 마스터 빌드의 스탯 수치(Post-Shrine 합계 정확히 330pt)를 절대로 변경하거나 왜곡하지 말고 원형 그대로 명확하게 제시하세요.\n"
                    )
        except Exception as e:
            logger.warning(f"Master build lookup failed: {e}")

        # 2. 로컬 RAG 검색 (지식 베이스 + 노트북LM 노트)
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

        # 3. 실시간 웹 검색 (Wiki / Reddit)
        web_context = self.search_web(user_query, max_results=4)

        # 4. 대화 맥락(History) 포맷팅
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

        # 5. 통합 프롬프트 생성 (5중 지식 융합)
        prompt = (
            f"{history_text}"
            f"=== [사용자의 현재 질문 및 딥위큰 룰 분석] ===\n{enriched_query}\n\n"
            f"{matched_master_build_text}\n"
            f"=== [참고 1: 로컬 깃허브 & 노트북LM 지식 데이터베이스] ===\n"
            f"{rag_context if rag_context else '로컬에 직접 매칭된 빌드 없음'}\n\n"
            f"=== [참고 2: 실시간 Deepwoken 위키 및 빌더 검색 데이터] ===\n"
            f"{web_context if web_context else '웹 검색 결과 없음'}\n"
            f"{audit_instruction}\n\n"
            f"⚠️ [절대 필수 검증 룰]\n"
            f"1. 사원 후(Post-Shrine) 최종 스탯을 제시할 때는 6대 기본 스탯 + 무기 + 속성의 합산이 반드시 '정확히 330 pt'가 되도록 암산하여 1포인트의 오차도 없이 작성하세요.\n"
            f"2. 종족 기본치 이하로 스탯을 깎지 마세요 (Canor는 Str 3 이상, Cha 2 이상 필수. 불필요한 Int 2 등을 임의로 넣지 마세요).\n"
            f"3. 위 대화 맥락과 딥위큰 시스템 룰을 엄격히 준수하여, 사용자가 의도한 정확한 빌드(예: 사일런트하트 평타, 브릭월 극탱 등)로 실전 전술과 정확한 330pt 분배를 한국어로 명확히 제시하세요."
        )

        def _call_model(client: genai.Client) -> str:
            last_err = None
            # 신속하고 안정적인 고성능 모델 우선 호출
            for m_name in [
                "gemini-flash-lite-latest",
                "gemini-3.6-flash",
                "gemini-3.7-flash",
                "gemini-flash-latest",
                "gemini-3.1-pro-preview"
            ]:
                try:
                    response = client.models.generate_content(
                        model=m_name,
                        contents=prompt,
                        config=types.GenerateContentConfig(
                            system_instruction=ADVISOR_SYSTEM_PROMPT,
                            temperature=0.2
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
