🚀 Proyecto Fullstack

Este proyecto se divide en Backend y Frontend, cada uno en su propio repositorio.
A continuación se detallan los pasos para levantar todo el entorno de desarrollo correctamente.

📂 Clonar repositorios

Primero clonar ambos proyectos:

# Clonar backend
git clone https://github.com/LeandroPossanzini/backend.git

# Clonar frontend
git clone https://github.com/LeandroPossanzini/frontend.git

⚙️ Backend

Ir al directorio del backend:

cd backend


Crear y activar el entorno virtual:

python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows


Instalar dependencias:

pip install -r requirements.txt


Ejecutar el proceso batch (necesario antes de iniciar la app):

python process_batch.py


Levantar el servidor:

python app.py


Acceder a la documentación del backend:
👉 http://127.0.0.1:5000/docs

💻 Frontend

Ir al directorio del frontend:

cd frontend


Crear y activar el entorno virtual:

python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows


Instalar dependencias:

pip install -r requirements.txt

✅ Testing

Para correr los tests en el backend:

pytest


Si se desea obtener el reporte de cobertura:

coverage run -m pytest
coverage report -m

📝 Notas

El backend corre por defecto en http://127.0.0.1:5000.

Asegúrate de ejecutar el proceso batch antes de iniciar la aplicación.

Frontend y backend deben levantarse en consolas separadas.