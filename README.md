# 🧪 Automatizaciones Global Seguros

Repositorio de automatización de pruebas para el proyecto **Global Seguros**, utilizando buenas prácticas de control de versiones con Git y ejecución de pruebas automatizadas.

---

## 🚀 Configuración del proyecto

### 1. Inicializar repositorio Git

```bash
git init
```

---

### 2. Clonar el repositorio

Clonar el proyecto desde GitHub:

```bash
git clone https://github.com/adrianamarcelaorozco/automatizaciones_GlobalSeguros.git
```

---

### 3. Conectar con repositorio remoto

En caso de no estar vinculado:

```bash
git remote add origin https://github.com/adrianamarcelaorozco/automatizaciones_GlobalSeguros.git
```

Validar conexión:

```bash
git remote -v
```

---

### 4. Abrir el proyecto

* Abrir Visual Studio Code
* Seleccionar **Open Folder**
* Cargar la carpeta del proyecto clonado

---

## 🧪 Ejecución de pruebas

Ejecutar pruebas automatizadas con pytest:

```bash
pytest tests/test_consulta.py
```

---

## 🔧 Comandos básicos de Git

### Ver estado del repositorio

```bash
git status
```

### Agregar cambios

```bash
git add .
```

### Crear commit

```bash
git commit -m "Descripción de los cambios"
```

### Subir cambios al repositorio

```bash
git push origin main
```

### Traer cambios del repositorio

```bash
git pull origin main
```

---

## 📌 Buenas prácticas QA

* Mantener commits claros y descriptivos
* Ejecutar pruebas antes de subir cambios
* Trabajar con ramas cuando sea necesario (`feature`, `bugfix`)
* Validar que los tests pasen correctamente antes de hacer push

---

## 📁 Estructura básica del proyecto

```
/tests
  └── test_consulta.py
```

---

## 👩‍💻 Autor

Proyecto desarrollado por Adriana Orozco como parte de automatización QA.

---
