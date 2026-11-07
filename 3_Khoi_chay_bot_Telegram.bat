@echo off
setlocal
cd /d "%~dp0"
set "PYTHONIOENCODING=utf-8"
title Telegram Bot - Google AI Pro

echo ======================================================================
echo   Telegram Bot for Google AI Pro Dashboard
echo   Start the dashboard before using this bot.
echo ======================================================================

if not defined TELEGRAM_BOT_TOKEN (
    set /p "TELEGRAM_BOT_TOKEN=Telegram bot token from BotFather: "
)
if not defined TELEGRAM_ALLOWED_USER_IDS (
    echo You can send /id to the bot to get your Telegram user ID.
    set /p "TELEGRAM_ALLOWED_USER_IDS=Allowed Telegram user ID: "
)

python telegram_bot.py
pause
endlocal
