"""Pasos del beneficiario sin colegio y de la pantalla de financiación."""
from datetime import date, timedelta

from behave import step

from pages.financiacion_page import FinanciacionPage, a_numero


def _fecha_nacimiento_para_edad(anios):
    """Fecha (dd/mm/aaaa) de alguien que hoy tiene 'anios' años cumplidos.
    Se resta además unos 60 días para no caer en una fecha futura ni en el día del cumpleaños."""
    hoy = date.today() - timedelta(days=60)
    try:
        fecha = hoy.replace(year=hoy.year - anios)
    except ValueError:  # 29 de febrero en un año que no es bisiesto
        fecha = hoy.replace(year=hoy.year - anios, day=28)
    return fecha.strftime("%d/%m/%Y")


@step('diligencia la cotización para un beneficiario de {anios:d} años sin datos de colegio')
def step_diligenciar_sin_colegio(context, anios):
    """Igual que la cotización normal, pero con la edad indicada y SIN la sección 'Datos sobre el colegio'
    (solo se llena si el beneficiario estudia en colegio)."""
    pagina = context.pagina_cotizacion
    fecha = _fecha_nacimiento_para_edad(anios)
    print(f"[QA Info] Beneficiario de {anios} años, fecha de nacimiento {fecha}, sin datos de colegio.")

    pagina.ubicar_formulario_cotizador()
    pagina.asegurar_seccion_beneficiario_visible()
    pagina.seleccionar_tipo_documento_beneficiario("Registro Civil")
    pagina.diligenciar_datos_aleatorios_beneficiario(fecha_nacimiento=fecha)
    pagina.seleccionar_producto_materialize("Global Garantizada 360")
    pagina.calcular_y_confirmar_anio_ingreso()


@step('escribe "{texto}" en las observaciones')
def step_observaciones(context, texto):
    context.pagina_cotizacion.escribir_observaciones(texto)


@step('da clic en el botón "Cotizar financiación"')
def step_abrir_financiacion(context):
    context.pagina_financiacion = FinanciacionPage(context.driver)
    context.pagina_financiacion.abrir_desde_resumen()


@step('ingresa un valor de cuota inicial de "{valor}"')
def step_cuota_inicial(context, valor):
    context.cuota_inicial = valor
    context.pagina_financiacion.ingresar_valor_cuota_inicial(valor)


@step('calcula la financiación con el botón "Cotizar financiación"')
def step_calcular_financiacion(context):
    context.pagina_financiacion.calcular_financiacion()


@step('el sistema debe mostrar la tabla de financiación para el producto "{producto}"')
def step_validar_tabla(context, producto):
    context.resultado_financiacion = context.pagina_financiacion.leer_resultado()
    obtenido = context.resultado_financiacion.get("producto", "")
    assert obtenido == producto, \
        f"Error de Negocio: La tabla muestra el producto '{obtenido}' y se esperaba '{producto}'."


@step('la cuota inicial de la tabla debe ser la ingresada')
def step_validar_cuota_inicial(context):
    r = context.resultado_financiacion
    assert a_numero(r["cuota_inicial"]) == a_numero(context.cuota_inicial), \
        f"Error de Negocio: Cuota inicial en tabla {r['cuota_inicial']}, se ingresó {context.cuota_inicial}."


@step('el valor a financiar debe ser la prima menos la cuota inicial')
def step_validar_valor_a_financiar(context):
    r = context.resultado_financiacion
    prima, cuota, financiar = a_numero(r["prima"]), a_numero(r["cuota_inicial"]), a_numero(r["valor_a_financiar"])
    assert financiar == prima - cuota, \
        f"Error de Negocio: Valor a financiar {financiar:,} y se esperaba {prima:,} - {cuota:,} = {prima - cuota:,}."
    print(f"[QA Info] Valor a financiar correcto: {prima:,} - {cuota:,} = {financiar:,}")


@step('el porcentaje de cuota inicial debe corresponder a la cuota sobre la prima')
def step_validar_porcentaje(context):
    r = context.resultado_financiacion
    esperado = round(a_numero(r["cuota_inicial"]) * 100 / a_numero(r["prima"]))
    obtenido = a_numero(r["ci"])
    assert abs(obtenido - esperado) <= 1, \
        f"Error de Negocio: CI en tabla {obtenido}% y se esperaba aproximadamente {esperado}%."


@step('todas las cuotas mensuales deben tener valor mayor a cero')
def step_validar_cuotas(context):
    cuotas = context.resultado_financiacion["cuotas"]
    assert cuotas, "Error de Negocio: La tabla no muestra cuotas por plazo."
    for cuota in cuotas:
        assert a_numero(cuota) > 0, f"Error de Negocio: Hay una cuota en cero o vacía: '{cuota}'."
    print(f"[QA Info] Cuotas por plazo: {cuotas}")
