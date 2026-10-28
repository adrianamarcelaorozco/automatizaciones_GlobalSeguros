"""Pantalla de financiación (financiacion.aspx) del Cotizador en Línea."""
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from pages.base_page import BasePage


def a_numero(texto):
    """Convierte un valor de la tabla en número: '142.596.000' -> 142596000, '35%' -> 35."""
    limpio = texto.replace(".", "").replace("%", "").replace(",", ".").strip()
    return float(limpio) if "." in limpio else int(limpio)


class FinanciacionPage(BasePage):

    # El botón tiene el mismo id en el resumen y en la pantalla de financiación.
    # Si algún día cambia el id, se busca también por el texto del botón.
    BTN_COTIZAR_FINANCIACION = (By.XPATH, "//input[@id='CotizarFinanciacion' or @value='Cotizar financiación']")

    RADIO_VALOR_CUOTA_INICIAL = (By.ID, "optCiValor")
    CAMPO_VALOR_CUOTA_INICIAL = (By.ID, "CiValor")

    # Tabla de resultados: la fila de valores está en <tbody id="cuerpo">
    FILAS_RESULTADO = (By.CSS_SELECTOR, "#tablaProductos #cuerpo tr")

    # Orden de las columnas de la fila de resultados (ver encabezados de la tabla)
    COLUMNAS = ["producto", "prima", "ci", "cuota_inicial", "valor_a_financiar", "seguro_deudor"]

    def abrir_desde_resumen(self):
        """En el resumen da clic en 'Cotizar financiación' y espera la pantalla de financiación."""
        boton = WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable(self.BTN_COTIZAR_FINANCIACION))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", boton)
        time.sleep(1)
        self.driver.execute_script("arguments[0].click();", boton)
        print("[QA Info] Clic en 'Cotizar financiación' desde el resumen.")

        try:
            WebDriverWait(self.driver, 60).until(lambda d: "financiacion.aspx" in d.current_url.lower())
        except TimeoutException:
            raise AssertionError(
                f"Error de Negocio: No se abrió la pantalla de financiación. URL actual: {self.driver.current_url}"
            )
        self.esperar_postback()
        print(f"[QA Info] Pantalla de financiación cargada: {self.driver.current_url}")

    def ingresar_valor_cuota_inicial(self, valor):
        """Marca la opción 'Valor Cuota Inicial' y escribe el valor."""
        # El radio real está oculto por el diseño (Materialize); se marca con JavaScript
        radio = self.wait.until(EC.presence_of_element_located(self.RADIO_VALOR_CUOTA_INICIAL))
        self.driver.execute_script("arguments[0].click();", radio)
        self.esperar_postback()
        assert self.driver.find_element(*self.RADIO_VALOR_CUOTA_INICIAL).is_selected(), \
            "Error de Negocio: No se pudo marcar la opción 'Valor Cuota Inicial'."

        self.type_text(self.CAMPO_VALOR_CUOTA_INICIAL, valor)
        print(f"[QA Info] Valor de cuota inicial ingresado: {valor}")

    def calcular_financiacion(self):
        """Da clic en 'Cotizar financiación' de esta pantalla y espera la tabla de resultados."""
        self.click_js(self.BTN_COTIZAR_FINANCIACION)
        print("[QA Info] Clic en 'Cotizar financiación' en la pantalla de financiación.")
        self.esperar_spinner()

        try:
            WebDriverWait(self.driver, 60).until(lambda d: d.find_elements(*self.FILAS_RESULTADO))
        except TimeoutException:
            raise AssertionError("Error de Negocio: No apareció la tabla de financiación.")

    def leer_resultado(self):
        """Lee la fila de resultados y la devuelve como diccionario.

        Ejemplo: {'producto': 'Global Garantizada 360', 'prima': '142.596.000', ...,
                  'cuotas': ['8.370.225', '1.969.044', '1.671.987']}
        """
        fila = self.driver.find_elements(*self.FILAS_RESULTADO)[0]
        celdas = [c.text.strip() for c in fila.find_elements(By.XPATH, "./th|./td")]
        resultado = dict(zip(self.COLUMNAS, celdas))
        resultado["cuotas"] = celdas[len(self.COLUMNAS):]  # una por cada plazo (12, 72, 96 meses...)
        print(f"[QA Info] Resultado de financiación: {resultado}")
        return resultado
