import pytest
import time
import os
import sys
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# Aseguramos que la raíz del proyecto esté en el sistema de rutas de Python
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Ahora la importación funcionará de manera nativa y directa
from pages.login_page import LoginPage

@pytest.fixture(scope="function")
def driver():
    """Crea una ventana limpia del navegador exclusivamente para CADA test."""
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    _driver = webdriver.Chrome(options=options)
    
    yield _driver
    
    # BLINDAJE EXTRA: Cerrar cualquier ventana secundaria colgada que rompa el siguiente test
    try:
        handles = _driver.window_handles
        for handle in handles[1:]:
            _driver.switch_to.window(handle)
            _driver.close()
        _driver.switch_to.window(handles[0])
        _driver.quit()
    except Exception:
        try:
            _driver.quit()
        except Exception:
            pass

@pytest.fixture(scope="function")
def login_autenticado(driver):
    """
    Garantiza el inicio de sesión completo y la transición exitosa
    hacia la sección de cotizaciones, manejando la limpieza de sesión
    y los modales emergentes repetidos.
    """
    login_page = LoginPage(driver)
    
    # 1. Entramos al dominio para habilitar el uso de JS y almacenamiento
    login_page.open()
    
    # 2. Limpiamos almacenamiento residual de inmediato
    try:
        driver.delete_all_cookies()
        driver.execute_script("window.localStorage.clear();")
        driver.execute_script("window.sessionStorage.clear();")
        # Refrescamos para aplicar la limpieza profunda
        driver.refresh() 
    except Exception:
        print("[QA Info] Advertencia: No se pudo limpiar el almacenamiento web.")

    # 3. ¡CORREGIDO!: Llamamos al nombre exacto del método de tu clase LoginPage
    try:
        login_page.cerrar_modal_si_aparece() 
        print("[QA Info] Proceso de validación de modal post-refresh ejecutado.")
    except Exception:
        print("[QA Info] No se detectó modal tras el refresh de página.")
        
    login_page.login("NCRUZV", "Clave123")
    
    # 2. Manejo del modal de carga inicial
    try:
        WebDriverWait(driver, 12).until(
            EC.invisibility_of_element_located((By.ID, "mpeMensajeNoCliente_backgroundElement"))
        )
        print("[QA Info] Modal inicial controlado.")
    except:
        pass
        
    # 3. Forzar espera de renderizado de la página ASPX
    time.sleep(4)
    
    # 4. Asegurar que el estado del documento sea 'complete'
    try:
        WebDriverWait(driver, 10).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
    except:
        print("[QA Info] Advertencia: La página no terminó de reportar 'complete'.")

    # =========================================================================
    # NUEVO PASO: Cambiar al iframe donde realmente está el botón de cotizaciones
    # =========================================================================
    try:
        print("[QA Info] Cambiando al iframe 'contenido'...")
        WebDriverWait(driver, 15).until(
            EC.frame_to_be_available_and_switch_to_it((By.ID, "contenido"))
        )
    except Exception:
        print("[QA Info] Advertencia crítico: No se pudo ingresar al iframe 'contenido'.")

    # 5. Intento robusto de interacción con el botón (con reintento por JS si se oculta)
    elemento = None
    ultimo_error = None
    
    # Intentamos buscarlo con una espera amplia (20 segundos) por si el servidor va lento
    try:
        print("[QA Info] Esperando presencia del botón 'IrCotizadores' dentro del iframe...")
        elemento = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(login_page.BTN_MIS_COTIZACIONES)
        )
        
        # Una vez presente, intentamos el clic tradicional si es cliqueable
        try:
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable(login_page.BTN_MIS_COTIZACIONES))
            elemento.click()
            print("[QA Info] Clic en 'Mis cotizaciones' ejecutado de forma tradicional.")
        except Exception:
            # Si no es cliqueable tradicionalmente, disparamos JS inmediatamente
            driver.execute_script("arguments[0].click();", elemento)
            print("[QA Info] Clic forzado mediante JavaScript exitoso.")
            
    except Exception as e:
        ultimo_error = e
        # REINTENTO EXTREMO: Si falló en la clase de pruebas, refrescamos una vez la página intermedia
        print("[QA Info] Botón no hallado. Aplicando refresco de contingencia...")
        driver.refresh()
        time.sleep(3)
        try:
            # Al refrescar la página se sale del iframe automáticamente; hay que volver a entrar
            print("[QA Info] Re-ingresando al iframe 'contenido' tras el refresco...")
            WebDriverWait(driver, 10).until(
                EC.frame_to_be_available_and_switch_to_it((By.ID, "contenido"))
            )
            
            elemento = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(login_page.BTN_MIS_COTIZACIONES)
            )
            driver.execute_script("arguments[0].click();", elemento)
            print("[QA Info] Clic exitoso mediante JS tras refrescar el sitio.")
            ultimo_error = None  # Se solucionó
        except Exception as re_error:
            ultimo_error = re_error

    # Si tras el intento y el reintento falló, lanzamos el error con contexto
    if ultimo_error:
        raise RuntimeError(
            f"Fallo crítico: El botón 'IrCotizadores' no apareció en el DOM. "
            f"URL final: {driver.current_url}"
        ) from ultimo_error

    return driver