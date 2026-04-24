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


## 🛠️ Proyecto de Automatización - GlobalSeguros
Este proyecto contiene pruebas automatizadas para el Portal EM, desarrolladas con Python y Selenium. Está diseñado bajo el patrón de diseño POM (Page Object Model) para garantizar que sea fácil de mantener y escalar.

## 📋 Requisitos Previos
Antes de comenzar, asegúrate de tener instalado lo siguiente en tu computador:

Python 3.10 o superior: Descargar aquí (Al instalar, marca la casilla "Add Python to PATH").

Google Chrome: Las pruebas se ejecutan en este navegador.

Visual Studio Code (Opcional): Para visualizar el código.

## 🚀 Configuración Inicial
Sigue estos pasos para preparar el entorno en tu máquina local:

Abrir una terminal en la carpeta del proyecto.

Crear un entorno virtual (para no afectar otros programas):

PowerShell
python -m venv venv
Activar el entorno virtual:

En Windows: .\venv\Scripts\activate

Instalar las librerías necesarias:

PowerShell
pip install -r requirements.txt

## 📂 Estructura del Proyecto
Para entender cómo está organizado el código:

pages/: Contiene el "mapa" del sitio web. Aquí se definen los botones y campos de texto de cada página.

test/: Contiene las pruebas reales (los pasos que Selenium seguirá).

conftest.py: Configuración del navegador (Chrome).

pytest.ini: Configuración técnica para que las pruebas se ejecuten correctamente.

requirements.txt: Lista de herramientas externas que el proyecto necesita.

## 🧪 Cómo Ejecutar las Pruebas
Una vez configurado el entorno, ejecutar las pruebas es muy sencillo:

Asegúrate de tener el entorno virtual activo (verás un (venv) al principio de tu línea de comandos).

Escribe el siguiente comando y presiona Enter:

PowerShell
pytest
Opciones de ejecución:
Si quieres ver el detalle paso a paso en la terminal: pytest -v -s

Las pruebas abrirán una ventana de Chrome automáticamente y realizarán las acciones programadas.
