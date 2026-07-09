import random
import time
from enum import Enum
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage

class TipoDocumento(Enum):
    CIUDADANIA = ("CEDULA DE CIUDADANIA", "CEDULA DE CIUDADANIA")
    EXTRANJERIA = ("CEDULA DE EXTRANJERIA", "CEDULA DE EXTRANJERIA")
    PROTECCION_TEMPORAL = ("PERMISO PROTECCION TEMPORAL", "PERMISO DE PROTECCIÓN TEMPORAL")

class BusquedaClientePage(BasePage):
    def __init__(self, driver):
        # Heredamos el inicializador y el self.wait (de 15 segundos) de BasePage
        super().__init__(driver)
        
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
        # OPTIMIZACIÓN: Usamos el método click centralizado de BasePage
        self.click(self.SELECT_DOCUMENTO_DESPLEGABLE)
        
        texto_busqueda = tipo_documento.value[0]
        xpath_opcion = f"//ul[contains(@class, 'dropdown-content')]//span[text()='{texto_busqueda}']"
        opcion_li = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath_opcion)))
        opcion_li.click()
        time.sleep(0.5)

        # OPTIMIZACIÓN: Usamos el método type_text de BasePage
        self.type_text(self.CAMPO_NUMERO_DOCUMENTO, numero_documento)

        boton_buscar = self.wait.until(EC.element_to_be_clickable(self.BOTON_BUSCAR))
        try:
            boton_buscar.click()
        except Exception:
            self.driver.execute_script("arguments[0].click();", boton_buscar)
        print(f"[QA Info] Búsqueda ejecutada para: {tipo_documento.name} - {numero_documento}")
        time.sleep(1.5)

    def click_nuevo_cliente(self):
        """Avanza al formulario de creación."""
        # OPTIMIZACIÓN: Delegamos el clic dinámico (normal o JS) a la BasePage
        self.click(self.BOTON_NUEVO_CLIENTE)
        print("[QA Info] Clic en botón 'Nuevo Cliente' ejecutado.")
        time.sleep(2.0)

    def completar_datos_personales(self, numero_documento: str, tipo_documento: TipoDocumento, correo: str, celular: str, departamento: str, ciudad: str):
        """Diligencia el formulario de registro adaptando los datos inyectados mediante JS."""
        
        # BANCO DE DATOS ALEATORIOS COHERENTES (Se mantiene intacto)
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
        
        departamentos_colombia = [
            "AMAZONAS", "ANTIOQUIA", "ARAUCA", "ATLANTICO", "BOLIVAR", "BOYACA", 
            "CALDAS", "CAQUETA", "CASANARE", "CAUCA", "CESAR", "CHOCO", "CORDOBA", 
            "CUNDINAMARCA", "LA GUAJIRA", "GUAINIA", "GUAVIARE", "HUILA", "MAGDALENA", 
            "META", "NARIÐO", "NORTE DE SANTANDER", "PUTUMAYO", "QUINDIO", "RISARALDA", 
            "SAN ANDRES", "SANTANDER", "SUCRE", "TOLIMA", "VALLE DEL CAUCA", "VAUPES", 
            "VICHADA", "DISTRITO CAPITAL"
        ]

        # 1. Seleccionar Tipo de Documento en Formulario de Registro
        self.click(self.FORM_SELECT_DOCUMENTO)
        time.sleep(0.5)
        
        texto_registro = tipo_documento.value[1]
        opcion_form_li = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//select[@id='TipoIdentificacion']/preceding-sibling::ul[contains(@class, 'dropdown-content')]//span[text()='{texto_registro}']"))
        )
        opcion_form_li.click()
        time.sleep(0.5)

        # 2. Ingresar el mismo Número de Documento
        self.type_text(self.FORM_NUMERO_DOCUMENTO, numero_documento)
        campo_form_num = self.driver.find_element(*self.FORM_NUMERO_DOCUMENTO)
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
        self.type_text(self.CAMPO_CORREO, correo)
        self.type_text(self.CAMPO_CELULAR, celular)

        # 6. Definición del Departamento final
        if departamento == "ALEATORIO":
            departamento_final = random.choice(departamentos_colombia)
        else:
            departamento_final = departamento

        # OPTIMIZACIÓN: Eliminamos las variables duplicadas 'nombre_random' y 'apellido_random' que reescribían la lógica
        print(f"[QA Info] Registro Dinámico: {nombre_aleatorio} {apellido1_aleatorio} en {departamento_final}")

        # Seleccionar Departamento
        self.click(self.SELECT_DEPARTAMENTO)
        time.sleep(0.5)
        
        opcion_dep = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//select[@id='Departamento']/preceding-sibling::ul[contains(@class, 'dropdown-content')]//span[text()='{departamento_final.upper()}']"))
        )
        opcion_dep.click()
        
        print("[QA Info] Esperando recarga de ciudades (PostBack)...")
        time.sleep(4.0)

        # 7. Seleccionar Ciudad
        self.click(self.SELECT_CIUDAD)
        time.sleep(0.5)
        
        opciones_ciu = self.driver.find_elements(By.XPATH, "//select[@id='Ciudad']/preceding-sibling::ul[contains(@class, 'dropdown-content')]//span")
        
        if len(opciones_ciu) > 1:
            opcion_ciu = opciones_ciu[1] # Selecciona la segunda opción real
            print(f"[QA Info] Seleccionando segunda ciudad disponible: {opcion_ciu.text}")
        else:
            opcion_ciu = opciones_ciu[0]
            print(f"[QA Info] Seleccionando única ciudad disponible: {opcion_ciu.text}")
        
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(opcion_ciu))
        opcion_ciu.click()
        time.sleep(0.5)

        # 8. Guardar Formulario
        # OPTIMIZACIÓN: Delegamos el clic robusto a la BasePage
        self.click(self.BOTON_GRABAR)
        print(f"[QA Info] Registro enviado para {nombre_aleatorio} {apellido1_aleatorio}.")

    def obtener_mensaje_exito_y_cerrar(self) -> str:
        # Aumentamos el tiempo de espera específicamente para esta confirmación
        # y usamos 'presence_of_element_located' en lugar de 'visibility' para evitar 
        # problemas con elementos que cambian de estilo durante el postback.
        wait_custom = WebDriverWait(self.driver, 50)
        elemento_texto = wait_custom.until(EC.presence_of_element_located(self.TEXTO_ALERTA_EXITO))
        
        texto_alerta = elemento_texto.text.strip()
        
        # Aseguramos que el botón de cerrar sea cliqueable antes de proceder
        boton_cerrar = wait_custom.until(EC.element_to_be_clickable(self.BOTON_ACEPTAR_ALERTA))
        boton_cerrar.click()
        
        return texto_alerta