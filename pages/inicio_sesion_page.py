import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from config import PORTAL_URL
from pages.base_page import BasePage


class LoginPage(BasePage):

    URL = PORTAL_URL

    # Locators (IDs limpios, rápidos y estables)
    BTN_CANCELAR = (By.ID, "btnCancelar")
    INPUT_USUARIO = (By.ID, "usuarioLogin")
    INPUT_PASSWORD = (By.ID, "claveLogin")
    BTN_INGRESAR = (By.ID, "btnLogin")
    BTN_MIS_COTIZACIONES = (By.XPATH, "//*[contains(@id, 'btnMisCotizaciones') or contains(@id, 'IrCotizadores')]")
    MODAL_INICIAL = (By.ID, "mpeMensajeNoCliente_backgroundElement")
    BTN_ADICION_SEMESTRE = (By.XPATH, "//*[contains(@id, 'IrAdicionSemestres') or contains(@id, 'btnAdicionSemestre')]")

    # --- Login ---

    def open(self):
        self.driver.get(self.URL)
        self.cerrar_modal_si_aparece()

    def enter_username(self, username):
        self.type_text(self.INPUT_USUARIO, username)

    def enter_password(self, password):
        self.type_text(self.INPUT_PASSWORD, password)

    def click_ingresar(self):
        # BasePage resuelve con JavaScript si el botón queda interceptado visualmente
        self.click(self.BTN_INGRESAR)

    def login(self, username, password):
        self.enter_username(username)
        self.enter_password(password)
        self.click_ingresar()

    def iniciar_sesion_limpia(self, username, password):
        """Abre el portal, limpia cookies/almacenamiento, cierra el modal inicial e inicia sesión."""
        self.open()
        try:
            self.driver.delete_all_cookies()
            self.driver.execute_script("window.localStorage.clear(); window.sessionStorage.clear();")
            self.driver.refresh()
        except Exception:
            pass

        try:
            self.cerrar_modal_si_aparece()
        except Exception:
            pass

        self.login(username, password)

    def cerrar_modal_si_aparece(self):
        """
        Intenta cerrar el modal informativo si aparece en instancias limpias.
        Si no aparece en 3 segundos, continúa con el flujo sin romper el test.
        """
        try:
            boton = WebDriverWait(self.driver, 3).until(
                EC.element_to_be_clickable(self.BTN_CANCELAR)
            )
            boton.click()
            print("\n[QA Info] Modal inicial detectado y cerrado con éxito.")
            WebDriverWait(self.driver, 3).until(
                EC.invisibility_of_element_located(self.MODAL_INICIAL)
            )
        except TimeoutException:
            print("\n[QA Info] El modal no apareció. Continuando con el login directo.")

    # --- Menú principal post-login ---

    def ir_a_modulo_cotizaciones(self):
        """Espera a que desaparezcan los modales post-login y entra al iframe operativo."""
        try:
            WebDriverWait(self.driver, 12).until(
                EC.invisibility_of_element_located(self.MODAL_INICIAL)
            )
        except TimeoutException:
            pass

        time.sleep(4)  # El servidor tarda en estabilizar la página después del login
        self.entrar_iframe_contenido()

    def validar_opciones_menu(self):
        """Verifica que los botones 'Mis Cotizaciones' y 'Adición de Semestre' estén visibles."""
        btn_cotizaciones = self.wait.until(EC.visibility_of_element_located(self.BTN_MIS_COTIZACIONES))
        assert btn_cotizaciones.is_displayed(), \
            "Error crítico: El botón de 'Mis Cotizaciones' no está visible en la interfaz."

        btn_semestres = self.wait.until(EC.visibility_of_element_located(self.BTN_ADICION_SEMESTRE))
        assert btn_semestres.is_displayed(), \
            "Error crítico: El botón de 'Adición de Semestres' no está visible en la interfaz."

        print("[QA Info] Smoke Test Exitoso: 'Mis Cotizaciones' y 'Adición de Semestres' cargaron correctamente.")

    def click_mis_cotizaciones(self):
        """Abre el flujo de búsqueda de clientes (espera larga por la lentitud del servidor)."""
        elemento = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located(self.BTN_MIS_COTIZACIONES)
        )
        try:
            WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(self.BTN_MIS_COTIZACIONES))
            elemento.click()
        except Exception:
            self.driver.execute_script("arguments[0].click();", elemento)
