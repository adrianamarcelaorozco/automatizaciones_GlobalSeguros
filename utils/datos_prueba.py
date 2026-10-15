"""Generación de datos de prueba únicos para cada ejecución."""
import time

from pages.cliente_nuevo_page import TipoDocumento


def generar_datos_cliente(tipo_documento: TipoDocumento) -> dict:
    """Devuelve documento, correo y celular únicos basados en la marca de tiempo actual."""
    tiempo_actual = str(int(time.time()))

    if tipo_documento == TipoDocumento.CIUDADANIA:
        semilla = tiempo_actual[-7:]
        documento = "10" + semilla
    elif tipo_documento == TipoDocumento.EXTRANJERIA:
        semilla = tiempo_actual[-7:]
        documento = "90" + semilla
    else:
        semilla = tiempo_actual[-5:]
        documento = "5" + semilla

    return {
        "documento": documento,
        "correo": f"qa_global_{tipo_documento.name.lower()}_{semilla}@globaleguros.com",
        "celular": "312" + tiempo_actual[-7:],
    }
