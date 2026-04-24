from selenium.webdriver.common.by import By
from .base_page import BasePage

class LoginPage(BasePage):
    # Locators
    BTN_CANCELAR = (By.XPATH, "//input[@value='Cancelar']")
    INPUT_USUARIO = (By.ID, "usuarioLogin")
    INPUT_PASS = (By.ID, "claveLogin")

    def open(self):
        self.driver.get("http://10.1.2.33/PortalEM/ingreso-usuarios.aspx")

    def login_workflow(self, user, pwd):
        self.click(self.BTN_CANCELAR)
        self.type_text(self.INPUT_USUARIO, user)
        self.type_text(self.INPUT_PASS, pwd)