import time
import random
from enum import Enum
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TipoDocumento(Enum):
    CIUDADANIA = ("CEDULA DE CIUDADANIA", "CEDULA DE CIUDADANIA")
    EXTRANJERIA = ("CEDULA DE EXTRANJERIA", "CEDULA DE EXTRANJERIA")
    PROTECCION_TEMPORAL = ("PERMISO PROTECCION TEMPORAL", "PERMISO DE PROTECCIÓN TEMPORAL")

class BusquedaClientePage:
    def __init__(self, driver):
        self.driver = driver
        
        # LOCALIZADORES PANTALLA 1 (BÚSQUEDA)
        self.SELECT_DOCUMENTO_DESPLEGABLE = (By.XPATH, "//select[@id='ListaDocumentos']/preceding-sibling::input[@class='select-dropdown']")
        self.CAMPO_NUMERO_DOCUMENTO = (By.ID, "NdocClient")
        self.BOTON_BUSCAR = (By.CSS_SELECTOR, "input[id*='BuscarCliente'], #BuscarCliente, button[id*='Buscar']")
        self.BOTON_NUEVO_CLIENTE = (By.CSS_SELECTOR, ".btn.green, input[id*='NuevoCliente'], button[id*='Nuevo']")

        # LOCALIZADORES PANTALLA 2 (FORMULARIO REGISTRO)
        self.FORM_SELECT_DOCUMENTO = (By.XPATH, "//select[@id='TipoIdentificacion']/preceding-sibling::input[@class='select-dropdown']")
        self.FORM_NUMERO_DOCUMENTO = (By.ID, "NroIdentificacion")
        self.FORM_NOMBRES = (By.ID, "NomTom")
        self.FORM_APELLIDO1 = (By.ID, "ApeTom")
        self.FORM_APELLIDO2 = (By.ID, "ApeTom2")
        self.FORM_FECHA_NACIMIENTO = (By.ID, "FecNacimientoTom")
        self.FORM_EDAD = (By.ID, "EdadTomador")
        
        # Radios de Sexo
        self.RADIO_MASCULINO = (By.ID, "GeneroMTomador")
        self.RADIO_FEMENINO = (By.ID, "GeneroFTomador")
        
        # Datos de contacto y geografía
        self.CAMPO_CORREO = (By.ID, "CorreoCliente")
        self.CAMPO_CELULAR = (By.ID, "Celular")
        self.SELECT_DEPARTAMENTO = (By.XPATH, "//select[@id='Departamento']/preceding-sibling::input[@class='select-dropdown']")
        self.SELECT_CIUDAD = (By.XPATH, "//select[@id='Ciudad']/preceding-sibling::input[@class='select-dropdown']")
        self.BOTON_GRABAR = (By.ID, "GrabaPersona")

        # POPUP DE ÉXITO
        self.TEXTO_ALERTA_EXITO = (By.XPATH, "//div[contains(@class, 'alert') and contains(@class, 'informacion')]//span")
        self.BOTON_ACEPTAR_ALERTA = (By.ID, "CierraMensajeInformativo")

    def ingresar_y_buscar_cliente(self, numero_documento: str, tipo_documento: TipoDocumento):
        """Selecciona el tipo de documento en la pantalla inicial de búsqueda."""
        dropdown = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable(self.SELECT_DOCUMENTO_DESPLEGABLE))
        dropdown.click()
        
        texto_busqueda = tipo_documento.value[0]
        xpath_opcion = f"//ul[contains(@class, 'dropdown-content')]//span[text()='{texto_busqueda}']"
        opcion_li = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath_opcion)))
        opcion_li.click()
        time.sleep(0.5)

        campo_numero = WebDriverWait(self.driver, 15).until(EC.visibility_of_element_located(self.CAMPO_NUMERO_DOCUMENTO))
        campo_numero.clear()
        campo_numero.send_keys(numero_documento)

        boton_buscar = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable(self.BOTON_BUSCAR))
        try:
            boton_buscar.click()
        except Exception:
            self.driver.execute_script("arguments[0].click();", boton_buscar)
        print(f"[QA Info] Búsqueda ejecutada para: {tipo_documento.name} - {numero_documento}")
        time.sleep(1.5)

    def click_nuevo_cliente(self):
        """Avanza al formulario de creación."""
        boton_nuevo = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable(self.BOTON_NUEVO_CLIENTE))
        try:
            boton_nuevo.click()
        except Exception:
            self.driver.execute_script("arguments[0].click();", boton_nuevo)
        print("[QA Info] Clic en botón 'Nuevo Cliente' ejecutado.")
        time.sleep(2.0)

    def completar_datos_personales(self, numero_documento: str, tipo_documento: TipoDocumento, correo: str, celular: str, departamento: str, ciudad: str):
        """Diligencia el formulario de registro adaptando los datos inyectados mediante JS."""
        
        # BANCO DE DATOS ALEATORIOS COHERENTES
        apellidos = ["Gomez", "Rodriguez", "Perez", "Martinez", "Lopez", "Zapata", "Gaviria", "Restrepo", "Cardona"]
        nombres_m = ["Carlos", "Juan", "Andres", "Mateo", "Luis", "Santiago", "Diego", "Alejandro"]
        nombres_f = ["Diana", "Camila", "Valeria", "Sofia", "Maria", "Laura", "Natalia", "Paula"]
        
        sexo = random.choice(["M", "F"])
        nombre_aleatorio = random.choice(nombres_m) if sexo == "M" else random.choice(nombres_f)
        apellido1_aleatorio = random.choice(apellidos)
        apellido2_aleatorio = random.choice(apellidos)
        
        año_nacimiento = random.randint(1975, 2005)
        mes_nacimiento = random.randint(1, 12)
        dia_nacimiento = random.randint(1, 28)
        fecha_str = f"{dia_nacimiento:02d}/{mes_nacimiento:02d}/{año_nacimiento}"
        edad_calculada = 2026 - año_nacimiento

        print(f"[QA Info] Formulario: Perfil {sexo} nacido en {año_nacimiento} ({edad_calculada} años).")

        # 1. Seleccionar Tipo de Documento en Formulario de Registro
        drop_form_doc = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable(self.FORM_SELECT_DOCUMENTO))
        drop_form_doc.click()
        time.sleep(0.5)
        
        texto_registro = tipo_documento.value[1]
        # Corrección: Asegura buscar la opción dentro del ul hermano del select de TipoIdentificacion
        opcion_form_li = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//select[@id='TipoIdentificacion']/preceding-sibling::ul[contains(@class, 'dropdown-content')]//span[text()='{texto_registro}']"))
        )
        opcion_form_li.click()
        time.sleep(0.5)

        # 2. Ingresar el mismo Número de Documento
        campo_form_num = WebDriverWait(self.driver, 15).until(EC.presence_of_element_located(self.FORM_NUMERO_DOCUMENTO))
        campo_form_num.clear()
        campo_form_num.send_keys(numero_documento)
        self.driver.execute_script("arguments[0].blur();", campo_form_num)
        time.sleep(1.0)

        # 3. Forzar desbloqueo y llenado de datos de identidad (Campos deshabilitados de ASPX)
        input_nombres = self.driver.find_element(*self.FORM_NOMBRES)
        input_ape1 = self.driver.find_element(*self.FORM_APELLIDO1)
        input_ape2 = self.driver.find_element(*self.FORM_APELLIDO2)
        input_fecha = self.driver.find_element(*self.FORM_FECHA_NACIMIENTO)
        input_edad = self.driver.find_element(*self.FORM_EDAD)
        
        self.driver.execute_script("arguments[0].removeAttribute('disabled'); arguments[0].value = arguments[1];", input_nombres, nombre_aleatorio)
        self.driver.execute_script("arguments[0].removeAttribute('disabled'); arguments[0].value = arguments[1];", input_ape1, apellido1_aleatorio)
        self.driver.execute_script("arguments[0].removeAttribute('disabled'); arguments[0].value = arguments[1];", input_ape2, apellido2_aleatorio)
        self.driver.execute_script("arguments[0].removeAttribute('disabled'); arguments[0].value = arguments[1];", input_fecha, fecha_str)
        self.driver.execute_script("arguments[0].removeAttribute('disabled'); arguments[0].value = arguments[1];", input_edad, str(edad_calculada))

        # 4. Desbloqueo y selección de Radio Button de Sexo
        locator_sexo = self.RADIO_MASCULINO if sexo == "M" else self.RADIO_FEMENINO
        radio_sexo_elem = self.driver.find_element(*locator_sexo)
        self.driver.execute_script("arguments[0].removeAttribute('disabled'); arguments[0].click();", radio_sexo_elem)

        # 5. Llenar Correo Electrónico y Celular
        campo_correo = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.CAMPO_CORREO))
        campo_correo.clear()
        campo_correo.send_keys(correo)

        campo_celular = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.CAMPO_CELULAR))
        campo_celular.clear()
        campo_celular.send_keys(celular)

        # 6. Seleccionar Departamento
        drop_dep = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.SELECT_DEPARTAMENTO))
        drop_dep.click()
        time.sleep(0.5)
        # Corrección: Apunta al ul específico del select de Departamento
        opcion_dep = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//select[@id='Departamento']/preceding-sibling::ul[contains(@class, 'dropdown-content')]//span[text()='{departamento.upper()}']"))
        )
        opcion_dep.click()
        
        print("[QA Info] Esperando recarga de ciudades (PostBack)...")
        time.sleep(3.0)

        # 7. Seleccionar Ciudad
        drop_ciu = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.SELECT_CIUDAD))
        drop_ciu.click()
        time.sleep(0.5)
        # SOLUCIÓN CRÍTICA: Apunta estrictamente al ul hermano del select de Ciudad (#Ciudad) para evitar colisiones visuales
        opcion_ciu = WebDriverWait(self.driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, f"//select[@id='Ciudad']/preceding-sibling::ul[contains(@class, 'dropdown-content')]//span[text()='{ciudad.upper()}']"))
        )
        opcion_ciu.click()
        time.sleep(0.5)

        # 8. Guardar Formulario
        btn_grabar = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.BOTON_GRABAR))
        try:
            btn_grabar.click()
        except Exception:
            self.driver.execute_script("arguments[0].click();", btn_grabar)
            
        print(f"[QA Info] Registro enviado para {nombre_aleatorio} {apellido1_aleatorio}.")

    def obtener_mensaje_exito_y_cerrar(self) -> str:
        """Valida visualmente el mensaje de confirmación y cierra la alerta."""
        elemento_texto = WebDriverWait(self.driver, 15).until(
            EC.visibility_of_element_located(self.TEXTO_ALERTA_EXITO)
        )
        texto_alerta = elemento_texto.text.strip()
        
        boton_aceptar = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.BOTON_ACEPTAR_ALERTA))
        try:
            boton_aceptar.click()
        except Exception:
            self.driver.execute_script("arguments[0].click();", boton_aceptar)
            
        return texto_alerta