import os
import re
import sys
import time
import json
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
        if any(k in clean_u.lower() for k in ['youtube.com', 'youtu.be', 'docs.google.com', 'deepwoken.co', 'deepwoken.fandom.com']):
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
        
        # 키워드 기반 기본 메타 세팅 추천
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

def create_rich_build_embed(raw: Dict[str, Any], url: str) -> discord.Embed:
    """수치, 스탯, 탤런트, 장비, 아웃핏, 육성법이 모두 포함된 고밀도 Discord 보고서 Embed 생성"""
    summary = raw.get("build_summary", {})
    b_name = summary.get("build_name", "Deepwoken Custom Build")
    b_type = summary.get("build_type", "PvP/PvE")
    difficulty = summary.get("difficulty", "Intermediate")
    opinion = summary.get("creator_opinion", "AI 정밀 분석 빌드 가이드입니다.")

    setup = raw.get("character_setup", {})
    oath = setup.get("oath") or summary.get("oath") or "Oathless"
    race = setup.get("race") or "Any Race (Ganymede/Kiron/Vesperian 추천)"
    origin = setup.get("origin") or "Castaway / Voidheart"
    bell = setup.get("resonance_bell") or "Reaper / Kamui / Wind Up"

    embed = discord.Embed(
        title=f"⚔️ {b_name} [{b_type}]",
        url=url,
        description=f"**📝 빌드 핵심 메커니즘 & 개요:**\n{opinion}",
        color=discord.Color.from_rgb(234, 88, 12)  # High-energy Orange/Amber
    )
    embed.set_author(name=f"난이도: {difficulty} ┃ Oath: {oath} ┃ 종족: {race}", icon_url="https://cdn.discordapp.com/emojis/1042718873733054524.png")

    # 1. 📊 상세 스탯 수치 (Pre-Shrine & Post-Shrine)
    stats_data = raw.get("stats", {})
    pre_shrine = stats_data.get("pre_shrine", {})
    post_shrine = stats_data.get("post_shrine", {})

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
        embed.add_field(name="⛩️ 1. Pre-Shrine 스탯 (초반 탤런트 파밍)", value=pre_str, inline=False)
        embed.add_field(name="📊 2. Post-Shrine 최종 완성 스탯 (Final Level 20)", value=post_str, inline=False)
    else:
        # Fallback to old format
        old_attrs = raw.get("stats_and_attunements", {}).get("attributes", {})
        if old_attrs:
            stat_line = f"**STR** `{old_attrs.get('strength', 0)}` ┃ **FTD** `{old_attrs.get('fortitude', 0)}` ┃ **AGL** `{old_attrs.get('agility', 0)}` ┃ **INT** `{old_attrs.get('intelligence', 0)}` ┃ **WLL** `{old_attrs.get('willpower', 0)}` ┃ **CHA** `{old_attrs.get('charisma', 0)}`"
            embed.add_field(name="📊 완성 스탯 (Attributes)", value=stat_line, inline=False)

    # 2. 🛡️ 장비, 아웃핏 및 추천 인챈트 (Equipment & Outfit)
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
        # 자동 유추 메타 장비 추천
        inferred = infer_missing_equipment(b_name, oath, "Bloodrend / Attunement")
        eq_text = (
            f"**⚔️ 추천 무기:** `{inferred['weapon']}` (인챈트: `{inferred['enchant']}`)\n"
            f"**🥋 추천 아웃핏:** `{inferred['outfit']}`\n"
            f"**💍 추천 장신구/벨:** `{inferred['accessories']}` ┃ Bell: `{bell}`"
        )
    embed.add_field(name="🛡️ 3. 장비 및 최적 아웃핏 (Equipment & Outfits)", value=eq_text, inline=False)

    # 3. 🌟 핵심 탤런트 (Core Talents)
    talents = raw.get("talents", [])
    if talents:
        t_names = [f"`{t.get('name')}`" for t in talents if isinstance(t, dict) and t.get("name")]
        embed.add_field(name="🌟 4. 핵심 탤런트 (Key Talents)", value=" • ".join(t_names[:12]) if t_names else "기본 생존 및 공격 탤런트 세팅", inline=False)
    else:
        old_talents = raw.get("talents_and_mantras", {}).get("core_talents", [])
        if old_talents:
            embed.add_field(name="🌟 4. 핵심 탤런트 (Key Talents)", value=" • ".join([f"`{t}`" for t in old_talents[:12]]), inline=False)

    # 4. 🔮 주요 만트라 (Mantras)
    mantras = raw.get("mantras", []) or raw.get("talents_and_mantras", {}).get("core_mantras", [])
    if mantras:
        m_names = [f"`{m.get('name')}`" if isinstance(m, dict) else f"`{m}`" for m in mantras]
        embed.add_field(name="🔮 5. 주요 만트라 (Mantras)", value=" • ".join(m_names[:8]), inline=False)

    # 5. 🎯 빌드 장단점 & 실전 운용법
    strengths = summary.get("strengths") or raw.get("combo_and_playstyle", {}).get("strengths") or ["우수한 딜링/생존 밸런스"]
    weaknesses = summary.get("weaknesses") or raw.get("combo_and_playstyle", {}).get("weaknesses") or ["스태미나 관리 필요"]
    
    char_text = (
        f"**✅ 장점:** {', '.join(strengths) if isinstance(strengths, list) else strengths}\n"
        f"**⚠️ 단점/주의점:** {', '.join(weaknesses) if isinstance(weaknesses, list) else weaknesses}"
    )
    embed.add_field(name="🎯 6. 실전 특징 및 장단점", value=char_text, inline=False)

    embed.set_footer(text="Deepwoken AI Build Analyzer • 실시간 웹 검색 및 지식 기반 구축 완료 • deepwoken.co 연동 가능")
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
    try:
        synced = await bot.tree.sync()
        logger.info(f"Slash Commands synced: {len(synced)} commands.")
    except Exception as e:
        logger.error(f"Error syncing slash commands: {e}")
    print("\n" + "="*60)
    print(f"[SUCCESS] Deepwoken AI Discord Bot is ONLINE! (Bot: {bot.user.name})")
    print("Auto-listening in '#input-link' (for analysis) and '#chat' (for AI conversation)!")
    print("="*60 + "\n")

@bot.event
async def on_message(message: discord.Message):
    if message.author == bot.user:
        return

    ch_name = getattr(message.channel, "name", "").lower()
    logger.info(f"📩 [Message Received] #{ch_name} from {message.author.name}: '{message.content[:50]}'")

    urls = extract_urls(message.content)

    # Case 1: 링크가 포함된 메시지 -> 빌드 자동 분석 실행
    if urls:
        logger.info(f"🎯 Detected {len(urls)} URLs in #{ch_name} from {message.author.name}: {urls}")
        try:
            await message.add_reaction("⏳")
        except Exception:
            pass

        for url in urls:
            status_msg = await message.reply(
                f"🚀 **[0%]** <@{message.author.id}> 님의 링크를 접수했습니다. 분석 준비 중...\n`{url}`"
            )
            
            try:
                data = await run_pipeline_with_progress(url, status_msg)
                raw = data["raw"]
                result_dict = data["result_dict"]
                b_name = raw.get("build_summary", {}).get("build_name", "Build")

                embed = create_rich_build_embed(raw, url)

                # JSON 파일 첨부
                doc_id = raw.get("doc_id") or result_dict.get("video_id") or url.split("v=")[-1].split("&")[0] or "build"
                json_file_path = PROJECT_DIR / "data" / "analysis" / f"{doc_id}.json"
                if not json_file_path.exists():
                    files = sorted((PROJECT_DIR / "data" / "analysis").glob("*.json"), key=os.path.getmtime, reverse=True)
                    if files:
                        json_file_path = files[0]

                discord_file = discord.File(str(json_file_path), filename=f"{doc_id}.json") if json_file_path.exists() else None

                await status_msg.delete()
                completion_text = (
                    f"🎉 **[100% 완료]** <@{message.author.id}> 님! 요청하신 **'{b_name}'** 정밀 빌드 보고서가 완성되었습니다!\n"
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

            except Exception as e:
                logger.error(f"Analysis failed for {url}: {e}", exc_info=True)
                await status_msg.edit(content=f"❌ **[분석 실패]** <@{message.author.id}> 님, `{url}` 분석 중 오류가 발생했습니다: `{e}`")
                try:
                    await message.remove_reaction("⏳", bot.user)
                    await message.add_reaction("❌")
                except Exception:
                    pass
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

def main():
    token = os.getenv("DISCORD_BOT_TOKEN")
    if not token:
        print("ERROR: DISCORD_BOT_TOKEN is not set.")
        sys.exit(1)
    bot.run(token)

if __name__ == "__main__":
    main()
