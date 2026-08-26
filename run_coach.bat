@echo off
chcp 65001 > nul
set PYTHONIOENCODING=utf-8
title Deepwoken AI Web Coach
echo ==================================================
echo [Deepwoken Builder & AI Master Coach]
echo ==================================================
streamlit run web_coach.py
pause
