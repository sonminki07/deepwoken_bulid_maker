#!/bin/bash
echo "=================================================="
echo "⚡ Deepwoken AI Discord Bot 자동 시작 & 업데이트"
echo "=================================================="

# 1. 기존 실행 중인 파이썬 봇 강제 종료
echo "1️⃣ 기존 봇 정리 중..."
pkill -f "discord_bot.py" 2>/dev/null || true
pkill -f "python3" 2>/dev/null || true
sleep 1

# 2. 깃허브 최신 코드 강제 동기화 (충돌 없이 100% 최신화)
echo "2️⃣ 최신 패치 자동 다운로드 중..."
git fetch origin main
git reset --hard origin/main

# 3. 디스코드 봇 가동
echo "3️⃣ 디스코드 봇 시작!"
echo "=================================================="
python3 discord_bot.py
