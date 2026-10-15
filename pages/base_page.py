import time
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

    def click_js(self, locator, timeout=15):
        """Espera la presencia del elemento, lo centra en pantalla y hace clic vía JavaScript.
        Útil en los modales ASP.NET donde el clic normal queda interceptado."""
        element = WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located(locator))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        self.driver.execute_script("arguments[0].click();", element)
        return element

    def esperar_postback(self, timeout=30):
        """Espera a que el portal termine de ir al servidor (PostBack/AJAX de ASP.NET o jQuery).
        Si la página no usa esas librerías, simplemente continúa."""
        time.sleep(0.5)  # Da tiempo a que la petición arranque
        script = """
            var asp = (typeof Sys !== 'undefined' && Sys.WebForms && Sys.WebForms.PageRequestManager)
                ? Sys.WebForms.PageRequestManager.getInstance().get_isInAsyncPostBack() : false;
            var jq = (typeof jQuery !== 'undefined') ? jQuery.active > 0 : false;
            return document.readyState === 'complete' && !asp && !jq;
        """
        try:
            WebDriverWait(self.driver, timeout).until(lambda d: d.execute_script(script))
        except Exception:
            print("[QA Info] El servidor sigue procesando; se continúa con el flujo.")

    SPINNER_CARGANDO = (By.ID, "UpdateProgress1")

    def esperar_spinner(self, timeout=60):
        """Espera a que desaparezca el spinner azul de 'cargando' (UpdateProgress1) del portal.
        Si el spinner no existe en la pantalla actual, continúa de inmediato."""
        time.sleep(0.5)  # Da tiempo a que el spinner alcance a aparecer
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.invisibility_of_element_located(self.SPINNER_CARGANDO)
            )
        except Exception:
            print("[QA Info] El spinner de carga sigue visible; se continúa con el flujo.")

    def entrar_iframe_contenido(self, timeout=15):
        """Vuelve al documento principal y entra al iframe 'contenido' donde se renderizan los módulos."""
        self.driver.switch_to.default_content()
        WebDriverWait(self.driver, timeout).until(
            EC.frame_to_be_available_and_switch_to_it((By.ID, "contenido"))
        )

    def scroll_to(self, locator):
        """Desplaza la vista hacia el elemento para evitar errores de ClickIntercepted."""
        element = self.wait.until(EC.presence_of_element_located(locator))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        return element
    
    def interactuar_con_beneficiario(self, campo_locator, valor):
        # Scroll hacia el elemento
        elemento = self.driver.find_element(*campo_locator)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", elemento)
        
        # Esperar visibilidad y enviar datos
        self.wait.until(EC.element_to_be_clickable(campo_locator)).send_keys(valor)