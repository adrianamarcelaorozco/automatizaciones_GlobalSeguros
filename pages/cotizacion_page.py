from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage
import time
import random # Asegúrate de que esto esté al inicio del archivo si no lo tenías
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select


class CotizacionPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.BTN_COTIZAR = (By.ID, "btnCotizar")
    
    def obtener_resultado_cotizacion(self):
        """
        Espera a que aparezca el resultado de la cotización y devuelve el texto.
        Ajusta el ID según lo que aparezca en tu debug_boton_cotizar.html
        """
        print("[QA Info] Esperando a que el sistema muestre el número de cotización...")
        
        # Intentamos buscar el mensaje de éxito o el número de cotización
        # Ajusta este locator si el ID es diferente (ej. lblNumeroCotizacion)
        locator_resultado = (By.XPATH, "//*[contains(text(), 'Cotización') or contains(@id, 'NumeroCotizacion')]")
        
        try:
            # Esperamos hasta 20 segundos a que la pantalla final cargue
            wait_largo = WebDriverWait(self.driver, 20)
            elemento = wait_largo.until(EC.visibility_of_element_located(locator_resultado))
            print(f"[QA Info] ¡Cotización generada! Resultado: {elemento.text}")
            return elemento.text
        except Exception:
            print("[QA Error] No se pudo encontrar el mensaje de confirmación de cotización.")
            return None
        
    def diligenciar_datos_aleatorios_beneficiario(self):
        """
        Llena el formulario usando una técnica de inyección segura que evita 
        que los campos se limpien al perder el foco.
        """
        import random
        print("[QA Info] Generando y llenando datos mediante JS (Modo Persistente)...")
        
        datos = {
            "NroIdentificacionBen": str(random.randint(100000000, 9999999999)),
            "NomBen": random.choice(["Mateo", "Valeria", "Santiago", "Camila"]),
            "ApeBen": random.choice(["Garcia", "Restrepo", "Cardona"]),
            "ApeBen2": random.choice(["Gaviria", "Zapata", "Orozco"]),
            "FecNacimientoBen": "09/09/2017"
        }
        
        # Inyectamos valores uno a uno sin disparar eventos destructivos inmediatamente
        for id_campo, valor in datos.items():
            script = f"""
                var el = document.getElementById('{id_campo}');
                if (el) {{
                    el.value = '{valor}';
                    // Solo inyectamos el valor. 
                    // No disparamos 'blur' aún, esto evita que el ASP.NET valide y borre
                }}
            """
            self.driver.execute_script(script)
        
        # Una vez llenos todos, disparamos los eventos globales para 'engañar' al sistema
        # de una sola vez
        script_eventos = """
            var campos = ['NroIdentificacionBen', 'NomBen', 'ApeBen', 'ApeBen2', 'FecNacimientoBen'];
            campos.forEach(function(id) {
                var el = document.getElementById(id);
                if (el) {
                    el.dispatchEvent(new Event('input', { bubbles: true }));
                    el.dispatchEvent(new Event('change', { bubbles: true }));
                }
            });
        """
        self.driver.execute_script(script_eventos)
        
        # Sexo y edad
        self.driver.execute_script("document.getElementById('GeneroFBenef').click();")
        self.driver.execute_script("if(typeof CalcularEdadBen === 'function') CalcularEdadBen();")
        
        print("[QA Info] Beneficiario llenado con éxito y eventos sincronizados.")

    def seleccionar_por_valor(self, select_id, valor_opcion):
        print(f"[QA Info] Forzando valor '{valor_opcion}' en el select '{select_id}'...")
        
        # En lugar de inyectar __doPostBack, vamos a usar un enfoque más limpio
        # que dispara el evento change estándar, que suele ser suficiente para ASP.NET
        script = f"""
            var select = document.getElementById('{select_id}');
            if (select) {{
                select.value = '{valor_opcion}';
                // Disparar eventos estándar
                var event = new Event('change', {{ bubbles: true }});
                select.dispatchEvent(event);
                return true;
            }}
            return false;
        """
        
        try:
            exito = self.driver.execute_script(script)
            if exito:
                # Damos un tiempo razonable para que el servidor procese el cambio
                time.sleep(3) 
            else:
                print(f"[QA Error] No se pudo encontrar el elemento {select_id} mediante JS.")
        except Exception as e:
            print(f"[QA Error] Error al ejecutar script: {str(e)}")

    def diligenciar_datos_colegio(self, depto_text, institucion_nombre, curso_val):
        # 0. ASEGURAR VISIBILIDAD (Esto evita el error de ElementNotInteractable)
        contenedor = self.driver.find_element(By.ID, "divColegio")
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", contenedor)
        time.sleep(1)

        # 1. Llenar Departamento
        self.driver.execute_script(f"document.getElementById('DeptoColegio').value = '34';")
        self.driver.execute_script("document.getElementById('DeptoColegio').dispatchEvent(new Event('change'));")
        time.sleep(2)

        # 2. Escribir colegio y buscar
        campo_inst = self.driver.find_element(By.ID, "ColegioSeleccionado")
        campo_inst.clear()
        campo_inst.send_keys(institucion_nombre)
        
        btn_buscar = self.driver.find_element(By.NAME, "AbreBusquedaColegio")
        # Forzamos scroll al botón antes de clickear
        self.driver.execute_script("arguments[0].scrollIntoView(true);", btn_buscar)
        self.driver.execute_script("arguments[0].click();", btn_buscar)
        
        # 3. INTERACCIÓN CON EL MODAL (Si aparece)
        print("[QA Info] Buscando en tabla de resultados...")
        time.sleep(4) 
        
        # Intentamos hacer clic en el nombre del colegio dentro de la tabla
        # Usamos un selector que busca el texto exacto en el enlace
        xpath_colegio = f"//table[@id='grdColegios']//a[normalize-space(text())='{institucion_nombre}']"
        try:
            link_colegio = self.driver.find_element(By.XPATH, xpath_colegio)
            self.driver.execute_script("arguments[0].click();", link_colegio)
            print("[QA Info] Colegio seleccionado desde la tabla.")
            time.sleep(4) # Espera a que el modal se cierre y el curso se cargue
        except Exception:
            print("[QA Warning] No se encontró la tabla de colegios o el colegio no estaba en ella.")

        # 4. Seleccionar curso (Directo al DOM)
        js_curso = f"""
            var select = document.getElementById('CursosColegio');
            for (var i = 0; i < select.options.length; i++) {{
                if (select.options[i].text.trim() === '{curso_val}') {{
                    select.selectedIndex = i;
                    select.dispatchEvent(new Event('change'));
                    return true;
                }}
            }}
            return false;
        """
        if not self.driver.execute_script(js_curso):
            raise Exception("Tras la búsqueda, el campo Curso sigue vacío.")
        

    def _select_materialize_por_texto(self, select_id, texto_opcion):
        """
        Versión mejorada: Selecciona un elemento de Materialize buscando el texto dentro del <ul>
        """
        print(f"[QA Info] Seleccionando '{texto_opcion}' en el combo '{select_id}'...")
        
        # Abrimos el desplegable
        script_click = f"""
            var select = document.getElementById('{select_id}');
            var input = select.previousElementSibling;
            input.click();
            return input;
        """
        self.driver.execute_script(script_click)
        time.sleep(1)
        
        # Buscamos el elemento span que contenga el texto y hacemos clic
        xpath_opcion = f"//ul[contains(@id, 'select-options')]//li/span[text()='{texto_opcion}']"
        opcion = self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath_opcion)))
        self.driver.execute_script("arguments[0].click();", opcion)
        time.sleep(0.5)

    def asegurar_seccion_beneficiario_visible(self):
        self.driver.execute_script("window.scrollBy(0, 600)")
        time.sleep(1)

    def cambiar_a_ventana_cotizador(self):
        print("[QA Info] Esperando a que se abra la nueva pestaña/ventana...")
        self.wait.until(lambda d: len(d.window_handles) > 1)
        self.driver.switch_to.window(self.driver.window_handles[-1])
        
        # Pausa vital: Le damos tiempo al navegador para descargar el HTML de la nueva ventana
        time.sleep(3) 
        print(f"[QA Info] Foco cambiado. Título de la nueva ventana: '{self.driver.title}'")
    
    def validar_pantalla_cotizador(self):
        print("[QA Info] Esperando estabilización de pantalla de cotización...")
        
        self._entrar_al_iframe_si_existe()
        
        try:
            self.wait.until(EC.presence_of_element_located((By.ID, "ApoyoInstitucional")))
            print("[QA Info] Cotizador estable y elemento 'ApoyoInstitucional' encontrado.")
        except Exception:
            print("[QA Error] El elemento 'ApoyoInstitucional' NO se encontró. Generando archivo de depuración...")
            # TRUCO DE QA: Guardamos lo que Selenium está viendo en ese exacto momento para analizarlo
            try:
                with open("debug_pantalla_cotizador.html", "w", encoding="utf-8") as f:
                    f.write(self.driver.page_source)
                print("[QA Info] ¡Archivo 'debug_pantalla_cotizador.html' guardado en tu carpeta! Ábrelo para buscar el ID real del elemento.")
            except Exception as e:
                print(f"[QA Error] No se pudo guardar el archivo debug: {e}")
            
            time.sleep(2) # Pausa de seguridad antes de que el script falle inevitablemente en el siguiente paso

    def seleccionar_global_educacion_360(self):
        btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//a[contains(.,"Global Educacion - Garantizada 360")]')))
        self.driver.execute_script("arguments[0].click();", btn)

    def _entrar_al_iframe_si_existe(self):
        """Busca IFrames o Frames tradicionales y cambia el foco si es necesario."""
        print("[QA Info] Esperando a que el navegador reporte carga completa del HTML...")
        # Esperamos a que el estado del documento sea 'complete' a nivel de JavaScript
        self.wait.until(lambda d: d.execute_script('return document.readyState') == 'complete')
        time.sleep(3) # Pausa estratégica para dar tiempo a renderizados de Materialize/JS
        
        print("[QA Info] Buscando iframes o frames en la pantalla del cotizador...")
        try:
            # Buscamos ambas etiquetas
            iframes = self.driver.find_elements(By.TAG_NAME, "iframe")
            frames = self.driver.find_elements(By.TAG_NAME, "frame")
            todos_los_frames = iframes + frames
            
            if len(todos_los_frames) > 0:
                frame_objetivo = todos_los_frames[0]
                frame_id = frame_objetivo.get_attribute('id') or frame_objetivo.get_attribute('name') or 'Sin_Nombre_ID'
                print(f"[QA Info] Frame detectado ({frame_id}), cambiando foco...")
                self.driver.switch_to.frame(frame_objetivo)
                time.sleep(1.5) # Breve pausa tras cambiar el contexto
            else:
                print("[QA Info] No se detectaron iframes/frames. El formulario debería estar en la ventana principal.")
        except Exception as e:
            print(f"[QA Info] Error durante la validación de frames: {e}")

    def _select_materialize(self, select_id, index):
        """
        Versión agresiva: Forzamos la interacción sin esperar visibilidad.
        """
        # 1. Esperamos únicamente a que el contenedor principal exista
        self.wait.until(EC.presence_of_element_located((By.ID, select_id)))
        
        # 2. Localizamos el input de Materialize mediante JS
        # Buscamos el input que precede al select cuyo ID es select_id
        script = f"""
            var select = document.getElementById('{select_id}');
            var input = select.previousElementSibling;
            input.click();
            return input;
        """
        input_el = self.driver.execute_script(script)
        time.sleep(1.5) # Espera obligatoria para que el UL se renderice
        
        # 3. Seleccionamos la opción mediante JS directamente sobre el elemento
        # Esto ignora cualquier problema de visibilidad o de iframes
        lista_opciones_script = f"""
            var options = document.querySelectorAll('ul.dropdown-content li span');
            options[{index}].click();
        """
        self.driver.execute_script(lista_opciones_script)
        print(f"[QA Info] Interacción forzada por JS en {select_id}")

    def interactuar_con_beneficiario(self, locator, valor):
        try:
            # 1. Esperamos a que el elemento exista en el DOM
            campo = self.wait.until(EC.presence_of_element_located(locator))
            
            # 2. Hacemos scroll para que el campo quede exactamente en el centro de la pantalla
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", campo)
            time.sleep(0.5) # Pequeña pausa para que termine la animación de scroll
            
            # 3. Intentamos escribir normalmente
            campo = self.wait.until(EC.element_to_be_clickable(locator))
            campo.clear()
            campo.send_keys(valor)
            
        except Exception:
            # RESPALDO: Si la interfaz bloquea el teclado, inyectamos el valor con JavaScript directamente
            print(f"[QA Advertencia] El teclado fue bloqueado para {locator}. Inyectando valor con JS...")
            campo = self.wait.until(EC.presence_of_element_located(locator))
            self.driver.execute_script(f"arguments[0].value='{valor}';", campo)
            
            # Disparamos el evento 'change' para engañar a la página y que crea que alguien tecleó
            self.driver.execute_script("arguments[0].dispatchEvent(new Event('change', { bubbles: true }));", campo)
            self.driver.execute_script("arguments[0].dispatchEvent(new Event('blur', { bubbles: true }));", campo)

    def clic_boton_cotizar(self):
        print("[QA Info] Buscando el botón Cotizar...")
        try:
            # Buscamos un botón que contenga el ID btnCotizar o la palabra Cotizar en su texto/value
            xpath_btn = "//*[@id='btnCotizar'] | //input[contains(translate(@value, 'COTIZAR', 'cotizar'), 'cotizar')] | //a[contains(translate(., 'COTIZAR', 'cotizar'), 'cotizar')]"
            
            # Usamos presence_of_element_located en lugar de element_to_be_clickable para evitar bloqueos gráficos
            boton = self.wait.until(EC.presence_of_element_located((By.XPATH, xpath_btn)))
            
            # Hacemos scroll
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", boton)
            time.sleep(1) 
            
            # Clic forzado por JavaScript (Infalible)
            self.driver.execute_script("arguments[0].click();", boton)
            print("[QA Info] Clic en botón Cotizar exitoso.")
            
        except Exception as e:
            print(f"[QA Error] No se pudo hacer clic en el botón de cotizar. Generando debug...")
            with open("debug_boton_cotizar.html", "w", encoding="utf-8") as f:
                f.write(self.driver.page_source)
            raise e

    def scroll_hasta_opciones_cotizacion(self):
        print("[QA] Desplazando hasta Opciones de Cotización...")
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            self.wait.until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        "//a[contains(.,'Global Educacion - Garantizada 360')]"
                    )
                )
            )
        )
        time.sleep(1)

    # =========================================================================
    # Corrección: Integrado a la clase y ajustado el llamado al método correcto
    # =========================================================================
    def seleccionar_apoyo_institucional(self):
        # Ajustado para usar _select_materialize y pasar un índice numérico.
        # Cambia el '1' por el índice real de la opción "Si" en tu lista desplegable.
        self._select_materialize("ApoyoInstitucional", 1) 


    
    # =========================================================================
    # Nuevo método para el select del beneficiario
    # =========================================================================
    def seleccionar_tipo_documento_beneficiario(self, tipo_documento: str):
        print(f"[QA Info] Intentando seleccionar el documento de beneficiario: {tipo_documento}")
        
        locator_input = (By.XPATH, "//select[@id='TipoIdentificacionBen']/preceding-sibling::input[contains(@class, 'select-dropdown')]")
        locator_opcion = (By.XPATH, f"//select[@id='TipoIdentificacionBen']/preceding-sibling::ul//li/span[text()='{tipo_documento}']")
        
        try:
            input_element = self.wait.until(EC.presence_of_element_located(locator_input))
            self.driver.execute_script("arguments[0].click();", input_element)
            time.sleep(0.5) 
            
            opcion_element = self.wait.until(EC.presence_of_element_located(locator_opcion))
            self.driver.execute_script("arguments[0].click();", opcion_element)
            
            print(f"[QA Info] Tipo de documento '{tipo_documento}' seleccionado con éxito.")
            
        except Exception as e:
            print(f"[QA Error] No se pudo seleccionar el documento del beneficiario: {e}")
            raise
    
    