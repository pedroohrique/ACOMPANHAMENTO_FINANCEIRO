@echo off
title Servidor Financeiro - API + NGROK
chcp 65001 > nul

echo ==========================================
echo  INICIALIZANDO SERVIDOR FINANCEIRO
echo ==========================================
echo.

:: ---- PASSO 1: Encerrar processos antigos ----
echo [1/3] Encerrando processos anteriores...
taskkill /F /IM ngrok.exe > nul 2>&1
taskkill /F /IM python.exe > nul 2>&1
timeout /t 2 /nobreak > nul
echo       OK - Processos anteriores encerrados.
echo.

:: ---- PASSO 2: Iniciar API FastAPI ----
echo [2/3] Iniciando API FastAPI na porta 8000...
start "API_FastAPI" /min cmd /c "python main_api.py"
echo       Aguardando API inicializar...
timeout /t 6 /nobreak > nul
echo       OK - API iniciada.
echo.

:: ---- PASSO 3: Iniciar Tunel NGROK ----
echo [3/3] Iniciando tunel NGROK...
start "NGROK_Tunnel" .\ngrok.exe http 8000 --url=noncongruous-chiffonade-bernarda.ngrok-free.dev
timeout /t 3 /nobreak > nul
echo       OK - Tunel NGROK iniciado.
echo.

echo ==========================================
echo  SERVIDOR OPERACIONAL!
echo.
echo  API Local  : http://localhost:8000
echo  API Publica: https://noncongruous-chiffonade-bernarda.ngrok-free.dev
echo  Docs API   : http://localhost:8000/docs
echo.
echo  SEGURANCA: Chave de API (X-API-Key) ativa
echo ==========================================
echo.
echo  Mantenha esta janela aberta.
echo  Para encerrar, feche esta janela ou pressione qualquer tecla.
echo.
pause
