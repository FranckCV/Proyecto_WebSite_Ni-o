@echo off
:: Activar el entorno virtual si estás usando uno
call .venv\Scripts\activate

:: Ejecutar el servidor web (main.py)
start cmd /k python main.py

:: Esperar unos segundos para asegurarte de que el servidor esté arriba
timeout /t 5 >nul

:: Iniciar Ngrok en el puerto 8080 (ajusta si usas otro puerto)
start cmd /k ngrok http 8080

pause

