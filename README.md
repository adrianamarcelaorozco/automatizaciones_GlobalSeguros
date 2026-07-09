# 🧪 Automatizaciones Global Seguros

Repositorio de automatización de pruebas para el proyecto **Global Seguros**, utilizando Python, Selenium y una arquitectura unificada BDD (Behavior-Driven Development) bajo el patrón POM (Page Object Model).

---

## 📋 Requisitos Previos

Antes de comenzar, asegúrate de tener instalado lo siguiente en tu máquina:
* **Python 3.10 o superior**
* **Google Chrome** (Navegador donde se ejecutan las pruebas)
* **Visual Studio Code** (Opcional, para desarrollo)

---

## 🚀 Configuración Inicial

Sigue estos pasos para preparar el entorno en tu máquina local:

### 1. Clonar y abrir el proyecto

```bash
# Clonar el proyecto desde GitHub
git clone https://github.com/adrianamarcelaorozco/automatizaciones_GlobalSeguros.git

# Entrar a la carpeta del proyecto
cd automatizaciones_GlobalSeguros
```

* Abre Visual Studio Code, selecciona **Open Folder** y carga esta carpeta.

### 2. Configurar el Entorno Virtual (venv)

```bash
# Crear el entorno virtual
python3 -m venv venv

# Activar el entorno virtual en macOS / Linux
source venv/bin/activate
```

*(Cuando esté activo, verás un (venv) al principio de tu línea de comandos en la terminal).*

### 3. Instalar Dependencias

```bash
pip install -r requirements.txt
```

---

## 🧪 Ejecución de Pruebas (BDD)

> ⚠️ **Nota de Red:** Recuerda que para ejecutar las pruebas sobre el Portal corporativo es obligatorio tener la **VPN empresarial activa**, de lo contrario los entornos privados no responderán.

Asegúrate de tener el entorno virtual activo y ejecuta tus escenarios con:

```bash
# Ejecutar todas las pruebas BDD con Behave
behave
```

### Opciones de ejecución útiles:

```bash
# Ejecutar una característica o feature específica
behave features/tu_archivo.feature

# Ver la salida detallada de los pasos de prueba
behave --no-capture
```

---

## 📂 Estructura del Proyecto

```text
/features
  ├── *.feature          # Escenarios de prueba en lenguaje Gherkin
  └── /steps             # Implementación de los pasos en Python
/pages                   # Mapa del sitio (Page Object Model - Localizadores y Acciones)
├── environment.py       # Configuración de Hooks de Behave (WebDriver, Red, Timeouts)
├── requirements.txt     # Herramientas y librerías externas del proyecto
└── README.md            # Documentación del repositorio
```

---

## 🔧 Comandos Básicos de Git

### Flujo de trabajo diario

```bash
# Ver estado actual del repositorio
git status

# Agregar cambios al área de preparación
git add .

# Crear commit con tus cambios
git commit -m "feat: descripción clara del avance en QA"

# Subir cambios a tu rama de trabajo
git push origin tu_rama
```

### 🧹 Limpieza de ramas antiguas (Post-Merge)
Cuando una rama ya se fusionó en la nube y quieras limpiar tu entorno local:

```bash
# 1. Regresar a la rama principal
git checkout main

# 2. Traer cambios y limpiar el historial de ramas borradas en la nube
git pull --prune

# 3. Borrar la rama local de forma segura
git branch -d nombre_de_tu_rama
```

---

## 📌 Buenas prácticas QA

* Mantener los archivos .feature legibles y separados por responsabilidades de negocio.
* No duplicar la lógica de los localizadores; centralizarlos siempre dentro de la capa /pages.
* Asegurar commits descriptivos siguiendo estándares limpios (feat:, fix:, refactor:).
* Trabajar con ramas ordenadas para cada flujo o corrección.

---

## 👩‍💻 Autor

Proyecto desarrollado por Adriana Orozco como parte de la estrategia de automatización QA de Global Seguros.
