import os
import subprocess
import requests
import time
import threading

# Ruta al entorno virtual
VENV_ACTIVATE = os.path.join(".venv", "Scripts", "activate")  # Cambia ".venv" si tu entorno tiene otro nombre.

# Función para leer y mostrar los mensajes del servidor Flask
def read_server_output(process):
    while True:
        output = process.stdout.readline()
        error = process.stderr.readline()
        if output:
            print(output.strip())
        if error:
            print(f"Error: {error.strip()}", flush=True)
        if process.poll() is not None:
            break

# Paso 1: Activar el entorno virtual
if os.path.exists(VENV_ACTIVATE):
    print("Activando el entorno virtual...")
    subprocess.call(f"call {VENV_ACTIVATE} & echo Entorno virtual activado.", shell=True)
else:
    print("No se encontró el entorno virtual. Asegúrate de que '.venv' exista y esté configurado correctamente.")
    exit(1)

# Paso 2: Iniciar el servidor local
print("Iniciando servidor web...")
server_process = subprocess.Popen(
    ["python", "main.py"],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True  # Esto convierte la salida a texto automáticamente
)

# Crear un hilo para leer la salida del servidor Flask
server_output_thread = threading.Thread(target=read_server_output, args=(server_process,))
server_output_thread.daemon = True
server_output_thread.start()

# Paso 3: Iniciar Ngrok
print("Iniciando Ngrok...")
ngrok_process = subprocess.Popen(
    ["ngrok", "http", "8080"],  # Cambia "8080" al puerto de tu servidor local Flask
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)

# Paso 4: Esperar unos segundos para que Ngrok genere la URL pública
time.sleep(5)

# Paso 5: Obtener la URL pública de Ngrok
try:
    response = requests.get("http://localhost:4040/api/tunnels")
    response_data = response.json()
    public_url = response_data['tunnels'][0]['public_url']
    print(f"\nTu sitio web está disponible en: {public_url}\n")
except Exception as e:
    print("Error obteniendo la URL de Ngrok:", e)

# Mantener los procesos activos y permitir la interrupción con Ctrl+C
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\nCerrando procesos...")
    server_process.terminate()
    ngrok_process.terminate()
    print("Procesos cerrados.")
