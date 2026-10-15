"""Pasos del formulario de registro de cliente."""
import time

from behave import step


@step('completa los datos personales y geográficos para el tipo "{tipo_doc_key}"')
def step_completar_formulario(context, tipo_doc_key):
    context.pagina_busqueda.completar_datos_personales(
        numero_documento=context.documento_random,
        tipo_documento=context.tipo_doc_enum,
        correo=context.correo_dinamico,
        celular=context.celular_dinamico,
        departamento="ALEATORIO",
        ciudad="CIUDAD_AUTOMATICA",
    )


@step('el sistema debe confirmar que la grabación del nuevo cliente se realizó correctamente')
def step_verificar_grabacion(context):
    time.sleep(2.0)
    mensaje = context.pagina_busqueda.obtener_mensaje_exito_y_cerrar()
    assert "Grabación realizada correctamente" in mensaje, \
        f"Error de Negocio: Mensaje inesperado en pantalla: '{mensaje}'"
