from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.login_page import LoginPage


def test_ingresar_a_mis_cotizaciones(driver):
    login = LoginPage(driver)
    login.open()
    login.login("NCRUZV", "Clave123")

    # Entrar al iframe
    WebDriverWait(driver, 20).until(
        EC.frame_to_be_available_and_switch_to_it((By.ID, "contenido"))
    )
    
    # ✅ CORREGIDO: Cambiado self.driver por driver
    WebDriverWait(driver, 10).until(
        EC.invisibility_of_element_located((By.ID, "mpeMensajeNoCliente_backgroundElement"))
    )
    
    # Clic en Mis cotizaciones
    boton = WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable((By.XPATH, "//*[contains(@id, 'btnMisCotizaciones') or contains(@id, 'IrCotizadores')]"))
    )

    boton.click()

    print("Click en Mis cotizaciones realizado")