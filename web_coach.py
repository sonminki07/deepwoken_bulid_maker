import os
import json
import time
from pathlib import Path
from typing import Dict, Any, List
import streamlit as st

# 로컬 백엔드 모듈 임포트
from chatbot.build_advisor import BuildAdvisor
from chatbot.coach_validator import DeepwokenFactChecker, TALENT_PREREQUISITES, OATH_PREREQUISITES

# 페이지 기본 설정
st.set_page_config(
    page_title="Deepwoken Builder & AI Master Coach",
    page_icon="⚔️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Deepwoken Builder 고유 고딕 다크 테마 커스텀 CSS
st.markdown("""
<style>
    /* 전체 테마 색상 (Deepwoken Builder Dark Theme) */
    .stApp {
        background-color: #0b0c10;
        color: #e0e2ec;
        font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif;
    }
    
    /* 헤더 스타일링 */
    .deepwoken-title {
        font-family: 'Cinzel', serif, -apple-system;
        font-size: 2.2rem;
        font-weight: 700;
        color: #e5b869;
        text-shadow: 0 0 12px rgba(229, 184, 105, 0.4);
        margin-bottom: 0.2rem;
    }
    .deepwoken-subtitle {
        font-size: 0.95rem;
        color: #8c93a8;
        margin-bottom: 1.5rem;
    }

    /* 빌더 카드 및 컨테이너 */
    .builder-card {
        background: #141721;
        border: 1px solid #232838;
        border-radius: 8px;
        padding: 16px;
        margin-bottom: 14px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
    }
    
    /* 스탯 요약 뱃지 */
    .stat-badge-ok {
        background-color: #133a26;
        color: #4ade80;
        padding: 6px 12px;
        border-radius: 6px;
        font-weight: bold;
        display: inline-block;
        border: 1px solid #22c55e;
    }
    .stat-badge-warn {
        background-color: #451a1a;
        color: #f87171;
        padding: 6px 12px;
        border-radius: 6px;
        font-weight: bold;
        display: inline-block;
        border: 1px solid #ef4444;
    }

    /* 속성 알약 태그 (Attunement Pills) */
    .attunement-frost { color: #38bdf8; font-weight: bold; }
    .attunement-flame { color: #f87171; font-weight: bold; }
    .attunement-thunder { color: #fbbf24; font-weight: bold; }
    .attunement-gale { color: #34d399; font-weight: bold; }
    .attunement-shadow { color: #c084fc; font-weight: bold; }
    .attunement-iron { color: #cbd5e1; font-weight: bold; }

    /* 채팅 말풍선 커스텀 */
    .chat-user {
        background-color: #1e2433;
        border-left: 4px solid #38bdf8;
        padding: 12px;
        border-radius: 6px;
        margin-bottom: 10px;
    }
    .chat-assistant {
        background-color: #151824;
        border-left: 4px solid #e5b869;
        padding: 12px;
        border-radius: 6px;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# 프로필 파일 경로
PROFILES_FILE = Path("data/user_profiles.json")

def load_user_profiles() -> Dict[str, Any]:
    if PROFILES_FILE.exists():
        try:
            return json.loads(PROFILES_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    # 기본 프로필
    return {
        "Frostdraw 대검 Starkindred (샘플)": {
            "name": "Frostdraw 대검 Starkindred (샘플)",
            "oath": "Starkindred",
            "weapon_type": "Heavy Weapon (대검)",
            "attunement": "Frostdraw",
            "stats": {
                "Strength": 40, "Fortitude": 50, "Agility": 25,
                "Intelligence": 0, "Willpower": 20, "Charisma": 25,
                "Heavy Wep": 100, "Medium Wep": 0, "Light Wep": 0,
                "Frostdraw": 80, "Flamecharm": 0, "Thundercall": 0,
                "Galebreathe": 0, "Shadowcast": 0, "Ironsing": 0
            },
            "mantras": "Glacial Arc, Crystal Prism, Ice Lance, Sinister Halo, Ascension",
            "talents": "Conditioned Runner, Exoskeleton, To the Finish, Speed Demon, Charismatic Cast"
        }
    }

def save_user_profiles(profiles: Dict[str, Any]):
    PROFILES_FILE.parent.mkdir(parents=True, exist_ok=True)
    PROFILES_FILE.write_text(json.dumps(profiles, ensure_ascii=False, indent=2), encoding="utf-8")

# 세션 상태 초기화
if "profiles" not in st.session_state:
    st.session_state.profiles = load_user_profiles()
if "current_profile_name" not in st.session_state:
    st.session_state.current_profile_name = list(st.session_state.profiles.keys())[0]
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "advisor" not in st.session_state:
    st.session_state.advisor = BuildAdvisor(top_k=4)

# ----------------- UI 렌더링 -----------------

# 상단 헤더
st.markdown('<div class="deepwoken-title">⚔️ Deepwoken Builder & AI Master Coach</div>', unsafe_allow_html=True)
st.markdown('<div class="deepwoken-subtitle">Deepwoken Builder 스타일 캐릭터 슬롯 관리 & RAG 기반 100% 무환각 실시간 전술 코칭 시스템</div>', unsafe_allow_html=True)

# 메인 2분할 레이아웃: [좌측: Builder 슬롯 / 우측: 1:1 AI 코치 채팅]
col_builder, col_coach = st.columns([1.1, 1.4], gap="large")

# ==========================================
# 👤 좌측: Deepwoken Character Builder 슬롯
# ==========================================
with col_builder:
    st.markdown("### 👤 Deepwoken Character Builder")
    
    # 1. 프로필 슬롯 선택 & 관리
    profile_names = list(st.session_state.profiles.keys())
    selected_name = st.selectbox("📂 캐릭터 빌드 슬롯 선택:", profile_names, index=profile_names.index(st.session_state.current_profile_name) if st.session_state.current_profile_name in profile_names else 0)
    st.session_state.current_profile_name = selected_name
    curr_data = st.session_state.profiles[selected_name]

    with st.expander("➕ 새 빌드 생성 / 이름 변경", expanded=False):
        new_slot_name = st.text_input("새 빌드 이름:", value=f"내 캐릭터 빌드 {len(profile_names)+1}")
        if st.button("✨ 새 빌드 생성"):
            if new_slot_name and new_slot_name not in st.session_state.profiles:
                st.session_state.profiles[new_slot_name] = {
                    "name": new_slot_name,
                    "oath": "Oathless",
                    "weapon_type": "Heavy Weapon",
                    "attunement": "Frostdraw",
                    "stats": {k: 0 for k in curr_data.get("stats", {})},
                    "mantras": "",
                    "talents": ""
                }
                st.session_state.current_profile_name = new_slot_name
                save_user_profiles(st.session_state.profiles)
                st.rerun()

    # 2. 기본 정보 (Oath, 무기, 속성)
    c1, c2, c3 = st.columns(3)
    with c1:
        oath_list = list(OATH_PREREQUISITES.keys())
        current_oath = st.selectbox("Oath", oath_list, index=oath_list.index(curr_data.get("oath", "Oathless")) if curr_data.get("oath") in oath_list else 0)
    with c2:
        weapon_type = st.selectbox("주무기군", ["Heavy Weapon", "Medium Weapon", "Light Weapon", "Fist / Gun"], index=0)
    with c3:
        main_attunement = st.selectbox("주속성", ["Frostdraw", "Flamecharm", "Thundercall", "Galebreathe", "Shadowcast", "Ironsing", "Attunementless (무속성)"], index=0)

    # 3. 6대 기본 스탯 (Core Attributes)
    st.markdown("#### 📊 기본 스탯 (Core Attributes)")
    saved_stats = curr_data.get("stats", {})
    
    s_col1, s_col2, s_col3 = st.columns(3)
    with s_col1:
        str_val = st.number_input("Strength (근력)", 0, 102, int(saved_stats.get("Strength", 0)))
        fort_val = st.number_input("Fortitude (인내)", 0, 102, int(saved_stats.get("Fortitude", 0)))
    with s_col2:
        agi_val = st.number_input("Agility (민첩)", 0, 102, int(saved_stats.get("Agility", 0)))
        int_val = st.number_input("Intelligence (지능)", 0, 102, int(saved_stats.get("Intelligence", 0)))
    with s_col3:
        wil_val = st.number_input("Willpower (의지)", 0, 102, int(saved_stats.get("Willpower", 0)))
        cha_val = st.number_input("Charisma (매력)", 0, 102, int(saved_stats.get("Charisma", 0)))

    # 4. 무기 및 속성 투자 (Weapons & Attunements)
    st.markdown("#### ⚔️ 무기 및 속성 포인트 (Weapon & Element)")
    w_col1, w_col2 = st.columns(2)
    with w_col1:
        wep_stat = st.number_input(f"{weapon_type} 투자", 0, 100, int(saved_stats.get("Heavy Wep", 0) or saved_stats.get("Medium Wep", 0) or saved_stats.get("Light Wep", 0)))
    with w_col2:
        att_stat = st.number_input(f"{main_attunement} 투자", 0, 100, int(saved_stats.get(main_attunement, 0)))

    # 스탯 총합 계산 및 330 상한선 표시
    current_stat_dict = {
        "Strength": str_val, "Fortitude": fort_val, "Agility": agi_val,
        "Intelligence": int_val, "Willpower": wil_val, "Charisma": cha_val,
        "Heavy Wep": wep_stat if "Heavy" in weapon_type else 0,
        "Medium Wep": wep_stat if "Medium" in weapon_type else 0,
        "Light Wep": wep_stat if "Light" in weapon_type else 0,
        main_attunement: att_stat
    }
    total_stat_points = DeepwokenFactChecker.calculate_total_stats(current_stat_dict)

    if total_stat_points <= 330:
        st.markdown(f'<div class="stat-badge-ok">📊 총 스탯 투자: {total_stat_points} / 330 pt (정상 범위 ✅)</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="stat-badge-warn">⚠️ 총 스탯 초과: {total_stat_points} / 330 pt (+{total_stat_points - 330}pt 초과)</div>', unsafe_allow_html=True)

    # 5. 장착 만트라 및 핵심 탤런트
    mantras_input = st.text_input("🔮 장착 만트라 목록 (쉼표 구분):", value=curr_data.get("mantras", ""))
    talents_input = st.text_input("⭐ 핵심 탤런트 목록 (쉼표 구분):", value=curr_data.get("talents", ""))

    # 저장 버튼
    if st.button("💾 현재 캐릭터 프로필 저장", use_container_width=True):
        st.session_state.profiles[selected_name] = {
            "name": selected_name,
            "oath": current_oath,
            "weapon_type": weapon_type,
            "attunement": main_attunement,
            "stats": current_stat_dict,
            "mantras": mantras_input,
            "talents": talents_input
        }
        save_user_profiles(st.session_state.profiles)
        st.success(f"'{selected_name}' 프로필이 안전하게 저장되었습니다! ✅")

# ==========================================
# 💬 우측: 1:1 맞춤형 AI 전담 코치 & 팩트체커
# ==========================================
with col_coach:
    st.markdown("### 💬 1:1 맞춤형 AI Master Coach")
    
    # 현재 연결된 프로필 안내 배너
    active_profile = st.session_state.profiles.get(st.session_state.current_profile_name, {})
    st.info(f"🔗 **연결된 캐릭터:** `{active_profile.get('name')}` | **Oath:** `{active_profile.get('oath')}` | **주속성:** `{active_profile.get('attunement')}` | **무기:** `{active_profile.get('weapon_type')}`")

    # 빠른 질문 추천 칩 (Pills)
    st.markdown("⚡ **빠른 코칭 추천 질문:**")
    quick_cols = st.columns(4)
    quick_q = None
    if quick_cols[0].button("🥊 듀크 그로기 콤보"):
        quick_q = "내 캐릭터 세팅 기준으로 듀크(Duke) 실드가 깨지거나 그로기 걸렸을 때 가장 폭딜이 나오는 만트라/스킬 콤보 사이클을 알려줘."
    if quick_cols[1].button("🐵 프리마돈 공략 팁"):
        quick_q = "내 캐릭터 빌드로 프리마돈(Primadon) 패링 후 딜 타이밍과 주의해야 할 패턴을 알려줘."
    if quick_cols[2].button("🏛️ Shrine of Order 최적화"):
        quick_q = "내 현재 목표 스탯을 맞추기 위해 Shrine of Order를 타기 전(Pre-Shrine)과 탄 후(Post-Shrine) 어떤 순서로 스탯을 찍어야 하는지 최적의 루트를 계산해줘."
    if quick_cols[3].button("🛡️ 탤런트 무결성 검증"):
        quick_q = "현재 내 스탯으로 찍을 수 있는 핵심 필수 탤런트와 누락된 선행 스탯이 있는지 정밀 감사해줘."

    # 채팅 메시지 기록 출력
    chat_container = st.container()
    with chat_container:
        if not st.session_state.chat_history:
            st.markdown("""
            <div class="chat-assistant">
            🤖 <b>Deepwoken AI Coach</b>: 안녕하세요! 현재 좌측에 설정하신 <b>캐릭터 빌드</b>를 완벽하게 파악하고 있습니다.<br>
            보스별 그로기 딜 사이클, 만트라 연계 순서, Shrine of Order 스탯 육성법 등 무엇이든 물어보세요!
            </div>
            """, unsafe_allow_html=True)
        else:
            for turn in st.session_state.chat_history:
                if turn["role"] == "user":
                    st.markdown(f'<div class="chat-user">👤 <b>나:</b> {turn["content"]}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="chat-assistant">🤖 <b>AI 코치:</b><br>{turn["content"]}</div>', unsafe_allow_html=True)

    # 사용자 질문 입력창
    user_input = st.chat_input("질문을 입력하세요 (예: 듀크 딜 타임 때 어떤 콤보를 써야 해?)...")
    prompt_to_send = quick_q or user_input

    if prompt_to_send:
        # 사용자 질문 추가
        st.session_state.chat_history.append({"role": "user", "content": prompt_to_send})
        
        # AI 코칭 질문 프롬프트 구성 (캐릭터 프로필 강제 주입)
        profile_context = (
            f"[현재 사용자 캐릭터 프로필]\n"
            f"- 빌드명: {active_profile.get('name')}\n"
            f"- Oath: {active_profile.get('oath')}\n"
            f"- 주무기: {active_profile.get('weapon_type')}\n"
            f"- 주속성: {active_profile.get('attunement')}\n"
            f"- 스탯 분배: {active_profile.get('stats')}\n"
            f"- 장착 만트라: {active_profile.get('mantras')}\n"
            f"- 장착/목표 탤런트: {active_profile.get('talents')}\n"
        )
        
        full_query = f"{profile_context}\n[사용자 질문]\n{prompt_to_send}"
        
        with st.spinner("🧠 깃허브 지식 베이스 검색 & 팩트체크 검증 중..."):
            # 1. AI 조언가 응답 생성
            raw_advice = st.session_state.advisor.answer_query(
                user_query=full_query,
                history=st.session_state.chat_history[:-1]
            )
            
            # 2. 팩트체크 & 스탯 무결성 2차 감사 (Validation Pass)
            audit_result = DeepwokenFactChecker.audit_profile_and_advice(active_profile, raw_advice)
            verification_badge = DeepwokenFactChecker.generate_verification_badge(audit_result)
            
            final_response = raw_advice + "\n" + verification_badge
            st.session_state.chat_history.append({"role": "assistant", "content": final_response})
            st.rerun()

    # 대화 초기화 버튼
    if st.button("🧹 대화 기억 초기화"):
        st.session_state.chat_history = []
        st.rerun()

# ==========================================
# 📚 하단: 깃허브 검증 빌드 데이터베이스 뷰어
# ==========================================
st.markdown("---")
with st.expander("📚 깃허브 검증 빌드 데이터베이스 (Markdown 지식 문서 열람)", expanded=False):
    kb_files = list(Path("data/knowledge_base/builds").glob("*.md"))
    if kb_files:
        selected_doc = st.selectbox("열람할 빌드 지식 문서 선택:", [f.name for f in kb_files])
        doc_path = Path("data/knowledge_base/builds") / selected_doc
        if doc_path.exists():
            st.markdown(doc_path.read_text(encoding="utf-8"))
    else:
        st.info("현재 분석 완료된 지식 베이스 문서가 없습니다.")
