@echo off
chcp 65001 >nul
set PYTHONIOENCODING=utf-8
title Google AI Pro (5 TB) - Cài đặt và khởi chạy lần đầu
cd /d "%~dp0"
echo ======================================================================
echo   Đang kiểm tra và cài đặt các gói Python (fastapi, uvicorn, playwright)...
echo ======================================================================
python -m pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
echo.
echo ======================================================================
echo   Đang khởi động bảng điều khiển Web (http://127.0.0.1:8765) ...
echo ======================================================================
start "" "http://127.0.0.1:8765"
python app.py
pause
