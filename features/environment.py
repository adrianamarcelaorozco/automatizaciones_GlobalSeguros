from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def before_all(context):
    """Se ejecuta una vez antes de toda la suite de pruebas."""
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    
    # Inicializamos el driver
    context.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    # 🔥 ESCUDO: Si la página tarda más de 15 segundos en responder (por culpa de la VPN/Red), 
    # el script romperá con un error claro en lugar de quedarse congelado eternamente.
    context.driver.set_page_load_timeout(15)

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