@echo off
echo ===================================================
echo WHATSAPP AUTO SENDER - ADMIN MODE
echo ===================================================
echo.

REM Pindah ke direktori script
cd /d "%~dp0"

REM Metode langsung menggunakan Python dari venv
echo Menjalankan script dengan Python dari virtual environment...
echo.

.\.venv\Scripts\python.exe sendMessage.py

echo.
echo Script selesai dijalankan.
pause