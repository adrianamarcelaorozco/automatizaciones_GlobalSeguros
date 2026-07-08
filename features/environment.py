from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def before_all(context):
    """Se ejecuta una vez antes de toda la suite de pruebas."""
    # Usamos WebDriver Manager para evitar problemas con la versión del chromedriver
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless") # Descomenta si quieres ejecutar en segundo plano
    options.add_argument("--start-maximized")
    
    # Inicializamos el driver y lo asignamos al contexto global
    context.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def before_scenario(context, scenario):
    """Se ejecuta antes de cada escenario individual."""
    # Navegamos a la URL base antes de empezar cada prueba
    context.driver.get("http://10.1.2.33/PortalEM/ingreso-usuarios.aspx")

def after_all(context):
    """Se ejecuta después de toda la suite de pruebas."""
    # Cerramos el navegador para liberar recursos
    if hasattr(context, 'driver'):
        context.driver.quit()

def after_scenario(context, scenario):
    """Opcional: Captura un screenshot si un escenario falla."""
    if scenario.status == "failed":
        context.driver.save_screenshot(f"fail_{scenario.name}.png")