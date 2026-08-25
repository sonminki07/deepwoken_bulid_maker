@echo off
chcp 65001 > nul
cd /d "%~dp0"
cls
echo ===================================================================
echo   ⚡ Deepwoken AI Build Analyzer 터미널 환경
echo ===================================================================
echo.
echo   [사용 가능한 명령어]:
echo   1. 유튜브 분석: python main.py analyze "URL"
echo   2. 웹 가이드:   python main.py web "URL"
echo   3. 챗봇 대화:   python main.py chat
echo   4. 웹 뷰어:     python main.py view
echo   5. 위키 동기화: python main.py wiki
echo.
echo ===================================================================
echo.
cmd /k
