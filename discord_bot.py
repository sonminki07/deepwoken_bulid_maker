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

# 로깅 설정
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

load_dotenv()
PROJECT_DIR = Path(__file__).resolve().parent

# Discord Bot 설정
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

def push_to_github(commit_msg: str) -> bool:
    """분석된 빌드 JSON 및 지식 문서를 GitHub 저장소에 자동 커밋 & 푸시"""
    try:
        logger.info("[Git] Adding files to git...")
        subprocess.run(["git", "add", "data/analysis/", "data/knowledge_base/"], cwd=str(PROJECT_DIR), check=True)
        
        # 변경 사항 있는지 확인
        diff_proc = subprocess.run(["git", "diff", "--staged", "--quiet"], cwd=str(PROJECT_DIR))
        if diff_proc.returncode == 0:
            logger.info("[Git] No changes to commit.")
            return True
            
        subprocess.run(["git", "commit", "-m", commit_msg], cwd=str(PROJECT_DIR), check=True)
        logger.info("[Git] Pushing to origin main...")
        subprocess.run(["git", "push", "origin", "main"], cwd=str(PROJECT_DIR), check=True)
        logger.info("[Git] Successfully pushed to GitHub!")
        return True
    except Exception as e:
        logger.error(f"[Git Push Error] {e}")
        return False

def pull_from_github() -> str:
    """GitHub에서 최신 데이터 가져오기"""
    try:
        proc = subprocess.run(["git", "pull", "origin", "main"], cwd=str(PROJECT_DIR), capture_output=True, text=True, check=True)
        return proc.stdout
    except Exception as e:
        return f"Error: {e}"

def extract_urls(text: str) -> List[str]:
    """메시지 본문에서 유튜브, 구글 닥스, 위키 URL 추출"""
    raw_urls = re.findall(r'https?://[^\s\)\"\']+', text)
    valid_urls = []
    for u in raw_urls:
        clean_u = u.rstrip('.,;\"\'')
        if any(k in clean_u.lower() for k in ['youtube.com', 'youtu.be', 'docs.google.com', 'deepwoken.co', 'deepwoken.fandom.com']):
            if clean_u not in valid_urls:
                valid_urls.append(clean_u)
    return valid_urls

async def run_pipeline_for_url(url: str) -> Dict[str, Any]:
    """비동기 스레드 풀에서 AI 분석 파이프라인 가동"""
    from pipeline.orchestrator import BuildPipelineOrchestrator
    from pipeline.web_orchestrator import WebPipelineOrchestrator

    loop = asyncio.get_running_loop()
    is_youtube = "youtube.com" in url.lower() or "youtu.be" in url.lower()

    if is_youtube:
        orc = BuildPipelineOrchestrator()
        result = await loop.run_in_executor(None, orc.process_url, url)
    else:
        orc = WebPipelineOrchestrator()
        result = await loop.run_in_executor(None, orc.process_url, url)

    return result

def create_build_embed(result: Dict[str, Any], url: str) -> discord.Embed:
    """분석 결과를 깔끔한 Discord Embed 카드로 생성"""
    summary = result.get("build_summary", {})
    stats = result.get("stats_and_attunements", {})
    talents_mantras = result.get("talents_and_mantras", {})
    shrine = result.get("shrine_of_order", {})
    combo = result.get("combo_and_playstyle", {})

    b_name = summary.get("build_name", "Deepwoken Build")
    b_type = summary.get("build_type", "Hybrid")
    oath = summary.get("oath", "Oathless")
    author = summary.get("author", "Unknown")

    embed = discord.Embed(
        title=f"⚔️ {b_name} ({b_type})",
        url=url,
        description=summary.get("creator_opinion", "AI가 구조화한 빌드 가이드입니다."),
        color=discord.Color.from_rgb(56, 189, 248)
    )

    embed.set_author(name=f"작성자/크리에이터: {author}", icon_url="https://cdn.discordapp.com/emojis/1042718873733054524.png")

    # 스탯 요약
    attrs = stats.get("attributes", {})
    if attrs:
        stat_text = (
            f"**STR** `{attrs.get('strength', 0)}` | **FTD** `{attrs.get('fortitude', 0)}` | **AGL** `{attrs.get('agility', 0)}`\n"
            f"**INT** `{attrs.get('intelligence', 0)}` | **WLL** `{attrs.get('willpower', 0)}` | **CHA** `{attrs.get('charisma', 0)}`\n"
            f"**Oath**: `{oath}` | **무기**: `{stats.get('weapon_type', 'Medium')}`"
        )
        embed.add_field(name="📊 주요 스탯 & Oath", value=stat_text, inline=False)

    # 속성 (Attunements)
    attunements = stats.get("attunements", {})
    if attunements:
        att_str = " / ".join([f"{k.capitalize()}: `{v}`" for k, v in attunements.items() if v > 0])
        if att_str:
            embed.add_field(name="⚡ 속성 투자", value=att_str, inline=True)

    # 핵심 탤런트
    core_talents = talents_mantras.get("core_talents", [])
    if core_talents:
        embed.add_field(name="🌟 핵심 탤런트", value=", ".join(core_talents[:6]), inline=False)

    # 핵심 만트라
    core_mantras = talents_mantras.get("core_mantras", [])
    if core_mantras:
        embed.add_field(name="🔮 핵심 주문(Mantras)", value=", ".join(core_mantras[:6]), inline=False)

    # Shrine of Order
    if shrine and shrine.get("order_order_progression"):
        embed.add_field(name="⛩️ Shrine of Order", value=shrine.get("order_order_progression")[:250], inline=False)

    # 콤보 & 운용
    if combo and combo.get("combo_guide"):
        embed.add_field(name="🥊 콤보 & 플레이 가이드", value=combo.get("combo_guide")[:250], inline=False)

    embed.set_footer(text="Deepwoken AI Build Analyzer • GitHub 클라우드 자동 저장 완료")
    return embed

@bot.event
async def on_ready():
    logger.info(f"🤖 [Discord Bot Ready] Logged in as {bot.user} (ID: {bot.user.id})")
    try:
        synced = await bot.tree.sync()
        logger.info(f"Slash Commands synced: {len(synced)} commands.")
    except Exception as e:
        logger.error(f"Error syncing slash commands: {e}")
    print("\n" + "="*60)
    print(f"🎉 Deepwoken AI 디스코드 봇이 정상 가동되었습니다! (봇: {bot.user.name})")
    print("디스코드 채널에 유튜브 또는 구글 닥스 링크를 올리면 자동 분석됩니다.")
    print("="*60 + "\n")

@bot.event
async def on_message(message: discord.Message):
    # 봇 자신의 메시지는 무시
    if message.author == bot.user:
        return

    urls = extract_urls(message.content)
    if not urls:
        await bot.process_commands(message)
        return

    logger.info(f"Detected {len(urls)} URLs from {message.author.name}: {urls}")

    # 리액션 표시
    try:
        await message.add_reaction("⏳")
    except Exception:
        pass

    for url in urls:
        status_msg = await message.channel.send(f"🔍 **[Deepwoken AI]** `{url}` 분석을 시작합니다...\n*(영상 다운로드 및 Gemini 멀티모달 분석 가동 중)*")
        try:
            # 파이프라인 가동
            result = await run_pipeline_for_url(url)
            b_name = result.get("build_summary", {}).get("build_name", "Build")

            # GitHub 자동 커밋 & 푸시
            await status_msg.edit(content=f"💾 **[Deepwoken AI]** `{b_name}` 분석 완료! GitHub 저장소에 동기화 중...")
            commit_msg = f"🤖 [Discord Bot] '{b_name}' 빌드 분석 결과 저장"
            push_success = await asyncio.to_thread(push_to_github, commit_msg)

            # Embed 카드 전송
            embed = create_build_embed(result, url)
            
            # JSON 파일 첨부
            doc_id = result.get("doc_id") or result.get("video_meta", {}).get("url", "").split("v=")[-1] or "build"
            json_file_path = PROJECT_DIR / "data" / "analysis" / f"{doc_id}.json"
            
            discord_file = None
            if json_file_path.exists():
                discord_file = discord.File(str(json_file_path), filename=f"{doc_id}.json")

            await status_msg.delete()
            if discord_file:
                await message.channel.send(embed=embed, file=discord_file)
            else:
                await message.channel.send(embed=embed)

            try:
                await message.remove_reaction("⏳", bot.user)
                await message.add_reaction("✅")
            except Exception:
                pass

        except Exception as e:
            logger.error(f"Analysis failed for {url}: {e}")
            await status_msg.edit(content=f"❌ **[분석 오류]** `{url}` 분석 중 오류가 발생했습니다: `{e}`")
            try:
                await message.remove_reaction("⏳", bot.user)
                await message.add_reaction("❌")
            except Exception:
                pass

    await bot.process_commands(message)

# 슬래시 명령어: /ask (RAG 기반 빌드 조언)
@bot.tree.command(name="ask", description="Deepwoken AI에게 빌드/장비/특성 관련 질문을 합니다.")
@app_commands.describe(question="질문 내용 (예: 'Frostdraw에 어울리는 방어구랑 콤보 알려줘')")
async def ask_advisor(interaction: discord.Interaction, question: str):
    await interaction.response.defer(thinking=True)
    try:
        from chatbot.build_advisor import DeepwokenBuildAdvisor
        advisor = DeepwokenBuildAdvisor(top_k=4)
        response_text = await asyncio.to_thread(advisor.answer_query, question)
        
        # 2000자 초과 방지
        if len(response_text) > 1950:
            parts = [response_text[i:i+1900] for i in range(0, len(response_text), 1900)]
            await interaction.followup.send(f"**❓ 질문:** {question}\n\n" + parts[0])
            for p in parts[1:]:
                await interaction.followup.send(p)
        else:
            await interaction.followup.send(f"**❓ 질문:** {question}\n\n" + response_text)
    except Exception as e:
        await interaction.followup.send(f"❌ 오류 발생: {e}")

# 슬래시 명령어: /sync (GitHub 동기화)
@bot.tree.command(name="sync", description="GitHub 저장소로부터 최신 빌드 데이터베이스를 동기화합니다.")
async def sync_repo(interaction: discord.Interaction):
    await interaction.response.defer(thinking=True)
    res = await asyncio.to_thread(pull_from_github)
    await interaction.followup.send(f"🔄 **[GitHub Sync Result]**\n```{res}```")

def main():
    token = os.getenv("DISCORD_BOT_TOKEN")
    if not token or token == "YOUR_DISCORD_BOT_TOKEN_HERE":
        print("\n" + "="*60)
        print("⚠️ DISCORD_BOT_TOKEN 이 설정되지 않았습니다!")
        print("1. https://discord.com/developers/applications 에서 봇을 생성하세요.")
        print("2. .env 파일에 DISCORD_BOT_TOKEN=토큰값을 입력하세요.")
        print("="*60 + "\n")
        sys.exit(1)

    bot.run(token)

if __name__ == "__main__":
    main()
