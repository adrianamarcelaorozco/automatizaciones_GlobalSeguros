import time
from behave import given, when, then
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from pages.cliente_nuevo_page import BusquedaClientePage, TipoDocumento
from pages.inicio_sesion_page import LoginPage
from pages.cotizacion_page import CotizacionPage


@given('que el analista de QA nuevo ha iniciado sesión en el portal')
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


@when('navega a la sección de cotizaciones del nuevo flujo')
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
        
    time.sleep(4)

    # Cambio de contexto al iframe principal (id='contenido') donde se renderizan los módulos
    WebDriverWait(context.driver, 15).until(
        EC.frame_to_be_available_and_switch_to_it((By.ID, "contenido"))
    )

    # Interacción con Mis Cotizaciones
    elemento = WebDriverWait(context.driver, 20).until(
        EC.presence_of_element_located(context.login_page.BTN_MIS_COTIZACIONES)
    )
    try:
        WebDriverWait(context.driver, 5).until(EC.element_to_be_clickable(context.login_page.BTN_MIS_COTIZACIONES))
        elemento.click()
    except Exception:
        context.driver.execute_script("arguments[0].click();", elemento)


@when('busca un documento único para el nuevo tipo "{tipo_doc_key}"')
@then('busca un documento único para el nuevo tipo "{tipo_doc_key}"')
def step_impl_buscar_cliente(context, tipo_doc_key):
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


@when('avanza al formulario para registrar al nuevo cliente unificado')
@then('avanza al formulario para registrar al nuevo cliente unificado')
def step_impl_click_nuevo(context):
    context.pagina_busqueda.click_nuevo_cliente()
    print(f"[QA Info] Formulario unificado abierto para {context.tipo_doc_enum.name}. Esperando...")
    time.sleep(4.0)


@when('completa los datos personales y geográficos para el nuevo tipo "{tipo_doc_key}"')
@then('completa los datos personales y geográficos para el nuevo tipo "{tipo_doc_key}"')
def step_impl_completar_formulario(context, tipo_doc_key):
    context.pagina_busqueda.completar_datos_personales(
        numero_documento=context.documento_random,
        tipo_documento=context.tipo_doc_enum,
        correo=context.correo_dinamico,
        celular=context.celular_dinamico,
        departamento="ALEATORIO", 
        ciudad="CIUDAD_AUTOMATICA"
    )


@when('el sistema debe confirmar que la grabación del nuevo cliente se realizó correctamente')
@then('el sistema debe confirmar que la grabación del nuevo cliente se realizó correctamente')
def step_impl_verificar_grabacion(context):
    # Añadir un breve sleep o espera de invisibilidad del cargador si existe
    time.sleep(2.0) 
    mensaje_capturado = context.pagina_busqueda.obtener_mensaje_exito_y_cerrar()
    assert "Grabación realizada correctamente" in mensaje_capturado, \
        f"Error de Negocio: Mensaje inesperado en pantalla: '{mensaje_capturado}'"


@when('el analista se desplaza hasta la sección "Opciones de Cotización" del nuevo flujo')
@then('el analista se desplaza hasta la sección "Opciones de Cotización" del nuevo flujo')
def step_impl_scroll(context):
    # Instanciamos la página de cotización compartiendo el mismo driver
    context.pagina_cotizacion = CotizacionPage(context.driver)
    
    # Certificamos en consola que heredó el cliente recién creado en la variable de contexto
    if hasattr(context, 'documento_random'):
        print(f"[QA INFO] Flujo continuo: Cotizando al cliente recién registrado: {context.documento_random}")
    else:
        print("[QA INFO] Advertencia: No se detectó cliente previo.")
        
    context.pagina_cotizacion.scroll_hasta_opciones_cotizacion()


@when('selecciona el producto "Global Educacion Garantizada 360"')
@then('selecciona el producto "Global Educacion Garantizada 360"')
def step_impl_producto(context):
    context.pagina_cotizacion.seleccionar_global_educacion_360()


@when('el sistema debe abrir la pantalla "Cotizador en Línea"')
@then('el sistema debe abrir la pantalla "Cotizador en Línea"')
def step_impl_cambiar_ventana(context):
    context.pagina_cotizacion.cambiar_a_ventana_cotizador()
    context.pagina_cotizacion.validar_pantalla_cotizador()
    time.sleep(1)

@when('diligencia la información requerida para la cotización')
def step_impl_diligenciar_cotizacion(context):
    # 1. Asegurar que estamos en la ventana correcta (la última abierta)
    ventanas = context.driver.window_handles
    if len(ventanas) > 1:
        context.driver.switch_to.window(ventanas[-1])
    
    # 2. Solo buscar iframes dentro de esta ventana
    iframes = context.driver.find_elements(By.TAG_NAME, "iframe")
    if iframes:
        context.driver.switch_to.frame(iframes[0])

    # NUEVO: Asegurar visibilidad antes de interactuar
    context.pagina_cotizacion.asegurar_seccion_beneficiario_visible()
   
    # Proceder con las acciones
    # context.pagina_cotizacion.seleccionar_apoyo_institucional()
    
    # 2. Llamamos a nuestra nueva función para seleccionar el tipo de documento
    context.pagina_cotizacion.seleccionar_tipo_documento_beneficiario("Registro Civil")
    
    # 3. Llenamos toda la información personal con el nuevo método aleatorio
    context.pagina_cotizacion.diligenciar_datos_aleatorios_beneficiario()
    context.pagina_cotizacion.diligenciar_datos_colegio(
        depto_text="DISTRITO CAPITAL",
        institucion_nombre="COLEGIO NACIONAL ANDRES BELLO",
        curso_val="TERCERO"
    )
    

@when('hace clic en el botón "Cotizar"')
@then('hace clic en el botón "Cotizar"')
def step_impl_clic_cotizar(context):
    context.pagina_cotizacion.clic_boton_cotizar()


@then('el sistema debe generar la cotización correctamente')
def step_impl_validar_cotizacion(context):
    resultado = context.pagina_cotizacion.obtener_resultado_cotizacion()
    assert resultado is not None, "El sistema no devolvió un resultado de cotización."
    print(f"[QA INFO] ¡Flujo Unificado Exitoso! Resultado obtenido: {resultado}")