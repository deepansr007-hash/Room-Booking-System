@echo off
title Hotel Room Booking System Server
cls
echo ======================================================
echo    STARTING HOTEL ROOM BOOKING SYSTEM (TAMIL NADU)
echo ======================================================
cd /d "%~dp0"
python run.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Server stopped or encountered an error.
    pause
)
