from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def before_all(context):
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    # Cambiamos la estrategia de carga a 'eager'. 
    # Esto le dice a Selenium: "Continúa en cuanto el DOM esté interactivo, no esperes a que bajen todas las imágenes/scripts".
    options.page_load_strategy = 'eager' 
    
    context.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def before_scenario(context, scenario):
    """Se ejecuta antes de cada escenario individual."""
    try:
        print("[QA Info] Intentando conectar al portal de Global Seguros...")
        context.driver.get("http://10.1.2.33/PortalEM/ingreso-usuarios.aspx")
    except Exception as e:
        print(f"\n❌ [ERROR DE RED] No se pudo cargar el portal. Verifica que la VPN esté conectada.")
        raise e

def after_all(context):
    """Se ejecuta después de toda la suite de pruebas."""
    if hasattr(context, 'driver'):
        context.driver.quit()

def after_scenario(context, scenario):
    """Captura un screenshot si un escenario falla."""
    if scenario.status == "failed" and hasattr(context, 'driver'):
        try:
            context.driver.save_screenshot(f"fail_{scenario.name}.png")
        except Exception:
            pass

