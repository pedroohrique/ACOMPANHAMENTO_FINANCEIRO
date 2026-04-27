@echo off
title Servidor Financeiro - API + NGROK
echo Iniciando API FastAPI...
start /min python main_api.py
echo Aguardando API subir...
timeout /t 5
echo Iniciando Túnel NGROK...
start .\ngrok.exe http 8000
echo.
echo ==========================================
echo SERVIDOR RODANDO COM SUCESSO!
echo Mantenha estas janelas abertas.
echo ==========================================
pause
