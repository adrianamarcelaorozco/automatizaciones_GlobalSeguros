from selenium.webdriver.common.by import By
from .base_page import BasePage


class LoginPage(BasePage):

    URL = "http://10.1.2.33/PortalEM/ingreso-usuarios.aspx"

    # Locators
    BTN_CANCELAR = (By.XPATH, "//input[@value='Cancelar']")
    INPUT_USUARIO = (By.ID, "usuarioLogin")
    INPUT_PASSWORD = (By.ID, "claveLogin")
    BTN_INGRESAR = (By.ID, "btnLogin")
    BTN_MIS_COTIZACIONES = (By.ID, "IrCotizadores")

    def open(self):
        self.driver.get(self.URL)

    def click_cancelar(self):
        self.click(self.BTN_CANCELAR)

    def enter_username(self, username):
        self.type_text(self.INPUT_USUARIO, username)

    def enter_password(self, password):
        self.type_text(self.INPUT_PASSWORD, password)

    def click_ingresar(self):
        self.click(self.BTN_INGRESAR)

    def click_mis_cotizaciones(self):
        self.click(self.BTN_MIS_COTIZACIONES)

    def login(self, username, password):
        self.click_cancelar()
        self.enter_username(username)
        self.enter_password(password)
        self.click_ingresar()