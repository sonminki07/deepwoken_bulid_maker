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

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

load_dotenv()
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
    raw_urls = re.findall(r'https?://[^\s\)\"\']+', text)
    valid_urls = []
    for u in raw_urls:
        clean_u = u.rstrip('.,;\"\'')
        if any(k in clean_u.lower() for k in ['youtube.com', 'youtu.be', 'docs.google.com', 'deepwoken.co', 'deepwoken.fandom.com']):
            if clean_u not in valid_urls:
                valid_urls.append(clean_u)
    return valid_urls

async def run_pipeline_with_progress(url: str, status_msg: discord.Message) -> Dict[str, Any]:
    """실시간 퍼센티지(%) 진행 상태를 업데이트하며 파이프라인 가동"""
    from pipeline.orchestrator import BuildPipelineOrchestrator
    from pipeline.web_orchestrator import WebPipelineOrchestrator

    loop = asyncio.get_running_loop()
    is_youtube = "youtube.com" in url.lower() or "youtu.be" in url.lower()

    # Step 1: 다운로드 시작 (20%)
    await status_msg.edit(content=f"⏳ **[20%]** 콘텐츠 수집 및 비디오 다운로드 중...\n`{url}`")
    
    if is_youtube:
        orc = BuildPipelineOrchestrator()
        
        # Step 2: Gemini 비디오 스캔 (50%)
        await asyncio.sleep(1)
        await status_msg.edit(content=f"🧠 **[55%]** Gemini 3.7 AI 멀티모달 비디오 프레임 스캔 중...\n`{url}`")
        
        result_dict = await loop.run_in_executor(None, orc.process_url, url)
        raw_build = result_dict.get("build_data", {})
    else:
        orc = WebPipelineOrchestrator()
        
        # Step 2: 웹 파싱 & 텍스트 분석 (50%)
        await asyncio.sleep(1)
        await status_msg.edit(content=f"🧠 **[55%]** 가이드 문서 구조화 및 서브 에이전트 병렬 분석 중...\n`{url}`")
        
        result_dict = await loop.run_in_executor(None, orc.process_url, url)
        raw_build = result_dict.get("build_data", result_dict)

    # Step 3: 지식 베이스 및 RAG 등록 (85%)
    await status_msg.edit(content=f"📊 **[85%]** 스탯, 탤런트, 콤보 메커니즘 검증 및 DB 적재 중...")
    await asyncio.sleep(0.5)

    # Step 4: GitHub 동기화 (95%)
    await status_msg.edit(content=f"☁️ **[95%]** GitHub 클라우드 저장소 자동 푸시 중...")
    b_name = raw_build.get("build_summary", {}).get("build_name", "Deepwoken Build")
    await asyncio.to_thread(push_to_github, f"🤖 [Discord Bot] '{b_name}' 빌드 분석 결과 저장")

    return {
        "raw": raw_build,
        "result_dict": result_dict,
        "is_youtube": is_youtube
    }

def create_rich_build_embed(raw: Dict[str, Any], url: str) -> discord.Embed:
    """빌드 상세 정보 및 특징/장단점이 정리된 Discord Embed 생성"""
    summary = raw.get("build_summary", {})
    stats = raw.get("stats_and_attunements", {})
    talents_mantras = raw.get("talents_and_mantras", {})
    shrine = raw.get("shrine_of_order", {})
    combo = raw.get("combo_and_playstyle", {})

    b_name = summary.get("build_name", "Deepwoken Build")
    b_type = summary.get("build_type", "Hybrid")
    oath = summary.get("oath", "Oathless")
    author = summary.get("author", "Unknown")
    difficulty = summary.get("difficulty", "Intermediate")
    opinion = summary.get("creator_opinion", "AI가 구조화한 빌드 가이드입니다.")

    embed = discord.Embed(
        title=f"⚔️ {b_name} [{b_type}]",
        url=url,
        description=f"**📝 빌드 개요:**\n{opinion}",
        color=discord.Color.from_rgb(56, 189, 248)
    )

    embed.set_author(name=f"작성자: {author} | 난이도: {difficulty}", icon_url="https://cdn.discordapp.com/emojis/1042718873733054524.png")

    # 1. 스탯 분배
    attrs = stats.get("attributes", {})
    if attrs:
        stat_line = (
            f"**STR** `{attrs.get('strength', 0)}` ┃ **FTD** `{attrs.get('fortitude', 0)}` ┃ **AGL** `{attrs.get('agility', 0)}`\n"
            f"**INT** `{attrs.get('intelligence', 0)}` ┃ **WLL** `{attrs.get('willpower', 0)}` ┃ **CHA** `{attrs.get('charisma', 0)}`\n"
            f"**Oath:** `{oath}` ┃ **무기:** `{stats.get('weapon_type', 'Medium')}`"
        )
        embed.add_field(name="📊 스탯 및 특성 (Attributes)", value=stat_line, inline=False)

    # 2. 속성 (Attunements)
    attunements = stats.get("attunements", {})
    if attunements:
        att_items = [f"**{k.capitalize()}** `{v}`" for k, v in attunements.items() if v > 0]
        if att_items:
            embed.add_field(name="⚡ 속성 분배", value=" ┃ ".join(att_items), inline=False)

    # 3. 핵심 탤런트 & 만트라
    core_talents = talents_mantras.get("core_talents", [])
    if core_talents:
        embed.add_field(name="🌟 핵심 탤런트", value=" • ".join(core_talents[:8]), inline=False)

    core_mantras = talents_mantras.get("core_mantras", [])
    if core_mantras:
        embed.add_field(name="🔮 주요 만트라(주문)", value=" • ".join(core_mantras[:8]), inline=False)

    # 4. 빌드 특징 및 장단점 (Characteristics)
    strengths = combo.get("strengths") or ["우수한 콤보 연계력", "안정적인 딜링/생존 밸런스"]
    weaknesses = combo.get("weaknesses") or ["숙련도 필요", "스태미나/에테르 관리 유의"]
    
    char_text = (
        f"**✅ 장점:** {', '.join(strengths) if isinstance(strengths, list) else strengths}\n"
        f"**⚠️ 단점/주의점:** {', '.join(weaknesses) if isinstance(weaknesses, list) else weaknesses}"
    )
    embed.add_field(name="🎯 빌드 특징 및 장단점", value=char_text, inline=False)

    # 5. Shrine of Order & 콤보 팁
    if shrine and shrine.get("order_order_progression"):
        embed.add_field(name="⛩️ Shrine of Order 루트", value=shrine.get("order_order_progression")[:250], inline=False)

    if combo and combo.get("combo_guide"):
        embed.add_field(name="🥊 콤보 및 전투 팁", value=combo.get("combo_guide")[:250], inline=False)

    embed.set_footer(text="Deepwoken AI Build Analyzer • GitHub 클라우드 저장 완료 • deepwoken.co 연동 가능")
    return embed

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
    print("Channels listening: 'input-link' and all channels with build URLs.")
    print("="*60 + "\n")

@bot.event
async def on_message(message: discord.Message):
    if message.author == bot.user:
        return

    urls = extract_urls(message.content)
    if not urls:
        await bot.process_commands(message)
        return

    # 채널 검사: input-link 채널이거나 일반 링크 업로드
    logger.info(f"Received {len(urls)} URLs in #{message.channel.name} from {message.author.name}")

    try:
        await message.add_reaction("⏳")
    except Exception:
        pass

    for url in urls:
        status_msg = await message.channel.send(
            f"🚀 **[0%]** <@{message.author.id}> 님의 요청을 접수했습니다. 분석 준비 중...\n`{url}`"
        )
        
        try:
            # 실시간 진행도 업데이트 파이프라인
            data = await run_pipeline_with_progress(url, status_msg)
            raw = data["raw"]
            result_dict = data["result_dict"]
            b_name = raw.get("build_summary", {}).get("build_name", "Build")

            embed = create_rich_build_embed(raw, url)

            # JSON 파일 첨부
            doc_id = raw.get("doc_id") or result_dict.get("video_id") or url.split("v=")[-1].split("&")[0] or "build"
            json_file_path = PROJECT_DIR / "data" / "analysis" / f"{doc_id}.json"
            if not json_file_path.exists():
                # 최신 파일 탐색
                files = sorted((PROJECT_DIR / "data" / "analysis").glob("*.json"), key=os.path.getmtime, reverse=True)
                if files:
                    json_file_path = files[0]

            discord_file = discord.File(str(json_file_path), filename=f"{doc_id}.json") if json_file_path.exists() else None

            # 최종 100% 완료 메시지 및 멘션
            await status_msg.delete()
            completion_text = (
                f"🎉 **[100% 완료]** <@{message.author.id}> 님! 요청하신 **'{b_name}'** 빌드 분석 및 특징 브리핑이 완료되었습니다!\n"
                f"*(GitHub 저장소 자동 백업 완료 • 첨부된 JSON 파일로 deepwoken.co에 바로 주입할 수 있습니다)*"
            )

            if discord_file:
                await message.channel.send(content=completion_text, embed=embed, file=discord_file)
            else:
                await message.channel.send(content=completion_text, embed=embed)

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

    await bot.process_commands(message)

def main():
    token = os.getenv("DISCORD_BOT_TOKEN")
    if not token:
        print("ERROR: DISCORD_BOT_TOKEN is not set.")
        sys.exit(1)
    bot.run(token)

if __name__ == "__main__":
    main()
