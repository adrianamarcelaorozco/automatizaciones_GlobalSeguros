"""Pasos reutilizables por todos los flujos: login, menú principal y búsqueda de cliente.

Se usa @step (en vez de @given/@when/@then) para que cada frase funcione con
cualquier palabra clave: Dado, Cuando, Y, Entonces.
"""
import time

from behave import step

from config import USUARIO_QA, CLAVE_QA
from pages.inicio_sesion_page import LoginPage
from pages.cliente_nuevo_page import BusquedaClientePage, TipoDocumento
from utils.datos_prueba import generar_datos_cliente


@step('que el analista de QA ha iniciado sesión en el portal')
def step_login(context):
    context.login_page = LoginPage(context.driver)
    context.login_page.iniciar_sesion_limpia(USUARIO_QA, CLAVE_QA)


@step('navega a la sección de cotizaciones')
def step_navegar_cotizaciones(context):
    context.login_page.ir_a_modulo_cotizaciones()


@step('el sistema debe mostrar las opciones de "Mis Cotizaciones" y "Adición de Semestre"')
def step_validar_opciones_menu(context):
    context.login_page.validar_opciones_menu()


@step('ingresa a "Mis Cotizaciones"')
def step_ingresar_mis_cotizaciones(context):
    context.login_page.click_mis_cotizaciones()


@step('busca un documento único para el tipo "{tipo_doc_key}"')
def step_buscar_documento(context, tipo_doc_key):
    context.pagina_busqueda = BusquedaClientePage(context.driver)
    context.pagina_busqueda.entrar_iframe_contenido()

    context.tipo_doc_enum = TipoDocumento[tipo_doc_key]
    datos = generar_datos_cliente(context.tipo_doc_enum)
    context.documento_random = datos["documento"]
    context.correo_dinamico = datos["correo"]
    context.celular_dinamico = datos["celular"]

    context.pagina_busqueda.ingresar_y_buscar_cliente(
        numero_documento=context.documento_random,
        tipo_documento=context.tipo_doc_enum,
    )


@step('el sistema debe habilitar la opción para registrar al nuevo cliente')
def step_validar_nuevo_cliente(context):
    context.pagina_busqueda.validar_nuevo_cliente_habilitado()


@step('avanza al formulario para registrar al nuevo cliente')
def step_abrir_formulario_nuevo_cliente(context):
    context.pagina_busqueda.click_nuevo_cliente()
    print(f"[QA Info] Formulario abierto para {context.tipo_doc_enum.name}. Esperando estabilización...")
    time.sleep(4.0)  # El formulario tarda en cargar por la lentitud del servidor
