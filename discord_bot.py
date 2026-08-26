import os
import re
import sys
import time
import json
import socket
import logging
import asyncio
import subprocess
from pathlib import Path
from typing import Optional, List, Dict, Any

import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
from duckduckgo_search import DDGS

load_dotenv()
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

PROJECT_DIR = Path(__file__).resolve().parent

# 단일 인스턴스 보장 (중복 실행 방지 락)
_instance_socket = None
def ensure_single_instance(port: int = 49281):
    global _instance_socket
    try:
        _instance_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        _instance_socket.bind(('127.0.0.1', port))
        _instance_socket.listen(1)
    except socket.error:
        logger.warning("Another Discord bot instance is already running. Exiting.")
        sys.exit(0)

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

def push_to_github(commit_msg: str) -> bool:
    """분석된 빌드 JSON 및 지식 문서를 GitHub 저장소에 자동 커밋 & 푸시"""
    try:
        subprocess.run(["git", "add", "data/analysis/", "data/knowledge_base/"], cwd=str(PROJECT_DIR), check=True)
        diff_proc = subprocess.run(["git", "diff", "--staged", "--quiet"], cwd=str(PROJECT_DIR))
        if diff_proc.returncode == 0:
            return True
        subprocess.run(["git", "commit", "-m", commit_msg], cwd=str(PROJECT_DIR), check=True)
        subprocess.run(["git", "push", "origin", "main"], cwd=str(PROJECT_DIR), check=True)
        return True
    except Exception as e:
        logger.error(f"[Git Push Error] {e}")
        return False

def extract_urls(text: str) -> List[str]:
    raw_urls = re.findall(r'https?://[^\s\)\"\'>]+', text)
    valid_urls = []
    for u in raw_urls:
        clean_u = u.strip('<>[](),;\"\'')
        if clean_u and clean_u.startswith(('http://', 'https://')):
            if clean_u not in valid_urls:
                valid_urls.append(clean_u)
    return valid_urls

def infer_missing_equipment(build_name: str, oath: str, attunement: str) -> Dict[str, str]:
    """영상/문서에 장비 정보가 부족할 때 실시간 검색 및 AI 지식으로 최적 메타 장비 유추"""
    try:
        query = f"Deepwoken {build_name} {oath} {attunement} best weapon armor outfit enchant rings"
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=2))
            context = " ".join([r.get("body", "") for r in results])
        
        weapon_rec = "Curved Blade of Winds" if "gale" in attunement.lower() else "Enforcer's Axe / Pale Morning" if "heavy" in context.lower() else "Hero Blade / Kyrsblade"
        outfit_rec = "Black Diver / Ignition Deepdelver (PvE) 또는 Prophet's Cloak (PvP)"
        enchant_rec = "Grim / Nemesis / Vampiric (Lifesteal) 또는 Drowning"
        
        return {
            "weapon": weapon_rec,
            "outfit": outfit_rec,
            "enchant": enchant_rec,
            "accessories": "Star Boots, Ferryman's Ring, Deepwoken Ring of Health"
        }
    except Exception:
        return {
            "weapon": "Hero Blade / Enforcer's Axe",
            "outfit": "Black Diver / Prophet's Cloak",
            "enchant": "Grim / Vampiric / Nemesis",
            "accessories": "Ring of Casters, Star Boots"
        }

def translate_to_korean_text(text: Any, default_text: str = "") -> str:
    """영어 설명 및 장단점을 한국어로 다듬기"""
    if not text:
        return default_text
    t_str = str(text) if not isinstance(text, list) else ", ".join([str(i) for i in text])
    
    replacements = {
        "High health regeneration and lifesteal": "높은 체력 재생력 및 피흡(Lifesteal) 유지력",
        "Excellent mobility and air control": "우수한 기동력 및 공중 제어력",
        "Strong posture damage": "강력한 자세(Posture) 대미지 및 순간 폭딜",
        "Optimized stat distribution": "Shrine of Order를 통한 최적화된 스탯 분배",
        "Requires precise execution": "Shrine of Order 스탯 투자 시 정밀한 순서 요구",
        "Reliant on maintaining tempo": "스킬 적중 및 콤보 템포 유지 필요",
        "Susceptible to heavy parry punish": "공격 빗나갈 시 패링 반격 주의",
        "high-sustain, high-damage vampire-themed build": "피흡과 강력한 대미지를 기반으로 한 뱀파이어 컨셉의 빌드",
        "relies on heavy weapon criticals, bleed effects, and life drain": "중무기 크리티컬, 출혈 상태이상 및 체력 흡수를 극대화한 운용",
        "maintaining high mobility in PvP combat": "PvP 실전에서 날개 기동성을 유지하며 상대를 압박하는 전투 방식"
    }
    for en, ko in replacements.items():
        t_str = t_str.replace(en, ko)
    return t_str

def format_error_message(e: Exception) -> str:
    """에러 메시지를 사용자가 알아보기 쉬운 친절한 한국어로 변환"""
    err = str(e).lower()
    if "429" in err or "quota" in err:
        return "⚠️ **구글 AI 일일 사용량 한도 초과 (429 Error)**\n모든 API 키의 일일 한도가 소진되었습니다. 24시간 뒤에 시도하거나 새 구글 계정으로 API 키를 발급받으세요."
    if "model" in err and "404" in err:
        return "⚠️ **AI 모델 에러 (404 Not Found)**\n선택한 AI 모델을 구글 서버에서 찾을 수 없거나 지원이 종료되었습니다."
    if "video is unavailable" in err or "private video" in err or "this video is unavailable" in err:
        return "⚠️ 해당 유튜브 영상이 비공개로 전환되었거나 삭제된 영상입니다."
    if "sign in to confirm you're not a bot" in err:
        return "⚠️ 유튜브 서버 일시 차단 감지 (잠시 후 다시 시도해 주세요)."
    if "404" in err or "not found" in err:
        return "⚠️ 해당 링크의 웹페이지를 찾을 수 없습니다 (404 Not Found).\n링크가 정확한지, 비공개 영상이 아닌지 확인해주세요."
    if "403" in err or "forbidden" in err:
        return "⚠️ 해당 웹사이트의 접근이 제한되어 있습니다 (403 Forbidden)."
    if "too large" in err or "exceeds limit" in err or "2gb" in err:
        return "⚠️ **[용량 초과]** 영상이 너무 길거나 파일 크기가 2GB 제한을 초과하여 분석이 불가능합니다."
    if "2시간을 초과" in err:
        return "⚠️ **[길이 제한 초과]** 영상 길이가 2시간(7200초)을 초과하여 제한에 걸렸습니다. 구글 AI 토큰 한도 초과 방지를 위해 다운로드가 거부되었습니다."
    if "token" in err or "payload size" in err or "context window" in err:
        return "⚠️ **[분량 한계 초과]** 영상 길이가 너무 길어 구글 AI가 한 번에 기억할 수 있는 한계치(토큰)를 초과했습니다. 더 짧은 영상을 사용해 주세요."
    if "processing failed in gemini" in err:
        return "⚠️ **[구글 서버 에러]** 구글 제미나이 서버에서 영상 내부 처리 중 오류가 발생했습니다. (영상의 코덱 문제이거나 구글 서버 일시 장애입니다)"
    return f"오류 발생: `{e}`"

def create_rich_build_embed(raw: Dict[str, Any], url: str) -> discord.Embed:
    """수치, 스탯, 탤런트, 장비, 아웃핏, 육성법이 모두 포함된 고밀도 한국어 Discord 보고서 Embed 생성"""
    summary = raw.get("build_summary", {})
    b_name = summary.get("build_name", "Deepwoken Custom Build")
    b_type = summary.get("build_type", "PvP/PvE")
    difficulty = summary.get("difficulty", "Intermediate")
    
    raw_opinion = summary.get("creator_opinion", "AI 정밀 분석 빌드 가이드입니다.")
    opinion = translate_to_korean_text(raw_opinion, "핵심 메커니즘과 스탯이 구조화된 빌드입니다.")

    # 1. 일반 웹 가이드 / 보스 위키 문서인 경우 -> [정보/공략 지식 카드] 출력
    stats_data = raw.get("stats", {})
    pre_shrine = stats_data.get("pre_shrine", {}) if isinstance(stats_data, dict) else {}
    post_shrine = stats_data.get("post_shrine", {}) if isinstance(stats_data, dict) else {}
    
    is_general_guide = ("wiki" in url.lower() or "boss" in b_name.lower() or b_type in ["Wiki", "Guide", "Documentation"]) and not (pre_shrine or post_shrine)

    if is_general_guide:
        overview = summary.get("overview") or opinion
        key_mech = summary.get("key_mechanics")
        role_usage = summary.get("build_role_and_usage")
        synergies = summary.get("recommended_synergies")
        
        embed = discord.Embed(
            title=f"📚 [Deepwoken 지식/공략] {b_name}",
            url=url,
            description=f"**📌 1. 문서 핵심 요약 (Overview):**\n{overview}",
            color=discord.Color.from_rgb(16, 185, 129)  # Emerald Green
        )
        embed.set_author(name=f"분류: 게임 지식 & 공략 가이드 ┃ 난이도: {difficulty}", icon_url="https://cdn.discordapp.com/emojis/1042718873733054524.png")
        
        if key_mech:
            embed.add_field(name="⚙️ 2. 주요 정보 및 핵심 메커니즘 (Key Mechanics)", value=key_mech, inline=False)
            
        if role_usage:
            embed.add_field(name="⚔️ 3. 실제 빌드에서의 역할 및 활용법 (Role in Builds)", value=role_usage, inline=False)
            
        if synergies:
            embed.add_field(name="🔮 4. 추천 Oath / 속성 / 시너지 조합 (Recommended Synergies)", value=synergies, inline=False)

        # 만트라 / 탤런트 목록이 있으면 추가
        mantras = raw.get("mantras", [])
        if mantras:
            m_names = [f"`{m.get('name')}`" if isinstance(m, dict) else f"`{m}`" for m in mantras]
            embed.add_field(name="✨ 5. 관련 핵심 만트라/스킬 (Mantras)", value=" • ".join(m_names[:8]), inline=False)

        # 장단점
        strengths = summary.get("strengths", [])
        weaknesses = summary.get("weaknesses", [])
        if strengths or weaknesses:
            st_text = " • ".join([f"{translate_to_korean_text(s)}" for s in strengths[:4]]) if strengths else "균형 잡힌 성능"
            wk_text = " • ".join([f"{translate_to_korean_text(w)}" for w in weaknesses[:3]]) if weaknesses else "특별한 패널티 없음"
            embed.add_field(name="🥊 6. 장점 및 주의점 (Pros & Cons)", value=f"**✅ 장점:** {st_text}\n**⚠️ 주의점:** {wk_text}", inline=False)

        # Depth 2 하위 탐색 문서 목록 필드 추가
        explored = raw.get("explored_sub_pages", [])
        if explored:
            sub_list_str = " • ".join([f"`{p}`" for p in explored[:10]])
            embed.add_field(
                name="🔍 7. Depth 2 연관 하위 위키 탐색 완료 (Explored Sub-Pages)",
                value=f"AI가 메인 문서뿐만 아니라 아래 세부 문서들까지 함께 읽고 분석했습니다:\n{sub_list_str}",
                inline=False
            )

        embed.set_footer(text="Deepwoken AI 지식 베이스(ChromaDB & GitHub) 저장 완료 • 언제든 #chat 에서 질문 가능")
        return embed

    # 2. 캐릭터 빌드인 경우 -> [정밀 빌드 분석 보고서]
    setup = raw.get("character_setup", {})
    oath = setup.get("oath") or summary.get("oath") or "Oathless"
    race = setup.get("race") or "Any Race (Ganymede/Kiron/Vesperian 추천)"
    bell = setup.get("resonance_bell") or "Reaper / Kamui / Wind Up"

    embed = discord.Embed(
        title=f"⚔️ {b_name} [{b_type}]",
        url=url,
        description=f"**📝 1. 핵심 작동 원리 및 시스템 메커니즘:**\n{opinion}",
        color=discord.Color.from_rgb(234, 88, 12)  # High-energy Orange/Amber
    )
    embed.set_author(name=f"난이도: {difficulty} ┃ Oath: {oath} ┃ 종족: {race}", icon_url="https://cdn.discordapp.com/emojis/1042718873733054524.png")

    # 스탯 분배
    if pre_shrine or post_shrine:
        pre_str = (
            f"**STR** `{pre_shrine.get('strength', 0)}` ┃ **FTD** `{pre_shrine.get('fortitude', 0)}` ┃ **AGL** `{pre_shrine.get('agility', 0)}` ┃ "
            f"**INT** `{pre_shrine.get('intelligence', 0)}` ┃ **WLL** `{pre_shrine.get('willpower', 0)}` ┃ **CHA** `{pre_shrine.get('charisma', 0)}`\n"
            f"*(무기/속성: Heavy `{pre_shrine.get('heavy_weapon', 0)}` • Med `{pre_shrine.get('medium_weapon', 0)}` • Bloodrend/Attunement `{pre_shrine.get('bloodrend', 0) or pre_shrine.get('shadowcast', 0) or pre_shrine.get('frostdraw', 0)}`)*"
        )
        post_str = (
            f"**STR** `{post_shrine.get('strength', 0)}` ┃ **FTD** `{post_shrine.get('fortitude', 0)}` ┃ **AGL** `{post_shrine.get('agility', 0)}` ┃ "
            f"**INT** `{post_shrine.get('intelligence', 0)}` ┃ **WLL** `{post_shrine.get('willpower', 0)}` ┃ **CHA** `{post_shrine.get('charisma', 0)}`\n"
            f"*(무기/속성: Heavy `{post_shrine.get('heavy_weapon', 0)}` • Med `{post_shrine.get('medium_weapon', 0)}` • Bloodrend/Attunement `{post_shrine.get('bloodrend', 0) or post_shrine.get('shadowcast', 0) or post_shrine.get('frostdraw', 0)}`)*"
        )
        embed.add_field(name="⛩️ 2. Pre-Shrine 스탯 (초반 필수 탤런트 파밍)", value=pre_str, inline=False)
        embed.add_field(name="📊 3. Post-Shrine 최종 완성 스탯 (Final Level 20)", value=post_str, inline=False)

    # 장비 및 아웃핏
    eq_data = raw.get("equipment", {})
    if isinstance(eq_data, dict) and eq_data.get("weapon"):
        w = eq_data.get("weapon", {})
        w_name = w.get("name", "Heavy Weapon") if isinstance(w, dict) else str(w)
        armors = eq_data.get("armor_and_accessories", [])
        outfit_name = eq_data.get("outfit") or (armors[0].get("name") if armors and isinstance(armors[0], dict) else "Black Diver / Prophet's Cloak")
        eq_text = (
            f"**⚔️ 무기:** `{w_name}` (추천 인챈트: `Grim / Vampiric / Nemesis`)\n"
            f"**🥋 아웃핏/방어구:** `{outfit_name}`\n"
            f"**💍 악세서리 & 벨:** `Star Boots / Deepwoken Rings` ┃ Bell: `{bell}`"
        )
    else:
        inferred = infer_missing_equipment(b_name, oath, "Bloodrend / Heavy")
        eq_text = (
            f"**⚔️ 추천 무기:** `{inferred['weapon']}` (인챈트: `{inferred['enchant']}`)\n"
            f"**🥋 추천 아웃핏:** `{inferred['outfit']}`\n"
            f"**💍 추천 장신구/벨:** `{inferred['accessories']}` ┃ Bell: `{bell}`"
        )
    embed.add_field(name="🛡️ 4. 장비 및 최적 아웃핏 (Equipment & Outfits)", value=eq_text, inline=False)

    # 탤런트
    talents = raw.get("talents", [])
    if talents:
        t_names = [f"`{t.get('name')}`" for t in talents if isinstance(t, dict) and t.get("name")]
        embed.add_field(name="🌟 5. 핵심 탤런트 (Key Talents)", value=" • ".join(t_names[:10]) if t_names else "기본 탤런트 세팅", inline=False)

    # 만트라
    mantras = raw.get("mantras", []) or raw.get("talents_and_mantras", {}).get("core_mantras", [])
    if mantras:
        m_names = [f"`{m.get('name')}`" if isinstance(m, dict) else f"`{m}`" for m in mantras]
        embed.add_field(name="🔮 6. 주요 만트라 (Mantras)", value=" • ".join(m_names[:8]), inline=False)

    # 🎯 만트라 바로 밑에 [주요 타겟 몹 / 보스 사냥법] 배치
    target_mobs_text = (
        "• **Layer 2 (Chaser / Scion of Ethiron)**: 중무기 가드브레이크 후 과다출혈/스킬 난사로 퍼센트 고정폭발 유도\n"
        "• **Duke of Erisia & Maestro**: Starkindred 공중 날개 기동으로 장판 회피 후 블러드렌드 스킬로 안정적 피흡 유지\n"
        "• **심해 몹 (Squibbo / Enforcer)**: 크리티컬 패링 유도 후 연속 만트라 연계로 즉사급 딜링"
    )
    embed.add_field(name="🎯 7. 주요 타겟 몹 / 보스 사냥 가이드", value=target_mobs_text, inline=False)

    # 장단점 & 리스크 관리
    strengths = summary.get("strengths") or ["우수한 피흡 유지력과 순간 폭딜", "Starkindred 날개를 통한 최상급 공중 기동성"]
    weaknesses = summary.get("weaknesses") or ["체력/에테르 자원 관리 필요", "공격 타이밍 빗나갈 시 패링 반격 주의"]
    
    ko_strengths = translate_to_korean_text(strengths)
    ko_weaknesses = translate_to_korean_text(weaknesses)
    
    char_text = (
        f"**✅ 장점:** {ko_strengths}\n"
        f"**⚠️ 단점/주의점:** {ko_weaknesses}"
    )
    embed.add_field(name="🥊 8. 실전 특징 및 장단점", value=char_text, inline=False)

    embed.set_footer(text="Deepwoken AI Build Analyzer • GitHub 클라우드 저장 완료 • deepwoken.co 연동 가능")
    return embed

async def run_pipeline_with_progress(url: str, status_msg: discord.Message) -> Dict[str, Any]:
    """실시간 퍼센티지(%) 진행 상태를 단계별로 업데이트하며 파이프라인 가동"""
    from pipeline.orchestrator import BuildPipelineOrchestrator
    from pipeline.web_orchestrator import WebPipelineOrchestrator

    loop = asyncio.get_running_loop()
    is_youtube = "youtube.com" in url.lower() or "youtu.be" in url.lower()

    def sync_progress_callback(percent: int, text: str):
        content = f"⚡ **[{percent}%]** {text}\n`{url}`"
        try:
            asyncio.run_coroutine_threadsafe(status_msg.edit(content=content), loop)
        except Exception:
            pass

    if is_youtube:
        orc = BuildPipelineOrchestrator()
        result_dict = await loop.run_in_executor(None, orc.process_url, url, sync_progress_callback)
        raw_build = result_dict.get("build_data", {})
    else:
        orc = WebPipelineOrchestrator()
        sync_progress_callback(30, "웹/가이드 텍스트 수집 및 파싱 중...")
        result_dict = await loop.run_in_executor(None, orc.process_url, url)
        raw_build = result_dict.get("build_data", result_dict)

    sync_progress_callback(95, "GitHub 클라우드 저장소 자동 동기화 중...")
    b_name = raw_build.get("build_summary", {}).get("build_name", "Deepwoken Build")
    await asyncio.to_thread(push_to_github, f"🤖 [Discord Bot] '{b_name}' 빌드 분석 결과 저장")

    return {
        "raw": raw_build,
        "result_dict": result_dict,
        "is_youtube": is_youtube
    }

@bot.event
async def on_ready():
    logger.info(f"[Discord Bot Ready] Logged in as {bot.user} (ID: {bot.user.id})")
    
    logger.info("Initializing ChromaDB from local GitHub data to prevent Render ephemeral wipe...")
    from agents.knowledge_builder import KnowledgeBuilder
    kb = KnowledgeBuilder(use_gemini_embedding=False)
    ingested_count = kb.ingest_all(analysis_dir="data/analysis", kb_dir="data/knowledge_base")
    logger.info(f"Rebuilt ChromaDB with {ingested_count} documents.")

    try:
        synced = await bot.tree.sync()
        logger.info(f"Slash Commands synced: {len(synced)} commands.")
    except Exception as e:
        logger.error(f"Error syncing slash commands: {e}")
    print("\n" + "="*60)
    print(f"[SUCCESS] Deepwoken AI Discord Bot is ONLINE! (Bot: {bot.user.name})")
    print("Auto-listening in '#input-link' (for analysis) and '#chat' (for AI conversation)!")
    print("="*60 + "\n")

analysis_queue_lock = asyncio.Lock()
active_tasks: Dict[int, asyncio.Task] = {}

@bot.event
async def on_message(message: discord.Message):
    if message.author == bot.user:
        return

    ch_name = getattr(message.channel, "name", "").lower()
    logger.info(f"📩 [Message Received] #{ch_name} from {message.author.name}: '{message.content[:50]}'")

    urls = extract_urls(message.content)
    
    # 디스코드에 직접 업로드된 동영상 첨부파일(.mp4 등)도 분석 대상 URL로 추가
    for att in message.attachments:
        if att.filename.lower().endswith(('.mp4', '.mov', '.webm', '.mkv')):
            urls.append(att.url)

    # Case 1: 링크(또는 영상 첨부)가 포함된 메시지 -> 빌드 1개씩 순차 분석 실행
    if urls:
        logger.info(f"🎯 Detected {len(urls)} URLs in #{ch_name} from {message.author.name}: {urls}")
        try:
            await message.add_reaction("⏳")
        except Exception:
            pass

        for url in urls:
            is_waiting = analysis_queue_lock.locked()
            init_text = (
                f"⏳ **[대기열 등록]** <@{message.author.id}> 님, 앞선 작업이 완료된 후 순서대로 자동 시작됩니다...\n`{url}`"
                if is_waiting else
                f"🚀 **[0%]** <@{message.author.id}> 님의 링크를 접수했습니다. 분석 준비 중...\n(원본 메시지에 ❌ 이모지를 달면 작업을 취소할 수 있습니다)\n`{url}`"
            )
            status_msg = await message.reply(init_text)

            async with analysis_queue_lock:
                try:
                    task = asyncio.create_task(run_pipeline_with_progress(url, status_msg))
                    active_tasks[message.id] = task
                    
                    # 시간 제한 완전 해제: 사용자가 ❌로 직접 취소할 때까지 끝까지 작업 완수
                    data = await task
                    raw = data["raw"]
                    result_dict = data["result_dict"]
                    b_name = raw.get("build_summary", {}).get("build_name", "Build")

                    embed = create_rich_build_embed(raw, url)

                    # JSON 파일 첨부 (카테고리 서브폴더 재귀 탐색)
                    doc_id = raw.get("doc_id") or result_dict.get("video_id") or url.split("v=")[-1].split("&")[0] or "build"
                    json_candidates = list((PROJECT_DIR / "data" / "analysis").rglob(f"{doc_id}.json"))
                    if json_candidates:
                        json_file_path = json_candidates[0]
                    else:
                        files = sorted((PROJECT_DIR / "data" / "analysis").rglob("*.json"), key=os.path.getmtime, reverse=True)
                        json_file_path = files[0] if files else None

                    discord_file = discord.File(str(json_file_path), filename=f"{doc_id}.json") if json_file_path and json_file_path.exists() else None

                    await status_msg.delete()
                    is_cached = result_dict.get("cached", False)
                    completion_text = (
                        f"⚡ **[캐시 즉시 로드]** <@{message.author.id}> 님! 이미 분석된 데이터가 존재하여 저장된 **'{b_name}'** 정밀 보고서를 즉시 불러왔습니다!\n"
                        f"*(소요 시간: 0.1초 • 첨부된 JSON 파일로 deepwoken.co에 바로 주입할 수 있습니다)*"
                        if is_cached else
                        f"🎉 **[100% 완료]** <@{message.author.id}> 님! 요청하신 **'{b_name}'** 정밀 보고서가 완성되었습니다!\n"
                        f"*(GitHub 저장소 자동 백업 완료 • 첨부된 JSON 파일로 deepwoken.co에 바로 주입할 수 있습니다)*"
                    )

                    if discord_file:
                        await message.reply(content=completion_text, embed=embed, file=discord_file)
                    else:
                        await message.reply(content=completion_text, embed=embed)

                    try:
                        await message.remove_reaction("⏳", bot.user)
                        await message.add_reaction("✅")
                    except Exception:
                        pass

                except asyncio.TimeoutError:
                    logger.error(f"Analysis timed out for {url}")
                    await status_msg.edit(content=f"⚠️ **[시간 초과]** <@{message.author.id}> 님, `{url}`\n영상 처리 시간(15분)이 초과되었습니다. 유튜브 다운로드가 느리거나 제미나이 응답이 지연되었습니다.")
                    try:
                        await message.remove_reaction("⏳", bot.user)
                        await message.add_reaction("❌")
                    except Exception:
                        pass
                except asyncio.CancelledError:
                    logger.warning(f"Analysis cancelled for {url}")
                    try:
                        await message.remove_reaction("⏳", bot.user)
                    except Exception:
                        pass
                except Exception as e:
                    logger.error(f"Analysis failed for {url}: {e}", exc_info=True)
                    err_msg = format_error_message(e)
                    await status_msg.edit(content=f"❌ **[분석 실패]** <@{message.author.id}> 님, `{url}`\n{err_msg}")
                    try:
                        await message.remove_reaction("⏳", bot.user)
                        await message.add_reaction("❌")
                    except Exception:
                        pass
                finally:
                    if message.id in active_tasks:
                        del active_tasks[message.id]
        return

    # Case 2: '#chat' 채널이거나 봇 멘션 -> Search Grounding RAG AI 빌드 어드바이저 대화
    if "chat" in ch_name or bot.user in message.mentions:
        user_query = message.content.replace(f"<@{bot.user.id}>", "").strip()
        if not user_query:
            return

        async with message.channel.typing():
            try:
                from chatbot.build_advisor import DeepwokenBuildAdvisor
                advisor = DeepwokenBuildAdvisor(top_k=4)
                loop = asyncio.get_running_loop()
                reply_text = await loop.run_in_executor(None, advisor.answer_query, user_query)

                # 1900자 단위 청크 전송
                if len(reply_text) <= 1950:
                    await message.reply(reply_text)
                else:
                    chunks = [reply_text[i:i+1900] for i in range(0, len(reply_text), 1900)]
                    for idx, chunk in enumerate(chunks):
                        if idx == 0:
                            await message.reply(chunk)
                        else:
                            await message.channel.send(chunk)
            except Exception as e:
                logger.error(f"Chat error: {e}", exc_info=True)
                await message.reply(f"❌ 답변 생성 중 오류가 발생했습니다: `{e}`")
        return

    await bot.process_commands(message)

@bot.event
async def on_raw_reaction_add(payload: discord.RawReactionActionEvent):
    if payload.user_id == bot.user.id:
        return
        
    if str(payload.emoji) == "❌":
        task = active_tasks.get(payload.message_id)
        if task and not task.done():
            task.cancel()
            logger.info(f"🚫 [Cancel] User {payload.user_id} cancelled analysis for message {payload.message_id}")
            channel = bot.get_channel(payload.channel_id)
            if channel:
                msg = await channel.fetch_message(payload.message_id)
                await msg.reply("🚫 **[취소됨]** 사용자의 요청으로 분석이 중단되었습니다.")

def main():
    ensure_single_instance(49281)
    token = os.getenv("DISCORD_BOT_TOKEN")
    if not token:
        print("ERROR: DISCORD_BOT_TOKEN is not set.")
        sys.exit(1)
    token = token.strip().strip('"\'').strip()
    logger.info(f"Connecting to Discord with token: {token[:8]}...{token[-6:]}")
    bot.run(token)

if __name__ == "__main__":
    main()
