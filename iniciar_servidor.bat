@echo off
title Servidor Financeiro - API + NGROK (SEGURO)
echo Iniciando API FastAPI...
start /min python main_api.py
echo Aguardando API subir...
timeout /t 5

:: CONFIGURACOES DE SEGURANCA NGROK
:: Substitua 'usuario:senha' pela credencial que voce desejar
:: Substitua '--domain=...' pelo seu dominio reservado no painel do ngrok
echo Iniciando Tunel NGROK Seguro...
start .\ngrok.exe http 8000 --domain=noncongruous-chiffonade-bernarda.ngrok-free.dev --auth="pedro:financeiro123"

echo.
echo ==========================================
echo SERVIDOR RODANDO COM SEGURANCA MAXIMA!
echo.
echo Camadas de Protecao Ativas:
echo 1. Chave de API (X-API-Key) habilitada.
echo 2. Autenticacao Basica no Tunel ativada.
echo 3. Dominio Fixo configurado.
echo ==========================================
pause
