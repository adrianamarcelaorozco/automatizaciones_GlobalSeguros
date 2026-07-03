from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from .base_page import BasePage


class LoginPage(BasePage):

    URL = "http://10.1.2.33/PortalEM/ingreso-usuarios.aspx"

    # Locators (IDs limpios, rápidos y estables)
    BTN_CANCELAR = (By.ID, "btnCancelar")
    INPUT_USUARIO = (By.ID, "usuarioLogin")
    INPUT_PASSWORD = (By.ID, "claveLogin")
    BTN_INGRESAR = (By.ID, "btnLogin")
    BTN_MIS_COTIZACIONES = (By.XPATH, "//*[contains(@id, 'btnMisCotizaciones') or contains(@id, 'IrCotizadores')]")    
    MODAL_INICIAL = (By.ID, "mpeMensajeNoCliente_backgroundElement")
    BTN_ADICION_SEMESTRE = (By.XPATH, "//*[contains(@id, 'IrAdicionSemestres') or contains(@id, 'btnAdicionSemestre')]")

    def open(self):
        self.driver.get(self.URL)
        self.cerrar_modal_si_aparece()

    def enter_username(self, username):
        self.type_text(self.INPUT_USUARIO, username)

    def enter_password(self, password):
        self.type_text(self.INPUT_PASSWORD, password)

    def click_ingresar(self):
        # OPTIMIZACIÓN: Delegamos el clic a BasePage. Si por alguna razón el botón
        # se intercepta visualmente, nuestro BasePage lo resolverá usando JavaScript automáticamente.
        self.click(self.BTN_INGRESAR)

    def click_mis_cotizaciones(self):
        self.click(self.BTN_MIS_COTIZACIONES)

    def login(self, username, password):
        self.enter_username(username)
        self.enter_password(password)
        self.click_ingresar()

    def cerrar_modal_si_aparece(self):
        """
        Intenta cerrar el modal informativo si aparece en instancias limpias.
        Si no aparece en 3 segundos, continúa con el flujo sin romper el test.
        """
        try:
            # Espera corta de 3 segundos exclusiva para verificar el modal
            boton = WebDriverWait(self.driver, 3).until(
                EC.element_to_be_clickable(self.BTN_CANCELAR)
            )
            boton.click()
            print("\n[QA Info] Modal inicial detectado y cerrado con éxito.")
            
            # Esperamos a que el fondo gris desaparezca por completo de la pantalla
            WebDriverWait(self.driver, 3).until(
                EC.invisibility_of_element_located(self.MODAL_INICIAL)
            )
        except TimeoutException:
            print("\n[QA Info] El modal no apareció. Continuando con el login directo.")