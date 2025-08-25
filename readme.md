# 🚀 Proyecto Fullstack

Este proyecto se divide en **Backend** y **Frontend**, cada uno en su propio repositorio. A continuación se detallan los pasos para levantar todo el entorno de desarrollo correctamente.

---

## 📂 Clonar repositorios

```bash
# Clonar backend
git clone https://github.com/LeandroPossanzini/backend.git

# Clonar frontend
git clone https://github.com/LeandroPossanzini/frontend.git
```

---

## ⚙️ Backend

### 1️⃣ Ir al directorio del backend
```bash
cd backend
```

### 2️⃣ Crear y activar el entorno virtual
```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```

### 3️⃣ Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4️⃣ Ejecutar el proceso batch
> Necesario antes de iniciar la app
```bash
python process_batch.py
```

### 5️⃣ Levantar el servidor
```bash
python app.py
```

### 6️⃣ Acceder a la documentación del backend
👉 [http://127.0.0.1:5000/docs](http://127.0.0.1:5000/docs)

---

## 💻 Frontend

### 1️⃣ Ir al directorio del frontend
```bash
cd frontend
```

### 2️⃣ Crear y activar el entorno virtual
```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```

### 3️⃣ Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4️⃣ Levantar el servidor
```bash
python app.py
```

---

## ✅ Testing

### Ejecutar tests en el backend
```bash
pytest
```

### Generar reporte de cobertura
```bash
coverage run -m pytest
coverage report -m
```

---

## 📝 Notas importantes

> ⚠️ **Recuerda:**  
> - El backend corre por defecto en `http://127.0.0.1:5000`.  
> - Ejecutar el **proceso batch** antes de levantar la app.  
> - Frontend y backend deben correr en **consolas separadas**.



