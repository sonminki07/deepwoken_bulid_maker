import os
import json
import time
from pathlib import Path
from typing import Dict, Any, List
import streamlit as st

# 로컬 백엔드 모듈 임포트
from chatbot.build_advisor import BuildAdvisor
from chatbot.coach_validator import DeepwokenFactChecker, TALENT_PREREQUISITES, OATH_PREREQUISITES
from chatbot.builder_calculator import DeepwokenCalculator, DEEPWOKEN_RACES, OUTFIT_PRESETS
from chatbot.deepwoken_database import DEEPWOKEN_TALENTS_DB, DEEPWOKEN_MANTRAS_DB

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

    /* 탤런트 & 만트라 호버 툴팁 태그 */
    .talent-tag {
        display: inline-block;
        background: linear-gradient(135deg, rgba(234, 88, 12, 0.18), rgba(245, 158, 11, 0.12));
        border: 1px solid rgba(245, 158, 11, 0.5);
        color: #fde68a;
        padding: 5px 11px;
        border-radius: 7px;
        margin: 3px;
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
        margin: 3px;
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
    with tab_post:
        st.caption("✨ 질서의 성소(Shrine of Order)로 스탯을 재분배한 뒤 최종 20레벨까지 완성한 최종 스탯입니다.")
        s_col1, s_col2, s_col3 = st.columns(3)
        with s_col1:
            str_val = st.number_input("Strength (근력)", 0, 102, int(saved_post.get("Strength", 0)), key=f"{selected_name}_str")
            fort_val = st.number_input("Fortitude (인내)", 0, 102, int(saved_post.get("Fortitude", 0)), key=f"{selected_name}_fort")
        with s_col2:
            agi_val = st.number_input("Agility (민첩)", 0, 102, int(saved_post.get("Agility", 0)), key=f"{selected_name}_agi")
            int_val = st.number_input("Intelligence (지능)", 0, 102, int(saved_post.get("Intelligence", 0)), key=f"{selected_name}_int")
        with s_col3:
            wil_val = st.number_input("Willpower (의지)", 0, 102, int(saved_post.get("Willpower", 0)), key=f"{selected_name}_wil")
            cha_val = st.number_input("Charisma (매력)", 0, 102, int(saved_post.get("Charisma", 0)), key=f"{selected_name}_cha")

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

        if total_stat_points <= max_cap:
            st.markdown(f'<div class="stat-badge-ok">📊 최종 스탯 총합: {total_stat_points} / {max_cap} pt (공식 룰 100% 일치 ✅)</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="stat-badge-warn">⚠️ 최종 스탯 초과: {total_stat_points} / {max_cap} pt (+{total_stat_points - max_cap}pt 초과)</div>', unsafe_allow_html=True)

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

    # 6. 장비 & 방어구 세팅 (Equipment)
    st.markdown("#### 🛡️ 장비 및 방어구 세팅 (Equipment)")
    saved_eq = curr_data.get("equipment", {})
    eq_col1, eq_col2 = st.columns(2)
    with eq_col1:
        outfit_list = list(OUTFIT_PRESETS.keys())
        saved_outfit = saved_eq.get("outfit", outfit_list[0])
        outfit_idx = outfit_list.index(saved_outfit) if saved_outfit in outfit_list else 0
        selected_outfit = st.selectbox("👔 방어구 (Outfit)", outfit_list, index=outfit_idx, key=f"{selected_name}_outfit")
    with eq_col2:
        weapon_enchant = st.selectbox("✨ 무기 인챈트 (Enchant)", ["None", "Detonation (폭발 딜)", "Astral (하얀 오라/물리)", "Vampirism (흡혈)", "Chilling (동결)", "Blazing (화염)", "Grim (피해량 증폭)"], index=1 if "Silentheart" in current_oath else 0, key=f"{selected_name}_enchant")

    current_eq_dict = {
        "outfit": selected_outfit,
        "enchant": weapon_enchant,
        "extra_hp": saved_eq.get("extra_hp", 20),
        "extra_dve": saved_eq.get("extra_dve", 10),
    }

    # 7. ⭐ 핵심 탤런트 & 🔮 장착 만트라 (호버 툴팁 인터랙티브 뷰)
    st.markdown("#### ⭐ 핵심 탤런트 (마우스를 올리면 상세 효과/요구치가 표시됩니다)")
    current_talents_str = curr_data.get("talents", "")
    
    # 탤런트 호버 칩 렌더링
    talent_tokens = [t.strip() for t in current_talents_str.replace("•", ",").split(",") if t.strip()]
    talent_badges_html = []
    for t_raw in talent_tokens:
        clean_name = t_raw.split("(")[0].strip()
        matched_info = None
        for db_name, db_info in DEEPWOKEN_TALENTS_DB.items():
            if db_name.lower() in clean_name.lower() or clean_name.lower() in db_name.lower():
                matched_info = db_info
                break
        
        if matched_info:
            tooltip = f"[{matched_info['name_ko']}]\n📋 요구치: {matched_info['req']}\n🎯 효과: {matched_info['desc']}"
            talent_badges_html.append(f'<span class="talent-tag" title="{tooltip}">⭐ {clean_name}</span>')
        else:
            talent_badges_html.append(f'<span class="talent-tag" title="Deepwoken 고유 패시브 탤런트">⭐ {clean_name}</span>')
    
    if talent_badges_html:
        st.markdown("".join(talent_badges_html), unsafe_allow_html=True)
    
    talents_input = st.text_input("✏️ 탤런트 직접 편집 (쉼표로 구분):", value=current_talents_str, key=f"{selected_name}_talents")

    st.markdown("#### 🔮 장착 만트라 (마우스를 올리면 상세 효과/계열이 표시됩니다)")
    current_mantras_str = curr_data.get("mantras", "")
    mantra_tokens = [m.strip() for m in current_mantras_str.replace("•", ",").split(",") if m.strip()]
    mantra_badges_html = []
    for m_raw in mantra_tokens:
        clean_name = m_raw.split("(")[0].strip()
        matched_info = None
        for db_name, db_info in DEEPWOKEN_MANTRAS_DB.items():
            if db_name.lower() in clean_name.lower() or clean_name.lower() in db_name.lower():
                matched_info = db_info
                break
        
        if matched_info:
            tooltip = f"[{matched_info['name_ko']}]\n🏷️ 분류: {matched_info['category']}\n🎯 효과: {matched_info['desc']}"
            mantra_badges_html.append(f'<span class="mantra-tag" title="{tooltip}">🔮 {clean_name}</span>')
        else:
            mantra_badges_html.append(f'<span class="mantra-tag" title="Deepwoken 전투 액티브 스킬/만트라">🔮 {clean_name}</span>')
    
    if mantra_badges_html:
        st.markdown("".join(mantra_badges_html), unsafe_allow_html=True)
        
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
        st.success(f"'{selected_name}' 프로필(사원 전/후 스탯, 종족, 특성, 장비, 저항력)이 안전하게 저장되었습니다! ✅")

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
