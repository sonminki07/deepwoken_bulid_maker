import os
import json
import time
from pathlib import Path
from typing import Dict, Any, List, Tuple
import streamlit as st

# 로컬 백엔드 모듈 임포트
from chatbot.build_advisor import BuildAdvisor
from chatbot.coach_validator import DeepwokenFactChecker, TALENT_PREREQUISITES, OATH_PREREQUISITES
from chatbot.builder_calculator import DeepwokenCalculator, DEEPWOKEN_RACES, OUTFIT_PRESETS
from chatbot.deepwoken_database import DEEPWOKEN_TALENTS_DB, DEEPWOKEN_MANTRAS_DB, EQUIPMENT_SLOTS_DB, render_tooltip_badge

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
    /* 메인 배경 및 폰트 */
    .stApp {
        background-color: #0c0d14;
        color: #e2e8f0;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* 카드 컨테이너 테두리 */
    .deepwoken-card {
        background: linear-gradient(145deg, #151824, #1b2030);
        border: 1px solid #2d3748;
        border-radius: 10px;
        padding: 18px;
        margin-bottom: 16px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
    }
    
    /* 타이틀 골드 텍스트 */
    .deepwoken-title {
        color: #e5b869;
        font-family: 'Cinzel', 'Georgia', serif;
        font-size: 1.8rem;
        font-weight: bold;
        text-shadow: 0 0 10px rgba(229, 184, 105, 0.3);
        margin-bottom: 4px;
    }
    .deepwoken-subtitle {
        color: #94a3b8;
        font-size: 0.95rem;
        margin-bottom: 20px;
    }
    
    /* 스탯 요약 뱃지 */
    .stat-badge-ok {
        background-color: rgba(16, 185, 129, 0.15);
        color: #34d399;
        padding: 6px 12px;
        border-radius: 6px;
        font-weight: bold;
        display: inline-block;
        border: 1px solid #10b981;
    }
    .stat-badge-warn {
        background-color: rgba(239, 68, 68, 0.15);
        color: #f87171;
        padding: 6px 12px;
        border-radius: 6px;
        font-weight: bold;
        display: inline-block;
        border: 1px solid #ef4444;
    }

    /* 탤런트 & 만트라 호버 툴팁 컨테이너 */
    .deepwoken-tooltip-container {
        position: relative;
        display: inline-block;
        margin: 4px;
    }
    .deepwoken-tooltip-container .tooltip-box {
        visibility: hidden;
        opacity: 0;
        width: 280px;
        background: #151824;
        color: #e2e8f0;
        text-align: left;
        border-radius: 8px;
        padding: 10px 12px;
        position: absolute;
        z-index: 99999;
        bottom: 125%;
        left: 50%;
        transform: translateX(-50%);
        box-shadow: 0 8px 24px rgba(0,0,0,0.85);
        border: 1px solid #e5b869;
        transition: opacity 0.2s ease, visibility 0.2s ease;
        font-size: 0.82rem;
        line-height: 1.4;
        pointer-events: none;
    }
    .deepwoken-tooltip-container:hover .tooltip-box {
        visibility: visible;
        opacity: 1;
    }

    .talent-tag {
        display: inline-block;
        background: linear-gradient(135deg, rgba(234, 88, 12, 0.18), rgba(245, 158, 11, 0.12));
        border: 1px solid rgba(245, 158, 11, 0.5);
        color: #fde68a;
        padding: 5px 11px;
        border-radius: 7px;
        font-size: 0.85rem;
        font-weight: 500;
        cursor: help;
        transition: all 0.2s ease;
    }
    .talent-tag:hover {
        background: rgba(245, 158, 11, 0.35);
        border-color: #fbbf24;
        color: #ffffff;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(245, 158, 11, 0.35);
    }
    .mantra-tag {
        display: inline-block;
        background: linear-gradient(135deg, rgba(147, 51, 234, 0.18), rgba(59, 130, 246, 0.12));
        border: 1px solid rgba(147, 51, 234, 0.5);
        color: #e9d5ff;
        padding: 5px 11px;
        border-radius: 7px;
        font-size: 0.85rem;
        font-weight: 500;
        cursor: help;
        transition: all 0.2s ease;
    }
    .mantra-tag:hover {
        background: rgba(147, 51, 234, 0.35);
        border-color: #c084fc;
        color: #ffffff;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(147, 51, 234, 0.35);
    }

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
<script>
// Ctrl+C 복사 시 Streamlit의 개발자용 'Clear Cache(캐시 삭제)' 팝업 방지
window.addEventListener('keydown', function(e) {
    if (e.key === 'c' || e.key === 'C' || e.keyCode === 67) {
        const activeTag = document.activeElement ? document.activeElement.tagName.toLowerCase() : '';
        if (activeTag !== 'input' && activeTag !== 'textarea') {
            if (e.ctrlKey || e.metaKey) {
                // 클립보드 복사는 허용하되 Streamlit 핫키 이벤트 전파 중단
                e.stopPropagation();
            } else {
                // 단독 'c' 입력 시 캐시 삭제 모달 오픈 원천 차단
                e.stopImmediatePropagation();
            }
        }
    }
}, true);
</script>
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

CHAT_HISTORY_FILE = Path("data/coach_chat_history.json")

def load_chat_history() -> List[Dict[str, str]]:
    if CHAT_HISTORY_FILE.exists():
        try:
            return json.loads(CHAT_HISTORY_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return []

def save_chat_history(history: List[Dict[str, str]]):
    CHAT_HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
    CHAT_HISTORY_FILE.write_text(json.dumps(history, ensure_ascii=False, indent=2), encoding="utf-8")

def save_user_profiles(profiles: Dict[str, Any]):
    PROFILES_FILE.parent.mkdir(parents=True, exist_ok=True)
    PROFILES_FILE.write_text(json.dumps(profiles, ensure_ascii=False, indent=2), encoding="utf-8")

# 세션 상태 초기화 (새로고침 시 항상 최신 JSON 파일에서 불러옴)
st.session_state.profiles = load_user_profiles()
if "current_profile_name" not in st.session_state or st.session_state.current_profile_name not in st.session_state.profiles:
    st.session_state.current_profile_name = list(st.session_state.profiles.keys())[0]
if "chat_history" not in st.session_state:
    st.session_state.chat_history = load_chat_history()
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
    selected_name = st.selectbox(
        "📂 캐릭터 빌드 슬롯 선택:", 
        profile_names, 
        index=profile_names.index(st.session_state.current_profile_name) if st.session_state.current_profile_name in profile_names else 0,
        key="slot_selector"
    )
    st.session_state.current_profile_name = selected_name
    curr_data = st.session_state.profiles[selected_name]

    with st.expander("➕ 새 빌드 슬롯 생성", expanded=False):
        new_slot_name = st.text_input("새 빌드 이름:", value=f"내 캐릭터 빌드 {len(profile_names)+1}", key="new_slot_input")
        if st.button("✨ 새 슬롯 생성", key="create_slot_btn"):
            if new_slot_name and new_slot_name not in st.session_state.profiles:
                st.session_state.profiles[new_slot_name] = {
                    "name": new_slot_name,
                    "oath": "Oathless",
                    "weapon_type": "Heavy Weapon",
                    "attunement": "Frostdraw",
                    "stats": {
                        "Strength": 0, "Fortitude": 0, "Agility": 0,
                        "Intelligence": 0, "Willpower": 0, "Charisma": 0,
                        "Heavy Wep": 0, "Medium Wep": 0, "Light Wep": 0,
                        "Frostdraw": 0, "Flamecharm": 0, "Thundercall": 0,
                        "Galebreathe": 0, "Shadowcast": 0, "Ironsing": 0
                    },
                    "mantras": "",
                    "talents": ""
                }
                st.session_state.current_profile_name = new_slot_name
                save_user_profiles(st.session_state.profiles)
                st.rerun()

    # 2. Aspect / Race (종족) 및 Oath, 무기군
    r_col1, r_col2 = st.columns([1, 1])
    with r_col1:
        race_list = list(DEEPWOKEN_RACES.keys())
        saved_race = curr_data.get("race", "Vesperian")
        race_idx = race_list.index(saved_race) if saved_race in race_list else race_list.index("Vesperian")
        selected_race = st.selectbox("🧬 Aspect / Race (종족)", race_list, index=race_idx, key=f"{selected_name}_race")
        st.caption(f"💡 {DEEPWOKEN_RACES[selected_race]['desc']}")
    with r_col2:
        oath_list = list(OATH_PREREQUISITES.keys())
        oath_idx = oath_list.index(curr_data.get("oath", "Oathless")) if curr_data.get("oath") in oath_list else 0
        current_oath = st.selectbox("⚔️ Oath (서약)", oath_list, index=oath_idx, key=f"{selected_name}_oath")

    c2, c3 = st.columns(2)
    with c2:
        wep_options = ["Heavy Weapon", "Medium Weapon", "Light Weapon", "Fist / Gun"]
        wep_idx = wep_options.index(curr_data.get("weapon_type", "Heavy Weapon")) if curr_data.get("weapon_type") in wep_options else 0
        weapon_type = st.selectbox("주무기군", wep_options, index=wep_idx, key=f"{selected_name}_wtype")
    with c3:
        att_options = ["Frostdraw", "Flamecharm", "Thundercall", "Galebreathe", "Shadowcast", "Ironsing", "Attunementless (무속성)"]
        att_idx = att_options.index(curr_data.get("attunement", "Frostdraw")) if curr_data.get("attunement") in att_options else 0
        main_attunement = st.selectbox("주속성", att_options, index=att_idx, key=f"{selected_name}_matt")

    # 3. 4대 보조 특성 (Traits - Deepwoken Wiki 공식 기준: 만렙 총 12pt 분배, 각 항목당 최대 6pt)
    st.markdown("#### 🌟 4대 특성 (Traits - 만렙 총 12pt 분배)")
    saved_traits = curr_data.get("traits", {"Vitality": 6, "Erudition": 6, "Proficiency": 0, "Songchant": 0})
    t_col1, t_col2, t_col3, t_col4 = st.columns(4)
    with t_col1:
        vit_val = st.number_input("Vitality (체력 +10/pt)", 0, 6, int(saved_traits.get("Vitality", 6)), key=f"{selected_name}_vit")
    with t_col2:
        eru_val = st.number_input("Erudition (에테르 +25/pt)", 0, 6, int(saved_traits.get("Erudition", 6)), key=f"{selected_name}_eru")
    with t_col3:
        pro_val = st.number_input("Proficiency (무기 딜증)", 0, 6, int(saved_traits.get("Proficiency", 0)), key=f"{selected_name}_pro")
    with t_col4:
        son_val = st.number_input("Songchant (만트라 딜)", 0, 6, int(saved_traits.get("Songchant", 0)), key=f"{selected_name}_son")

    total_traits = vit_val + eru_val + pro_val + son_val
    if total_traits <= 12:
        st.caption(f"🌟 특성 포인트 사용: **{total_traits} / 12 pt** (공식 룰 일치 ✅)")
    else:
        st.warning(f"⚠️ 특성 포인트 초과: {total_traits} / 12 pt (+{total_traits - 12}pt 초과)")

    # 4. ⛩️ Shrine of Order (사원) 전/후 스탯 분배
    st.markdown("#### ⛩️ Shrine of Order (사원) 전 / 후 스탯")
    
    saved_pre = curr_data.get("pre_shrine", {})
    saved_post = curr_data.get("stats", {})

    tab_post, tab_pre = st.tabs([
        "📊 Post-Shrine (사원 사용 후 최종 330pt 완성)", 
        "⛩️ Pre-Shrine (사원 사용 전 핵심 탤런트 해금)"
    ])

    # --- [탭 1: Post-Shrine (최종 완성 330pt)] ---
    race_stats = DEEPWOKEN_RACES.get(selected_race, {}).get("stats", {})
    min_str = race_stats.get("Strength", 0)
    min_fort = race_stats.get("Fortitude", 0)
    min_agi = race_stats.get("Agility", 0)
    min_int = race_stats.get("Intelligence", 0)
    min_wil = race_stats.get("Willpower", 0)
    min_cha = race_stats.get("Charisma", 0)

    with tab_post:
        st.caption("✨ 질서의 성소(Shrine of Order)로 스탯을 재분배한 뒤 최종 20레벨까지 완성한 최종 스탯입니다.")
        s_col1, s_col2, s_col3 = st.columns(3)
        with s_col1:
            str_val = st.number_input("Strength (근력)", min_str, 102, max(min_str, int(saved_post.get("Strength", min_str))), key=f"{selected_name}_str")
            fort_val = st.number_input("Fortitude (인내)", min_fort, 102, max(min_fort, int(saved_post.get("Fortitude", min_fort))), key=f"{selected_name}_fort")
        with s_col2:
            agi_val = st.number_input("Agility (민첩)", min_agi, 102, max(min_agi, int(saved_post.get("Agility", min_agi))), key=f"{selected_name}_agi")
            int_val = st.number_input("Intelligence (지능)", min_int, 102, max(min_int, int(saved_post.get("Intelligence", min_int))), key=f"{selected_name}_int")
        with s_col3:
            wil_val = st.number_input("Willpower (의지)", min_wil, 102, max(min_wil, int(saved_post.get("Willpower", min_wil))), key=f"{selected_name}_wil")
            cha_val = st.number_input("Charisma (매력)", min_cha, 102, max(min_cha, int(saved_post.get("Charisma", min_cha))), key=f"{selected_name}_cha")

        w_col1, w_col2 = st.columns(2)
        with w_col1:
            saved_wep_val = saved_post.get("Heavy Wep", 0) or saved_post.get("Medium Wep", 0) or saved_post.get("Light Wep", 0)
            wep_stat = st.number_input(f"{weapon_type} 투자", 0, 100, int(saved_wep_val), key=f"{selected_name}_wstat")
        with w_col2:
            saved_att_val = saved_post.get(main_attunement, 0)
            att_stat = st.number_input(f"{main_attunement} 투자", 0, 100, int(saved_att_val), key=f"{selected_name}_astat")

        post_stat_dict = {
            "Strength": str_val, "Fortitude": fort_val, "Agility": agi_val,
            "Intelligence": int_val, "Willpower": wil_val, "Charisma": cha_val,
            "Heavy Wep": wep_stat if "Heavy" in weapon_type else 0,
            "Medium Wep": wep_stat if "Medium" in weapon_type else 0,
            "Light Wep": wep_stat if "Light" in weapon_type else 0,
            main_attunement: att_stat
        }
        total_stat_points = DeepwokenFactChecker.calculate_total_stats(post_stat_dict)
        max_cap = DeepwokenFactChecker.MAX_VALID_STAT_SUM

        stat_badge_html = []
        if total_stat_points <= max_cap:
            stat_badge_html.append(f'<div class="stat-badge-ok">📊 최종 스탯 총합: {total_stat_points} / {max_cap} pt (공식 룰 100% 일치 ✅)</div>')
        else:
            stat_badge_html.append(f'<div class="stat-badge-warn">⚠️ 최종 스탯 초과: {total_stat_points} / {max_cap} pt (+{total_stat_points - max_cap}pt 초과)</div>')

        # 종족 고유 스탯 보존 실시간 검증 (Shrine of Order 룰)
        def check_racial_base_compliance(r_name: str, cur_s: Dict[str, int]) -> Tuple[bool, List[str]]:
            r_info = DEEPWOKEN_RACES.get(r_name)
            if not r_info: return True, []
            errs = []
            for s_name, m_val in r_info.get("stats", {}).items():
                c_val = cur_s.get(s_name, 0)
                if c_val < m_val:
                    errs.append(f"⚠️ {r_name} 종족의 {s_name} 기본치는 최소 {m_val}pt 이상이어야 합니다. (현재: {c_val}pt - 질서의 성소 삭감 불가 룰)")
            return len(errs) == 0, errs

        race_ok, race_errs = check_racial_base_compliance(selected_race, post_stat_dict)
        if race_ok:
            stat_badge_html.append(f'<div style="color: #34d399; font-size: 0.85rem; margin-top: 6px;">🧬 <b>{selected_race}</b> 종족 기본치 보존 룰 일치 (질서의 성소 삭감 불가 룰 준수 ✅)</div>')
        else:
            for re_msg in race_errs:
                stat_badge_html.append(f'<div style="color: #f87171; font-size: 0.85rem; margin-top: 4px;">{re_msg}</div>')

        st.markdown("".join(stat_badge_html), unsafe_allow_html=True)

    # --- [탭 2: Pre-Shrine (사원 사용 전 탤런트 스탯)] ---
    with tab_pre:
        st.caption("⛩️ 육성 초반 높은 스탯을 요구하는 핵심 탤런트(Collapsed Lung, Reinforced Armor, Brick Wall 등)를 선행 획득하기 위한 스탯입니다.")
        p_col1, p_col2, p_col3 = st.columns(3)
        with p_col1:
            pre_str = st.number_input("Pre Strength (힘)", 0, 102, int(saved_pre.get("Strength", str_val)), key=f"{selected_name}_pre_str")
            pre_fort = st.number_input("Pre Fortitude (인내)", 0, 102, int(saved_pre.get("Fortitude", fort_val)), key=f"{selected_name}_pre_fort")
        with p_col2:
            pre_agi = st.number_input("Pre Agility (민첩)", 0, 102, int(saved_pre.get("Agility", agi_val)), key=f"{selected_name}_pre_agi")
            pre_int = st.number_input("Pre Intelligence (지능)", 0, 102, int(saved_pre.get("Intelligence", int_val)), key=f"{selected_name}_pre_int")
        with p_col3:
            pre_wil = st.number_input("Pre Willpower (의지)", 0, 102, int(saved_pre.get("Willpower", wil_val)), key=f"{selected_name}_pre_wil")
            pre_cha = st.number_input("Pre Charisma (매력)", 0, 102, int(saved_pre.get("Charisma", cha_val)), key=f"{selected_name}_pre_cha")

        pre_stat_dict = {
            "Strength": pre_str, "Fortitude": pre_fort, "Agility": pre_agi,
            "Intelligence": pre_int, "Willpower": pre_wil, "Charisma": pre_cha,
            "Heavy Wep": 0, "Medium Wep": 0, "Light Wep": 0,
            main_attunement: 0
        }

        # 사원 전 해금 가능한 상위 탤런트 실시간 판별
        unlocked_talents = []
        if pre_fort >= 90: unlocked_talents.append("🛡️ Reinforced Armor (Fort 90)")
        if pre_fort >= 40: unlocked_talents.append("🦴 Exoskeleton (Fort 40)")
        if pre_str >= 80: unlocked_talents.append("💥 Collapsed Lung (Str 80)")
        if pre_str >= 40: unlocked_talents.append("🥊 Showstopper (Str 40)")
        if pre_agi >= 40: unlocked_talents.append("👻 Ghost (Agl 40)")
        if pre_wil >= 50: unlocked_talents.append("🗡️ Giant Slayer (Wil 50)")
        if pre_cha >= 55: unlocked_talents.append("🎭 Chaotic Charm D3 (Cha 55)")
        if pre_fort >= 100 and pre_wil >= 100: unlocked_talents.append("🧱 Brick Wall (Fort 100, Wil 100)")

        if unlocked_talents:
            st.success(f"**⛩️ 사원 전 선행 획득 확정 탤런트:**\n" + " • ".join(unlocked_talents))
        else:
            st.info("💡 사원 전 필요한 핵심 탤런트 수치를 입력하세요.")

    current_stat_dict = post_stat_dict

    # 6. 장비 & 방어구 세팅 (11종 장비 슬롯)
    st.markdown("#### 🛡️ 장비 및 악세서리 세팅 (11종 슬롯)")
    saved_eq = curr_data.get("equipment", {})
    
    eq_col1, eq_col2 = st.columns(2)
    with eq_col1:
        outfit_list = list(OUTFIT_PRESETS.keys())
        saved_outfit = saved_eq.get("outfit", outfit_list[0])
        outfit_idx = outfit_list.index(saved_outfit) if saved_outfit in outfit_list else 0
        selected_outfit = st.selectbox("👔 방어구 (Outfit)", outfit_list, index=outfit_idx, key=f"{selected_name}_outfit")
    with eq_col2:
        weapon_enchant = st.selectbox("✨ 무기 인챈트 (Enchant)", EQUIPMENT_SLOTS_DB["enchants"], index=0 if "Silentheart" in current_oath else 7, key=f"{selected_name}_enchant")

    with st.expander("💍 전체 악세서리 & 방어구 세부 슬롯 (모자, 안경, 귀걸이, 반지 1~4, 신발, 벨)", expanded=False):
        eq_c1, eq_c2 = st.columns(2)
        with eq_c1:
            helmet_names = [h["name"] for h in EQUIPMENT_SLOTS_DB["helmets"]]
            cur_helmet = saved_eq.get("helmet", helmet_names[0])
            sel_helmet = st.selectbox("🪖 머리/모자 (Helmet)", helmet_names, index=helmet_names.index(cur_helmet) if cur_helmet in helmet_names else 0, key=f"{selected_name}_helmet")

            face_names = [f["name"] for f in EQUIPMENT_SLOTS_DB["face"]]
            cur_face = saved_eq.get("face", face_names[0])
            sel_face = st.selectbox("👓 안경/마스크 (Face)", face_names, index=face_names.index(cur_face) if cur_face in face_names else 0, key=f"{selected_name}_face")

            amulet_names = [a["name"] for a in EQUIPMENT_SLOTS_DB["amulets"]]
            cur_amulet = saved_eq.get("amulet", amulet_names[0])
            sel_amulet = st.selectbox("📿 귀걸이/부적 (Amulet)", amulet_names, index=amulet_names.index(cur_amulet) if cur_amulet in amulet_names else 0, key=f"{selected_name}_amulet")

            boot_names = [b["name"] for b in EQUIPMENT_SLOTS_DB["boots"]]
            cur_boots = saved_eq.get("boots", boot_names[0])
            sel_boots = st.selectbox("👢 신발 (Boots)", boot_names, index=boot_names.index(cur_boots) if cur_boots in boot_names else 0, key=f"{selected_name}_boots")

        with eq_c2:
            ring_options = EQUIPMENT_SLOTS_DB["rings"]
            r1 = st.selectbox("💍 반지 1", ring_options, index=ring_options.index(saved_eq.get("ring1", "Ring of Casters (에테르 재생)")) if saved_eq.get("ring1") in ring_options else 0, key=f"{selected_name}_r1")
            r2 = st.selectbox("💍 반지 2", ring_options, index=ring_options.index(saved_eq.get("ring2", "Starved Knight Ring (공격력 증폭)")) if saved_eq.get("ring2") in ring_options else 1, key=f"{selected_name}_r2")
            r3 = st.selectbox("💍 반지 3", ring_options, index=ring_options.index(saved_eq.get("ring3", "Deepwoken Ring of Health (체력 +10)")) if saved_eq.get("ring3") in ring_options else 4, key=f"{selected_name}_r3")
            r4 = st.selectbox("💍 반지 4", ring_options, index=ring_options.index(saved_eq.get("ring4", "None (미착용)")) if saved_eq.get("ring4") in ring_options else 7, key=f"{selected_name}_r4")

        bell_options = EQUIPMENT_SLOTS_DB["bells"]
        cur_bell = saved_eq.get("bell", bell_options[0])
        sel_bell = st.selectbox("🔔 공명 벨 (Resonance Bell)", bell_options, index=bell_options.index(cur_bell) if cur_bell in bell_options else 0, key=f"{selected_name}_bell")

    current_eq_dict = {
        "outfit": selected_outfit,
        "enchant": weapon_enchant,
        "helmet": sel_helmet,
        "face": sel_face,
        "amulet": sel_amulet,
        "boots": sel_boots,
        "ring1": r1, "ring2": r2, "ring3": r3, "ring4": r4,
        "bell": sel_bell,
        "extra_hp": saved_eq.get("extra_hp", 20),
        "extra_dve": saved_eq.get("extra_dve", 10),
    }

    # 7. ⭐ 핵심 탤런트 & 🔮 장착 만트라 (호버 툴팁 인터랙티브 뷰)
    def render_badge(name: str, item_type: str = "talent") -> str:
        clean = name.split("(")[0].strip()
        db = DEEPWOKEN_TALENTS_DB if item_type == "talent" else DEEPWOKEN_MANTRAS_DB
        info = None
        for k, v in db.items():
            if k.lower() in clean.lower() or clean.lower() in k.lower():
                info = v
                break
        if info:
            title_text = info.get("name_ko", clean)
            sub_text = f"📋 <b>요구치:</b> {info.get('req', '기본')}<br>🎯 <b>효과:</b> {info.get('desc', '')}" if item_type == "talent" else f"🏷️ <b>분류:</b> {info.get('category', '만트라')}<br>🎯 <b>효과:</b> {info.get('desc', '')}"
            tag_class = "talent-tag" if item_type == "talent" else "mantra-tag"
            icon = "⭐" if item_type == "talent" else "🔮"
            return f'<div class="deepwoken-tooltip-container"><span class="{tag_class}">{icon} {clean}</span><div class="tooltip-box"><div style="color: #e5b869; font-weight: bold; margin-bottom: 4px;">{title_text}</div><div style="color: #cbd5e1; font-size: 0.8rem;">{sub_text}</div></div></div>'
        else:
            tag_class = "talent-tag" if item_type == "talent" else "mantra-tag"
            icon = "⭐" if item_type == "talent" else "🔮"
            return f'<div class="deepwoken-tooltip-container"><span class="{tag_class}">{icon} {clean}</span><div class="tooltip-box"><div style="color: #e5b869; font-weight: bold; margin-bottom: 4px;">{clean}</div><div style="color: #cbd5e1; font-size: 0.8rem;">Deepwoken 고유 {item_type}입니다.</div></div></div>'

    st.markdown("#### ⭐ 핵심 탤런트 (마우스를 올리면 상세 효과/요구치가 팝업됩니다)")
    current_talents_str = curr_data.get("talents", "")
    
    # 탤런트 호버 칩 렌더링
    talent_tokens = [t.strip() for t in current_talents_str.replace("•", ",").split(",") if t.strip()]
    talent_badges_html = [render_badge(t_raw, "talent") for t_raw in talent_tokens]
    if talent_badges_html:
        st.markdown(f'<div style="margin-bottom: 8px;">{"".join(talent_badges_html)}</div>', unsafe_allow_html=True)
    
    talents_input = st.text_input("✏️ 탤런트 직접 편집 (쉼표로 구분):", value=current_talents_str, key=f"{selected_name}_talents")

    st.markdown("#### 🔮 장착 만트라 (마우스를 올리면 상세 효과/계열이 팝업됩니다)")
    current_mantras_str = curr_data.get("mantras", "")
    mantra_tokens = [m.strip() for m in current_mantras_str.replace("•", ",").split(",") if m.strip()]
    mantra_badges_html = [render_badge(m_raw, "mantra") for m_raw in mantra_tokens]
    if mantra_badges_html:
        st.markdown(f'<div style="margin-bottom: 8px;">{"".join(mantra_badges_html)}</div>', unsafe_allow_html=True)
        
    mantras_input = st.text_input("✏️ 만트라 직접 편집 (쉼표로 구분):", value=current_mantras_str, key=f"{selected_name}_mantras")

    # 8. 🧮 실시간 종합 계산기 (STATS & RESISTANCES Dashboard)
    char_sheet = DeepwokenCalculator.calculate_character_sheet(
        race=selected_race,
        stats=current_stat_dict,
        traits={"Vitality": vit_val, "Erudition": eru_val, "Proficiency": pro_val, "Songchant": son_val},
        equipment=current_eq_dict,
        talents_str=talents_input
    )
    computed_stats = char_sheet["stats"]
    computed_res = char_sheet["resistances"]

    st.markdown("---")
    st.markdown("#### 📈 최종 종합 능력치 (STATS)")
    stat_c1, stat_c2, stat_c3, stat_c4 = st.columns(4)
    stat_c1.metric("❤️ Max HP", f"{computed_stats['health']} HP")
    stat_c2.metric("🛡️ Posture", f"{computed_stats['posture']}")
    stat_c3.metric("💠 Ether", f"{computed_stats['ether']}")
    stat_c4.metric("⏩ Tempo", f"{computed_stats['tempo']}")

    stat_c5, stat_c6 = st.columns(2)
    stat_c5.metric("🗡️ PvE 딜증 (Dmg vs Monsters)", f"+{computed_stats['pve_dmg_pct']}%")
    stat_c6.metric("🏃 이동 속도 (Speed)", f"{computed_stats['speed_pct']}%")

    st.markdown("#### 🛡️ 최종 저항력 (RESISTANCES)")
    res_c1, res_c2, res_c3, res_c4 = st.columns(4)
    res_c1.metric("🛡️ 물리 저항", f"{computed_res['slash']}%")
    res_c2.metric("🔥 화염 저항", f"{computed_res['flame']}%")
    res_c3.metric("❄️ 빙결 저항", f"{computed_res['frost']}%")
    res_c4.metric("⚡ 번개 저항", f"{computed_res['thunder']}%")

    # 저장 버튼
    if st.button("💾 현재 캐릭터 프로필 저장", use_container_width=True, key=f"{selected_name}_save_btn"):
        st.session_state.profiles[selected_name] = {
            "name": selected_name,
            "race": selected_race,
            "oath": current_oath,
            "weapon_type": weapon_type,
            "attunement": main_attunement,
            "traits": {"Vitality": vit_val, "Erudition": eru_val, "Proficiency": pro_val, "Songchant": son_val},
            "pre_shrine": pre_stat_dict,
            "stats": post_stat_dict,
            "equipment": current_eq_dict,
            "mantras": mantras_input,
            "talents": talents_input
        }
        save_user_profiles(st.session_state.profiles)
        st.success(f"'{selected_name}' 프로필(11종 장비, 사원 전/후 스탯, 특성, 저항력)이 안전하게 저장되었습니다! ✅")

    # 📥 / 📤 deepwoken.co 공식 빌더 JSON 강제 주입 및 내보내기 도구
    with st.expander("🛠️ deepwoken.co 공식 빌더 JSON 주입(Import) & 내보내기(Export)", expanded=False):
        st.caption("외부 deepwoken.co 빌더의 JSON 코드를 복사해 붙여넣으면 현재 슬롯에 강제로 즉시 주입됩니다.")
        
        # 1. JSON 강제 주입
        import_text = st.text_area("📥 주입할 deepwoken.co JSON 코드 붙여넣기:", height=100, placeholder='{"stats": {"Strength": 40, ...}, "oath": "Silentheart", ...}', key="json_import_area")
        if st.button("🚀 현재 슬롯에 JSON 강제 주입 실행", key="btn_execute_import"):
            if import_text.strip():
                try:
                    parsed_json = json.loads(import_text.strip())
                    if isinstance(parsed_json, list) and len(parsed_json) > 0:
                        parsed_json = parsed_json[0]
                    if not isinstance(parsed_json, dict):
                        raise ValueError("JSON 데이터는 객체(Dictionary) 형태여야 합니다.")

                    target_p = st.session_state.profiles[selected_name]
                    target_p.setdefault("stats", {})
                    target_p.setdefault("pre_shrine", {})
                    target_p.setdefault("equipment", {})
                    target_p.setdefault("traits", {"Vitality": 6, "Erudition": 6, "Proficiency": 0, "Songchant": 0})

                    # Stats 매핑
                    stats_src = parsed_json.get("stats") or parsed_json.get("attributes") or parsed_json.get("post_shrine") or {}
                    if isinstance(stats_src, dict):
                        for k, v in stats_src.items():
                            try: target_p["stats"][k] = int(v)
                            except (ValueError, TypeError): pass

                    # Pre-Shrine 매핑
                    pre_src = parsed_json.get("pre_shrine") or parsed_json.get("preShrine") or {}
                    if isinstance(pre_src, dict):
                        for k, v in pre_src.items():
                            try: target_p["pre_shrine"][k] = int(v)
                            except (ValueError, TypeError): pass

                    # 기본 메타데이터
                    if "oath" in parsed_json: target_p["oath"] = str(parsed_json["oath"])
                    if "race" in parsed_json: target_p["race"] = str(parsed_json["race"])
                    if "weapon_type" in parsed_json or "weaponType" in parsed_json or "weapon" in parsed_json:
                        target_p["weapon_type"] = str(parsed_json.get("weapon_type") or parsed_json.get("weaponType") or parsed_json.get("weapon"))
                    if "attunement" in parsed_json: target_p["attunement"] = str(parsed_json["attunement"])

                    # Traits 매핑
                    traits_src = parsed_json.get("traits") or {}
                    if isinstance(traits_src, dict):
                        for k, v in traits_src.items():
                            try: target_p["traits"][k] = int(v)
                            except (ValueError, TypeError): pass

                    # Equipment 매핑
                    eq_src = parsed_json.get("equipment")
                    if isinstance(eq_src, dict):
                        target_p["equipment"].update(eq_src)
                    elif isinstance(eq_src, str):
                        target_p["equipment"]["outfit"] = eq_src

                    for eq_key in ["outfit", "helmet", "face", "amulet", "boots", "ring1", "ring2", "ring3", "ring4", "bell", "enchant"]:
                        if eq_key in parsed_json:
                            target_p["equipment"][eq_key] = parsed_json[eq_key]

                    # Talents & Mantras 매핑
                    talents_src = parsed_json.get("talents") or parsed_json.get("selectedTalents") or parsed_json.get("talentList")
                    if isinstance(talents_src, list):
                        target_p["talents"] = ", ".join([str(t) for t in talents_src])
                    elif talents_src is not None:
                        target_p["talents"] = str(talents_src)

                    mantras_src = parsed_json.get("mantras") or parsed_json.get("selectedMantras") or parsed_json.get("mantraList")
                    if isinstance(mantras_src, list):
                        target_p["mantras"] = ", ".join([str(m) for m in mantras_src])
                    elif mantras_src is not None:
                        target_p["mantras"] = str(mantras_src)
                    
                    save_user_profiles(st.session_state.profiles)
                    st.success("✅ deepwoken.co 빌드 JSON이 현재 슬롯에 성공적으로 주입되었습니다!")
                    st.rerun()
                except Exception as ex:
                    st.error(f"❌ JSON 파싱 실패: {ex}")

        # 3. NotebookLM 1-Click 전수 감사 프롬프트 생성기 & Google Drive 동기화
        st.markdown("---")
        st.markdown("##### 🤖 Google NotebookLM 1-Click `/build` 전수 감사 & 드라이브 동기화")
        st.caption("아래 코드를 복사해서 NotebookLM에 붙여넣으면, 소스에 기반해 현재 슬롯의 종족, 서약, 11대 장비, 330pt 스탯, EHP를 하나도 빠짐없이 1:1 전수 감사를 진행합니다.")

        if st.button("📂 Google Drive로 즉시 동기화 (G:\\내 드라이브\\Deepwoken)", key="btn_sync_gdrive_web"):
            from agents.gdrive_sync import sync_to_google_drive
            ok, gmsg, gfiles = sync_to_google_drive()
            if ok:
                st.success(f"✅ {gmsg} (NotebookLM에서 최신 구글 드라이브 소스를 즉시 불러올 수 있습니다!)")
            else:
                st.warning(f"⚠️ {gmsg}")
        
        prof_data = st.session_state.profiles[selected_name]
        notebooklm_prompt = f"""[역할 부여]
너는 딥위큰(Deepwoken) 공식 1,043개 탤런트와 330pt 수학적 공식, Shrine of Order 룰을 완벽히 꿰뚫고 있는 세계 최고 실력의 전담 AI 빌드 코치야.

[현재 내 캐릭터 빌드 명세서]
- 🏷️ 캐릭터 빌드명: {prof_data.get('name')}
- 🧬 종족 (Aspect/Race): {prof_data.get('race', 'Vesperian')}
- ⚔️ 서약 (Oath): {prof_data.get('oath', 'Oathless')}
- 🗡️ 주무기군: {prof_data.get('weapon_type')}
- ✨ 주속성 (Attunement): {prof_data.get('attunement')}
- 🌟 4대 특성 (Traits): {prof_data.get('traits', {})}
- ⛩️ 사원 전 (Pre-Shrine) 1차 스탯: {prof_data.get('pre_shrine', {})}
- 📊 사원 후 (Post-Shrine) 최종 스탯: {prof_data.get('stats', {})}
- 🛡️ 11대 장비 세팅: {prof_data.get('equipment', {})}
- ⭐ 목표/보유 탤런트: {prof_data.get('talents')}
- 🔮 장착 만트라: {prof_data.get('mantras')}

[명령어: /build 전수 감사 실행]
위 내 캐릭터 빌드를 소스에 근거하여 다음 6단계로 하나도 빠짐없이 1:1 전수 감사를 진행해줘:
1. 🧬 종족 & 서약 적합성 (종족 기본치 보존 및 Oath 선행 조건 충족 여부)
2. 🏛️ 스탯 및 성소(Shrine of Order) 무결성 (사원 전 탤런트 획득 가능 여부 & 사원 후 정확히 330pt 일치 검증)
3. ⭐ 탤런트 & 만트라 시너지 감사 (누락되거나 낭비된 탤런트, 중복/비효율 점검)
4. 🛡️ 11대 장비 & 인챈트 & 유효 체력(EHP) 및 속성 저항력 평가
5. 🐲 보스별 실전 사냥법 & 딜 사이클 (Duke, Primadon, Chaser, Ethiron)
6. 💡 총평 및 1티어 종결 빌드로 완성하기 위한 최종 보완책 3가지"""
        st.code(notebooklm_prompt, language="markdown")
        
        # deepwoken.co 호환 localStorage 인젝션 스크립트 생성
        js_inject_code = f"localStorage.setItem('saved_build', JSON.stringify({json.dumps(st.session_state.profiles[selected_name])})); alert('Deepwoken 빌드가 성공적으로 주입되었습니다!'); location.reload();"
        st.code(js_inject_code, language="javascript")

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
    if quick_cols[2].button("🏛️ Shrine of Order"):
        quick_q = "내 현재 목표 스탯을 맞추기 위해 Shrine of Order를 타기 전(Pre-Shrine)과 탄 후(Post-Shrine) 어떤 순서로 스탯을 찍어야 하는지 최적의 루트를 계산해줘."
    if quick_cols[3].button("🔍 /build 전수 감사"):
        quick_q = "/build 내 현재 종족, 특성, 사원 전/후 스탯, 탤런트, 만트라, 11대 장비 세팅을 빠짐없이 하나하나 전수 조사해서 이상한 점과 EHP 극대화 보완책을 상세히 감사해줘."

    # 사용자 질문 입력창
    user_input = st.chat_input("질문을 입력하세요 (예: 듀크 딜 타임 때 어떤 콤보를 써야 해?)...")
    prompt_to_send = quick_q or user_input

    # 채팅 메시지 전용 독립 스크롤 박스 (Fixed-Height Scroll Container)
    chat_container = st.container(height=560)
    with chat_container:
        if not st.session_state.chat_history and not prompt_to_send:
            st.markdown("""
            <div class="chat-assistant">
            🤖 <b>Deepwoken AI Coach</b>: 안녕하세요! 현재 좌측에 설정하신 <b>캐릭터 빌드(사원 전/후 스탯 포함)</b>를 완벽하게 파악하고 있습니다.<br>
            보스별 그로기 딜 사이클, 만트라 연계 순서, Shrine of Order 스탯 육성법 등 무엇이든 물어보세요!
            </div>
            """, unsafe_allow_html=True)
        else:
            for turn in st.session_state.chat_history:
                if turn["role"] == "user":
                    st.markdown(f'<div class="chat-user">👤 <b>나:</b> {turn["content"]}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="chat-assistant">🤖 <b>AI 코치:</b><br>{turn["content"]}</div>', unsafe_allow_html=True)

        # 새 질문 입력 시 즉시 화면에 내 질문 말풍선을 띄우고 답변 생성
        if prompt_to_send:
            st.markdown(f'<div class="chat-user">👤 <b>나:</b> {prompt_to_send}</div>', unsafe_allow_html=True)
            st.session_state.chat_history.append({"role": "user", "content": prompt_to_send})
            
            profile_context = (
                f"[현재 사용자 캐릭터 프로필]\n"
                f"- 빌드명: {active_profile.get('name')}\n"
                f"- 종족(Aspect/Race): {active_profile.get('race', 'Vesperian')}\n"
                f"- Oath: {active_profile.get('oath')}\n"
                f"- 주무기: {active_profile.get('weapon_type')}\n"
                f"- 주속성: {active_profile.get('attunement')}\n"
                f"- 4대 특성(Traits): {active_profile.get('traits', {})}\n"
                f"- ⛩️ 사원 전(Pre-Shrine) 1차 스탯: {active_profile.get('pre_shrine', {})}\n"
                f"- 📊 사원 후(Post-Shrine) 최종 스탯: {active_profile.get('stats', {})}\n"
                f"- 장비/인챈트: {active_profile.get('equipment', {})}\n"
                f"- 최종 산출 수치(STATS): Max HP: {computed_stats['health']}, Posture: {computed_stats['posture']}, Ether: {computed_stats['ether']}, Tempo: {computed_stats['tempo']}, PvE 보스딜: +{computed_stats['pve_dmg_pct']}%\n"
                f"- 최종 저항력(RESISTANCES): 물리 {computed_res['slash']}%, 화염 {computed_res['flame']}%, 빙결 {computed_res['frost']}%, 번개 {computed_res['thunder']}%\n"
                f"- 장착 만트라: {active_profile.get('mantras')}\n"
                f"- 장착/목표 탤런트: {active_profile.get('talents')}\n"
            )
            full_query = f"{profile_context}\n[사용자 질문]\n{prompt_to_send}"
            
            with st.spinner("🧠 깃허브 지식 베이스 검색 & 팩트체크 검증 중..."):
                raw_advice = st.session_state.advisor.answer_query(
                    user_query=full_query,
                    history=st.session_state.chat_history[:-1]
                )
                audit_result = DeepwokenFactChecker.audit_profile_and_advice(active_profile, raw_advice)
                verification_badge = DeepwokenFactChecker.generate_verification_badge(audit_result)
                
                final_response = raw_advice + "\n" + verification_badge
                st.session_state.chat_history.append({"role": "assistant", "content": final_response})
                save_chat_history(st.session_state.chat_history)
                st.rerun()

    # 대화 초기화 버튼
    if st.button("🧹 대화 기억 초기화"):
        st.session_state.chat_history = []
        save_chat_history([])
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
