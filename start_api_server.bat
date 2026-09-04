@echo off
chcp 65001 >nul
title Conciliamus Architecture Knowledge API Server
echo ======================================================================
echo   Conciliamus Architecture Knowledge API Server (OKF v0.2)
echo ======================================================================
echo.
echo Starte FastAPI Server auf http://127.0.0.1:8000 ...
echo Obsidian Graph Viewer:       http://127.0.0.1:8000/graph
echo Dokumentation (Swagger UI):  http://127.0.0.1:8000/docs
echo Dokumentation (ReDoc):       http://127.0.0.1:8000/redoc
echo.
python api\server.py
pause
