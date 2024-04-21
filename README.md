Instalación

Debe tener instalado
- Docker
- Python3
- Navegador Web

Para ejecutar este proyecto localmente, siga estos pasos:

Clona el repositorio en tu máquina local usando el siguiente comando:

git clone https://github.com/robertohm16/proyecto-videoclub-python.git

Navega hasta el directorio del proyecto:

cd proyecto-videoclub-python

Crea un entorno virtual para aislar las dependencias del proyecto:

python -m venv env

Activa el entorno virtual:
En macOS y Linux
  
  source env/bin/activate
  
En Windows
  
  .\env\Scripts\activate

Ejecutar el servidor local Flask

python3 app.py

Ejecutar el microservicio

docker build -t videoapp:latest .

docker run -p 4000:4000 videoapp:latest

