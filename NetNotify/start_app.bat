@echo off
cd /d %~dp0

:: Запускаем сервер в отдельном окне
start "Server" python -m server.server

:: Небольшая задержка, чтобы сервер успел подняться
timeout /t 2 >nul

:: Запускаем клиент
python -m client.client

pause

