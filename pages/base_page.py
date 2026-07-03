from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    def click(self, locator):
        """Espera a que el elemento sea clicleable y realiza el clic. 
        Si falla por intercepción visual, intenta mediante JavaScript."""
        element = self.wait.until(EC.element_to_be_clickable(locator))
        try:
            element.click()
        except Exception:
            self.driver.execute_script("arguments[0].click();", element)
        return element

    def type_text(self, locator, text):
        """Espera la visibilidad del elemento, limpia su contenido y escribe el texto."""
        element = self.wait.until(EC.visibility_of_element_located(locator))
        element.clear()
        element.send_keys(text)
        return element # Retornamos el elemento por si necesitas usar execute_script("arguments[0].blur();", element)