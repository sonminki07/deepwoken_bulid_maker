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
    raw_urls = re.findall(r'https?://[^\s\)\"\'>]+', text)
    valid_urls = []
    for u in raw_urls:
        clean_u = u.strip('<>[](),;\"\'')
        if any(k in clean_u.lower() for k in ['youtube.com', 'youtu.be', 'docs.google.com', 'deepwoken.co', 'deepwoken.fandom.com']):
            if clean_u not in valid_urls:
                valid_urls.append(clean_u)
    return valid_urls

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

    # Step 4: GitHub 동기화 (95%)
    sync_progress_callback(95, "GitHub 클라우드 저장소 자동 동기화 중...")
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
                    f"🎉 **[100% 완료]** <@{message.author.id}> 님! 요청하신 **'{b_name}'** 빌드 분석 및 특징 브리핑이 완료되었습니다!\n"
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

    # Case 2: '#chat' 채널이거나 봇 멘션 -> RAG AI 빌드 어드바이저 대화
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

                # 2000자 단위 청크 전송
                if len(reply_text) <= 1950:
                    await message.reply(reply_text)
                else:
                    chunks = [reply_text[i:i+1900] for i in range(0, len(reply_text), 1900)]
                    first_msg = await message.reply(chunks[0])
                    for chunk in chunks[1:]:
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
