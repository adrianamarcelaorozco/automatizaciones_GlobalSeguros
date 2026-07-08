from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage
import time
from datetime import date
import random

class CotizacionPage(BasePage):

    # ==========================================================================
    # LOCALIZADORES (CORREGIDOS)
    # ==========================================================================
    # Reemplaza tu línea actual por esta:
    TITULO_OPCIONES_COTIZACION = (By.CSS_SELECTOR, "h1.primary-title")
    BTN_GLOBAL_EDUCACION_360 = (By.XPATH, '//a[contains(.,"Global Educacion - Garantizada 360")]')
    
    # BENEFICIARIO
    SELECT_TIPO_DOCUMENTO = (By.XPATH, '//*[@id="divBeneficiario"]//input[contains(@class,"select-dropdown")]')
    INPUT_NUMERO_DOCUMENTO = (By.ID, "NroIdentificacionBen")
    INPUT_PRIMER_APELLIDO = (By.ID, "ApeBen")
    INPUT_SEGUNDO_APELLIDO = (By.ID, "ApeBen2")
    INPUT_FECHA_NACIMIENTO = (By.ID, "FecNacimientoBen")
    INPUT_EDAD = (By.ID, "EdadBen")
    RADIO_MASCULINO = (By.ID, "GeneroMBen")
    RADIO_FEMENINO = (By.ID, "GeneroFBen")
    
    # COLEGIO (Corregidos de ID a XPATH donde correspondía)
    SELECT_DEPARTAMENTO = (By.XPATH, "//select[@id='Departamento']/preceding-sibling::input")
    SELECT_MUNICIPIO = (By.XPATH, "//select[@id='MunicipioColegio']/preceding-sibling::input")
    SELECT_INSTITUCION = (By.ID, "ColegioSeleccionado") # ID correcto
    
    # COTIZACIÓN
    SELECT_APOYO_INSTITUCIONAL = (By.ID, "ID_APOYO_INSTITUCIONAL")
    SELECT_EVENTO = (By.ID, "ID_EVENTO")
    BTN_COTIZAR = (By.ID, "ID_BOTON_COTIZAR")
    MENSAJE_RESULTADO = (By.CSS_SELECTOR, ".clase-de-resultado-final")

    def __init__(self, driver):
        super().__init__(driver)
        self.wait = WebDriverWait(driver, 20)

    # ==========================================================================
    # MÉTODOS DE NAVEGACIÓN Y ACCIÓN
    # ==========================================================================

    def scroll_hasta_opciones_cotizacion(self):
        self.scroll_to(self.TITULO_OPCIONES_COTIZACION)
        time.sleep(1)

    def seleccionar_global_educacion_360(self):
        """Usa JS para forzar el clic y saltar bloqueos visuales."""
        boton = self.wait.until(EC.presence_of_element_located(self.BTN_GLOBAL_EDUCACION_360))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", boton)
        time.sleep(0.5) # Breve pausa para estabilización post-scroll
        try:
            boton.click()
        except Exception:
            self.driver.execute_script("arguments[0].click();", boton)

    def cambiar_a_ventana_cotizador(self):
        ventana_actual = self.driver.current_window_handle
        self.wait.until(lambda d: len(d.window_handles) > 1)
        for ventana in self.driver.window_handles:
            if ventana != ventana_actual:
                self.driver.switch_to.window(ventana)
                break

    def validar_pantalla_cotizador(self):
        # Asegúrate de que el título sea visible. Cambia el locator según tu necesidad.
        self.wait.until(EC.visibility_of_element_located((By.TAG_NAME, "h1")))

    def diligenciar_flujo_cotizacion(self):
        datos = self.generar_beneficiario_random()
        
        self.select_custom_dropdown(self.SELECT_TIPO_DOCUMENTO, datos["tipo_documento"])
        self.fill_field(self.INPUT_NUMERO_DOCUMENTO, datos["numero_documento"])
        self.fill_field(self.INPUT_PRIMER_APELLIDO, datos["apellido1"])
        self.fill_field(self.INPUT_SEGUNDO_APELLIDO, datos["apellido2"])
        self.fill_field(self.INPUT_FECHA_NACIMIENTO, datos["fecha"])
        self.fill_field(self.INPUT_EDAD, str(datos["edad"]))
        self.seleccionar_sexo(datos["sexo"])
        
        self.seleccionar_apoyo_institucional()
        self.seleccionar_evento()
        self.clic_boton_cotizar()

    # MÉTODOS DE SOPORTE
    def seleccionar_sexo(self, sexo):
        locator = self.RADIO_MASCULINO if sexo == "M" else self.RADIO_FEMENINO
        self.click(locator)

    def seleccionar_apoyo_institucional(self):
        # Si el elemento tiene ID, no necesita XPath
        self._select_dropdown_by_index(self.SELECT_APOYO_INSTITUCIONAL, 1)

    def seleccionar_evento(self):
        self._select_dropdown_by_index(self.SELECT_EVENTO, 1)

    def _select_dropdown_by_index(self, locator, index):
        element = self.wait.until(EC.element_to_be_clickable(locator))
        Select(element).select_by_index(index)

    def clic_boton_cotizar(self):
        btn = self.scroll_to(self.BTN_COTIZAR)
        self.click(self.BTN_COTIZAR)

    def obtener_resultado_cotizacion(self):
        return self.wait.until(EC.visibility_of_element_located(self.MENSAJE_RESULTADO)).text

    def generar_beneficiario_random(self):
        apellidos = ["Gomez", "Perez", "Rodriguez", "Lopez", "Martinez", "Cardona", "Restrepo", "Gaviria"]
        tipo = random.choice(["Registro Civil", "Tarjeta de Identidad"])
        edad = random.randint(1, 6) if tipo == "Registro Civil" else random.randint(7, 17)
        año = date.today().year - edad
        return {
            "tipo_documento": tipo,
            "numero_documento": str(random.randint(10000000, 99999999)),
            "apellido1": random.choice(apellidos),
            "apellido2": random.choice(apellidos),
            "sexo": random.choice(["M", "F"]),
            "edad": edad,
            "fecha": f"{random.randint(1,28):02d}/{random.randint(1,12):02d}/{año}"
        }