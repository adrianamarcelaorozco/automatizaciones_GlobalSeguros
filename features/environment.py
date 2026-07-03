import os
import sys
from selenium import webdriver

# OPTIMIZACIÓN: Simplificamos el cálculo de la raíz del proyecto
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

def before_scenario(context, scenario):
    """Inicializa un Chrome completamente limpio antes de CADA escenario."""
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    # Podrías agregar esta opción si quieres silenciar alertas basura en tu consola:
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    
    context.driver = webdriver.Chrome(options=options)

def after_scenario(context, scenario):
    """Garantiza la destrucción del proceso de Chrome para evitar fugas de memoria."""
    driver = getattr(context, "driver", None)
    if driver:
        try:
            driver.quit()
        except Exception:
            pass
        finally:
            # Eliminamos la referencia para asegurar limpieza absoluta en memoria
            context.driver = None