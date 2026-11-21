@echo off
title GreenGrid - Smart Energy Management Platform
echo ====================================================================
echo  Starting GreenGrid (P02 - FSD Python)
echo  Database: MySQL 8.0 (greengrid_db)
echo  Web Interface: http://127.0.0.1:8000/
echo ====================================================================
echo.

cd /d "%~dp0backend"
start "" http://127.0.0.1:8000/
"..\venv\Scripts\python.exe" manage.py runserver 127.0.0.1:8000

pause
