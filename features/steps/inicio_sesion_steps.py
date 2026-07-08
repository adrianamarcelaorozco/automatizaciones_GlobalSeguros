import time
from behave import given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.inicio_sesion_page import LoginPage
from pages.cliente_nuevo_page import BusquedaClientePage, TipoDocumento

@given('que el analista de QA ha iniciado sesión en el portal')
def step_impl_login_puro(context):
    """Precondición: Abre el navegador, limpia caché de sesión y realiza el login básico."""
    context.login_page = LoginPage(context.driver)
    context.login_page.open()
    
    try:
        context.driver.delete_all_cookies()
        context.driver.execute_script("window.localStorage.clear(); window.sessionStorage.clear();")
        context.driver.refresh()
    except Exception:
        pass

    try:
        context.login_page.cerrar_modal_si_aparece()
    except Exception:
        pass
        
    context.login_page.login("NCRUZV", "Clave123")


@when('navega a la sección de cotizaciones')
def step_impl_navegacion_cotizaciones(context):
    """Acción: Espera la estabilización de la página post-login e ingresa al iframe operativo."""
    try:
        WebDriverWait(context.driver, 10).until(
            EC.invisibility_of_element_located(context.login_page.MODAL_INICIAL)
        )
    except Exception:
        pass
        
    try:
        WebDriverWait(context.driver, 12).until(
            EC.invisibility_of_element_located((By.ID, "mpeMensajeNoCliente_backgroundElement"))
        )
    except:
        pass
        
    time.sleep(2)

    # Cambio de contexto al iframe principal (id='contenido') donde se renderizan los módulos
    WebDriverWait(context.driver, 15).until(
        EC.frame_to_be_available_and_switch_to_it((By.ID, "contenido"))
    )


@when('el sistema debe mostrar las opciones de "Mis Cotizaciones" y "Adición de Semestre"')
@then('el sistema debe mostrar las opciones de "Mis Cotizaciones" y "Adición de Semestre"')
def step_impl_verificar_opciones_inicio(context):
    """Resultado esperado: Valida la presencia visual de los botones utilizando los localizadores."""
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

    # Hacer clic en Mis Cotizaciones para abrir el flujo de búsqueda de clientes
    try:
        WebDriverWait(context.driver, 5).until(EC.element_to_be_clickable(context.login_page.BTN_MIS_COTIZACIONES))
        btn_cotizaciones.click()
    except Exception:
        context.driver.execute_script("arguments[0].click();", btn_cotizaciones)


@when('busca un documento único para el tipo "{tipo_doc_key}"')
@then('busca un documento único para el tipo "{tipo_doc_key}"')
def step_impl_buscar_cliente(context, tipo_doc_key):
    """Asegura el contexto del iframe e ingresa los datos del documento dinámico."""
    context.driver.switch_to.default_content()
    WebDriverWait(context.driver, 15).until(
        EC.frame_to_be_available_and_switch_to_it((By.ID, "contenido"))
    )
    
    context.pagina_busqueda = BusquedaClientePage(context.driver)
    context.tipo_doc_enum = TipoDocumento[tipo_doc_key]
    
    # Generación de datos únicos basados en marcas de tiempo
    tiempo_actual = str(int(time.time()))
    if context.tipo_doc_enum == TipoDocumento.CIUDADANIA:
        semilla = tiempo_actual[-7:]
        context.documento_random = "10" + semilla
    elif context.tipo_doc_enum == TipoDocumento.EXTRANJERIA:
        semilla = tiempo_actual[-7:]
        context.documento_random = "90" + semilla
    else:
        semilla = tiempo_actual[-5:]
        context.documento_random = "5" + semilla

    context.correo_dinamico = f"qa_global_{context.tipo_doc_enum.name.lower()}_{semilla}@globaleguros.com"
    context.celular_dinamico = "312" + tiempo_actual[-7:]
    
    context.pagina_busqueda.ingresar_y_buscar_cliente(
        numero_documento=context.documento_random, 
        tipo_documento=context.tipo_doc_enum
    )


@when('el sistema debe habilitar la opción para registrar al nuevo cliente')
@then('el sistema debe habilitar la opción para registrar al nuevo cliente')
def step_impl_click_nuevo(context):
    context.pagina_busqueda.click_nuevo_cliente()
    print(f"[QA Info] Formulario abierto para {context.tipo_doc_enum.name}. Esperando estabilización...")
    time.sleep(4.0)