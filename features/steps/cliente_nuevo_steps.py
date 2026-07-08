import time
from behave import given, when, then
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from pages.cliente_nuevo_page import BusquedaClientePage, TipoDocumento
from pages.inicio_sesion_page import LoginPage

@given('que el analista de QA ha iniciado sesión y navegado a la sección de cotizaciones')
def step_impl_login_y_navegacion(context):
    login_page = LoginPage(context.driver)
    login_page.open()
    
    try:
        context.driver.delete_all_cookies()
        context.driver.execute_script("window.localStorage.clear();")
        context.driver.execute_script("window.sessionStorage.clear();")
        context.driver.refresh() 
    except Exception:
        pass

    try:
        login_page.cerrar_modal_si_aparece() 
    except Exception:
        pass
        
    login_page.login("NCRUZV", "Clave123")
    
    try:
        WebDriverWait(context.driver, 12).until(
            EC.invisibility_of_element_located((By.ID, "mpeMensajeNoCliente_backgroundElement"))
        )
    except:
        pass
        
    time.sleep(4)

    # Ingresar al mensaje inicial
    WebDriverWait(context.driver, 15).until(
        EC.frame_to_be_available_and_switch_to_it((By.ID, "contenido"))
    )

    # Interacción con Mis Cotizaciones
    elemento = WebDriverWait(context.driver, 20).until(
        EC.presence_of_element_located(login_page.BTN_MIS_COTIZACIONES)
    )
    try:
        WebDriverWait(context.driver, 5).until(EC.element_to_be_clickable(login_page.BTN_MIS_COTIZACIONES))
        elemento.click()
    except Exception:
        context.driver.execute_script("arguments[0].click();", elemento)


@when('busca un documento único para el tipo "{tipo_doc_key}"')
def step_impl_buscar_cliente(context, tipo_doc_key):
    context.driver.switch_to.default_content()
    WebDriverWait(context.driver, 15).until(
        EC.frame_to_be_available_and_switch_to_it((By.ID, "contenido"))
    )
    
    context.pagina_busqueda = BusquedaClientePage(context.driver)
    context.tipo_doc_enum = TipoDocumento[tipo_doc_key]
    
    # Generación de datos únicos
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

@when('avanza al formulario para registrar al nuevo cliente')
def step_impl_click_nuevo(context):
    context.pagina_busqueda.click_nuevo_cliente()
    print(f"[QA Info] Formulario abierto para {context.tipo_doc_enum.name}. Esperando estabilización...")
    time.sleep(4.0)

# Reemplaza la cabecera de este step en tu archivo de pasos:
@when('completa los datos personales y geográficos para el tipo "{tipo_doc_key}"')
def step_impl_completar_formulario(context, tipo_doc_key):
    context.pagina_busqueda.completar_datos_personales(
        numero_documento=context.documento_random,
        tipo_documento=context.tipo_doc_enum,
        correo=context.correo_dinamico,
        celular=context.celular_dinamico,
        departamento="ALEATORIO", 
        ciudad="CIUDAD_AUTOMATICA"
    )


@then('el sistema debe confirmar que la grabación se realizó correctamente')
def step_impl_verificar_grabacion(context):
    mensaje_capturado = context.pagina_busqueda.obtener_mensaje_exito_y_cerrar()
    assert "Grabación realizada correctamente" in mensaje_capturado, \
        f"Error de Negocio: Mensaje inesperado en pantalla: '{mensaje_capturado}'"
    print(f"[QA Info] Guardado exitoso verificado para documento: {context.documento_random}")

