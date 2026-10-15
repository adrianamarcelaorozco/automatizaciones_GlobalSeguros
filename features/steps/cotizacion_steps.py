"""Pasos del cotizador en línea."""
import time

from behave import step

from pages.cotizacion_page import CotizacionPage


@step('el analista se desplaza hasta la sección "Opciones de Cotización"')
def step_scroll_opciones(context):
    context.pagina_cotizacion = CotizacionPage(context.driver)

    if hasattr(context, 'documento_random'):
        print(f"[QA INFO] Flujo continuo: Cotizando al cliente recién registrado: {context.documento_random}")
    else:
        print("[QA INFO] Advertencia: No se detectó cliente previo.")

    context.pagina_cotizacion.scroll_hasta_opciones_cotizacion()


@step('selecciona el producto "Global Educacion Garantizada 360"')
def step_seleccionar_producto(context):
    context.pagina_cotizacion.seleccionar_global_educacion_360()


@step('el sistema debe abrir la pantalla "Cotizador en Línea"')
def step_validar_cotizador(context):
    context.pagina_cotizacion.cambiar_a_ventana_cotizador()
    context.pagina_cotizacion.validar_pantalla_cotizador()
    time.sleep(1)


@step('diligencia la información requerida para la cotización')
def step_diligenciar_cotizacion(context):
    pagina = context.pagina_cotizacion
    pagina.ubicar_formulario_cotizador()
    pagina.asegurar_seccion_beneficiario_visible()
    pagina.seleccionar_tipo_documento_beneficiario("Registro Civil")
    pagina.diligenciar_datos_aleatorios_beneficiario()
    pagina.diligenciar_datos_colegio(
        depto_text="DISTRITO CAPITAL",
        institucion_nombre="COLEGIO NACIONAL ANDRES BELLO",
        curso_val="TERCERO",
    )
    pagina.seleccionar_producto_materialize("Global Garantizada 360")
    pagina.calcular_y_confirmar_anio_ingreso()


@step('hace clic en el botón "Cotizar"')
def step_cotizar(context):
    context.pagina_cotizacion.clic_cotizar()


@step('selecciona todas las coberturas y da clic en "Continuar"')
def step_seleccionar_coberturas(context):
    context.pagina_cotizacion.seleccionar_todas_coberturas_y_continuar()


@step('el sistema debe generar la cotización correctamente')
def step_validar_cotizacion(context):
    context.pagina_cotizacion.validar_resumen_cotizacion()


@step('cierra la cotización con el botón "Cerrar"')
def step_cerrar_cotizacion(context):
    context.pagina_cotizacion.cerrar_desde_resumen()

    print("[QA INFO] Devolviendo el foco a la ventana principal...")
    context.pagina_cotizacion.volver_a_ventana_principal()
    print("[QA Info] ¡Prueba finalizada con éxito!")

    # Pausa solo para revisión visual (quitar o reducir en ejecución desatendida)
    time.sleep(10)
