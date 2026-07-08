import time
from behave import given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.inicio_sesion_page import LoginPage

@given('que el analista de QA ha iniciado sesión en el portal')
def step_impl_login_puro(context):
    """Precondición: Abre el navegador, limpia caché de sesión y realiza el login básico."""
    context.login_page = LoginPage(context.driver)
    context.login_page.open()
    
    # Limpieza preventiva de cookies y almacenamiento para iniciar limpios
    try:
        context.driver.delete_all_cookies()
        context.driver.execute_script("window.localStorage.clear(); window.sessionStorage.clear();")
        context.driver.refresh()
    except Exception:
        pass

    # Control del modal informativo inicial de ASPX
    try:
        context.login_page.cerrar_modal_si_aparece()
    except Exception:
        pass
        
    # Inyectamos credenciales fijas para la autenticación
    context.login_page.login("NCRUZV", "Clave123")


@when('navega a la sección de cotizaciones')
def step_impl_navegacion_cotizaciones(context):
    """Acción: Espera la estabilización de la página post-login e ingresa al iframe operativo."""
    # Espera corta para garantizar que el modal gris de fondo desapareció por completo
    try:
        WebDriverWait(context.driver, 10).until(
            EC.invisibility_of_element_located(context.login_page.MODAL_INICIAL)
        )
    except Exception:
        pass
        
    time.sleep(2)

    # Cambio de contexto al iframe principal (id='contenido') donde se renderizan los módulos
    WebDriverWait(context.driver, 15).until(
        EC.frame_to_be_available_and_switch_to_it((By.ID, "contenido"))
    )


@then('el sistema debe mostrar las opciones de "Mis Cotizaciones" y "Adición de Semestre"')
def step_impl_verificar_opciones_inicio(context):
    """Resultado esperado: Valida la presencia visual de los botones usando localizadores XPath híbridos."""
    # Validación del botón de Mis Cotizaciones
    btn_cotizaciones = context.login_page.wait.until(
        EC.visibility_of_element_located(context.login_page.BTN_MIS_COTIZACIONES)
    )
    assert btn_cotizaciones.is_displayed(), "Error crítico: El botón de 'Mis Cotizaciones' no está visible en la interfaz."
        
    # Validación del botón de Adición de Semestre
    btn_semestres = context.login_page.wait.until(
        EC.visibility_of_element_located(context.login_page.BTN_ADICION_SEMESTRE)
    )
    assert btn_semestres.is_displayed(), "Error crítico: El botón de 'Adición de Semestres' no está visible en la interfaz."
        
    print("[QA Info] Smoke Test Exitoso: Los componentes 'Mis Cotizaciones' y 'Adición de Semestres' cargaron correctamente.")