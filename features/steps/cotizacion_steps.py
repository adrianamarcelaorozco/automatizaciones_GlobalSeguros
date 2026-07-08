from behave import given, when, then
from pages.cotizacion_page import CotizacionPage

@given(u'que existe un cliente registrado con cédula de ciudadanía')
def step_impl_verificar_cliente(context):
    context.pagina_cotizacion = CotizacionPage(context.driver)
    
    # SI NO EXISTE EN EL CONTEXTO (ejecución aislada), generamos uno falso
    if not hasattr(context, 'documento_random'):
        print("[QA INFO] Ejecución aislada: Generando documento de respaldo...")
        datos = context.pagina_cotizacion.generar_beneficiario_random()
        context.documento_random = datos["numero_documento"]
    else:
        print(f"[QA INFO] Cliente recuperado: {context.documento_random}")

@when(u'el analista se desplaza hasta la sección "Opciones de Cotización"')
def step_impl_scroll(context):
    context.pagina_cotizacion.scroll_hasta_opciones_cotizacion()

@when(u'selecciona el producto "Global Educacion Garantizada 360"')
def step_impl_producto(context):
    context.pagina_cotizacion.seleccionar_global_educacion_360()

@then(u'el sistema debe abrir la pantalla "Cotizador en Línea"')
def step_impl_cambiar_ventana(context):
    context.pagina_cotizacion.cambiar_a_ventana_cotizador()
    context.pagina_cotizacion.validar_pantalla_cotizador()

@when(u'diligencia la información requerida para la cotización')
def step_impl_diligenciar_cotizacion(context):
    context.pagina_cotizacion.seleccionar_apoyo_institucional()
    context.pagina_cotizacion.seleccionar_evento()

@when(u'hace clic en el botón "Cotizar"')
def step_impl_clic_cotizar(context):
    context.pagina_cotizacion.clic_boton_cotizar()

@then(u'el sistema debe generar la cotización correctamente')
def step_impl_validar_cotizacion(context):
    resultado = context.pagina_cotizacion.obtener_resultado_cotizacion()
    # Validación lógica: comprobamos que el sistema responde
    assert resultado is not None, "El sistema no devolvió un resultado de cotización."
    print(f"[QA INFO] Resultado obtenido: {resultado}")