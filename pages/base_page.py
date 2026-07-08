from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

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
        return element 

    # --- MÉTODOS AÑADIDOS PARA ESTABILIDAD SENIOR ---

    def fill_field(self, locator, text):
        """Versión robusta de type_text que también maneja campos deshabilitados."""
        try:
            return self.type_text(locator, text)
        except Exception:
            # Si falla por estar bloqueado (disabled), lo desbloqueamos vía JS
            element = self.wait.until(EC.presence_of_element_located(locator))
            self.driver.execute_script(
                "arguments[0].removeAttribute('disabled'); arguments[0].value = arguments[1];", 
                element, text
            )
            return element

    def select_custom_dropdown(self, trigger_locator, option_text):
        """Maneja dropdowns complejos (Materialize/ASPX) que usan inputs como disparadores."""
        # 1. Clic en el disparador (el input falso)
        self.click(trigger_locator)
        
        # 2. Construcción dinámica del XPath para la opción en la lista desplegable
        # Se asume que el contenedor es un ul.dropdown-content común en estos sistemas
        option_xpath = f"//ul[contains(@class, 'dropdown-content')]//span[contains(text(), '{option_text}')]"
        
        # 3. Espera a que la opción sea visible y clicleable
        option = self.wait.until(EC.element_to_be_clickable((By.XPATH, option_xpath)))
        option.click()
        return option

    def scroll_to(self, locator):
        """Desplaza la vista hacia el elemento para evitar errores de ClickIntercepted."""
        element = self.wait.until(EC.presence_of_element_located(locator))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        return element