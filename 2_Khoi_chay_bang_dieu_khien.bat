@echo off
chcp 65001 >nul
set PYTHONIOENCODING=utf-8
title Bảng điều khiển tự động Google AI Pro (5 TB) miễn phí hai năm
cd /d "%~dp0"
echo ======================================================================
echo   Đang khởi động bảng điều khiển tự động Google AI Pro (5 TB)...
echo   Địa chỉ bảng điều khiển: http://127.0.0.1:8765
echo ======================================================================
start "" "http://127.0.0.1:8765"
python app.py
pause
