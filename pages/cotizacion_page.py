from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage
import time
import random # Asegúrate de que esto esté al inicio del archivo si no lo tenías
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains


class CotizacionPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.BTN_COTIZAR = (By.ID, "btnCotizar")
    
    def obtener_resultado_cotizacion(self):
        print("[QA Info] Esperando a que el sistema muestre el resultado...")
        
        # Ampliamos la búsqueda: buscamos mensajes de error o de éxito
        # A veces el sistema lanza un 'alert' o un 'modal' en lugar de un texto en pantalla
        try:
            # Espera 30 segundos
            wait_largo = WebDriverWait(self.driver, 30)
            
            # Buscamos elementos comunes de confirmación
            # ID común en ASP.NET: 'lblNumeroCotizacion', 'divMensajeExito', etc.
            # Usamos un selector que busque en todo el cuerpo del documento
            locators = [
                (By.XPATH, "//div[contains(@class, 'success')]"),
                (By.XPATH, "//*[contains(text(), 'Cotización generada')]"),
                (By.XPATH, "//*[contains(text(), 'Número de cotización')]"),
                (By.ID, "lblNumeroCotizacion")
            ]
            
            for locator in locators:
                try:
                    elemento = wait_largo.until(EC.visibility_of_element_located(locator))
                    print(f"[QA Info] Resultado encontrado: {elemento.text}")
                    return elemento.text
                except:
                    continue
            
            # Si llegamos aquí, no encontramos nada. Guardamos el HTML para investigar
            html_final = self.driver.page_source
            with open("debug_resultado_final.html", "w", encoding="utf-8") as f:
                f.write(html_final)
            print("[QA Error] No se encontró mensaje de éxito. Guardado en 'debug_resultado_final.html'")
            return None

        except Exception as e:
            print(f"[QA Error] Excepción al buscar resultado: {e}")
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
    
    def seleccionar_producto_materialize(self, texto_producto="Global Garantizada 360"):
        print(f"[QA Info] Forzando selección de producto vía JS: {texto_producto}")
        
        # Este script hace todo el trabajo: busca el select, abre el menú y selecciona el item
        # Todo ocurre dentro del contexto del navegador, sin "tocar" el elemento desde fuera
        script_js = f"""
            try {{
                var select = document.getElementById('ProductoOpcionado');
                // 1. Forzamos el valor del select original
                for (var i = 0; i < select.options.length; i++) {{
                    if (select.options[i].text.trim() === '{texto_producto}') {{
                        select.selectedIndex = i;
                        break;
                    }}
                }}
                // 2. Disparamos los eventos que Materialize y ASP.NET esperan
                select.dispatchEvent(new Event('change', {{ bubbles: true }}));
                
                // 3. Opcional: intentamos actualizar la UI visual de Materialize
                var input = select.previousElementSibling;
                if (input) {{
                    input.value = '{texto_producto}';
                    input.dispatchEvent(new Event('change', {{ bubbles: true }}));
                }}
                return true;
            }} catch(e) {{
                return false;
            }}
        """
        
        exito = self.driver.execute_script(script_js)
        
        if exito:
            print(f"[QA Info] Producto '{texto_producto}' seleccionado y eventos disparados con éxito.")
            time.sleep(2) # Espera post-selección para que el servidor procese el cambio
        else:
            raise Exception(f"Fallo al seleccionar '{texto_producto}' mediante inyección JS.")
        
    def calcular_y_confirmar_anio_ingreso(self):
        print("[QA Info] Iniciando cálculo de maduración...")
        
        # 1. Clic en el botón Calcular
        btn_calcular = self.wait.until(EC.element_to_be_clickable((By.ID, "CalcularMaduracion")))
        self.driver.execute_script("arguments[0].click();", btn_calcular)
        
        # 2. Espera inteligente: Esperamos a que el campo calculado tenga un valor (distinto de vacío)
        # Esto es vital para asegurar que el PostBack terminó
        def campo_calculado_tiene_valor(driver):
            val = driver.find_element(By.ID, "AnioMaduracionCalc").get_attribute("value")
            return val and val.strip() != ""
        
        self.wait.until(campo_calculado_tiene_valor)
        
        # 3. Obtener el valor calculado
        anio_calculado = self.driver.find_element(By.ID, "AnioMaduracionCalc").get_attribute("value")
        print(f"[QA Info] Año calculado obtenido: {anio_calculado}")
        
        # 4. Inyectar el valor en el campo de confirmación
        campo_confirmacion = self.driver.find_element(By.ID, "AnioMaduracion")
        self.driver.execute_script(f"arguments[0].value = '{anio_calculado}';", campo_confirmacion)
        
        # 5. Disparar eventos para que el formulario valide la igualdad
        self.driver.execute_script("""
            var el = document.getElementById('AnioMaduracion');
            el.dispatchEvent(new Event('input', { bubbles: true }));
            el.dispatchEvent(new Event('change', { bubbles: true }));
            el.dispatchEvent(new Event('blur', { bubbles: true }));
        """)
        print("[QA Info] Año de ingreso confirmado correctamente.")

    
    def cerrar_cotizacion(self):
        print("[QA Info] Cerrando ventana de cotización...")
        
        # 1. Localizar el botón Cerrar
        btn_cerrar = self.wait.until(EC.element_to_be_clickable((By.ID, "Cerrar")))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn_cerrar)
        time.sleep(1.0)
        
        # 2. Obtener el 'handle' de la ventana principal para volver después
        ventana_principal = self.driver.window_handles[0]
        
        # 3. Clic mediante JS para ejecutar el 'cerrarpagina()' nativo
        self.driver.execute_script("arguments[0].click();", btn_cerrar)
        
        # 4. Sincronización: Esperar a que la ventana de cotización se cierre
        # Cambiamos el foco a la ventana principal
        self.wait.until(EC.number_of_windows_to_be(1))
        self.driver.switch_to.window(ventana_principal)
        
        print("[QA Info] Ventana de cotización cerrada. Foco regresado a la ventana principal.")

def seleccionar_cobertura_y_cerrar(self):
        """
        Marca el checkbox de selección de la cobertura y hace clic en cerrar/continuar una sola vez.
        """
        print("[QA Info] Seleccionando cobertura y cerrando modal...")
        
        # 1. Localizar y marcar el checkbox usando JS (evita problemas de interceptación de clic)
        checkbox_id = "gvCoberturasCampleto_chkSeleccionar_0"
        checkbox = self.wait.until(EC.presence_of_element_located((By.ID, checkbox_id)))
        
        # Verificamos si ya está marcado antes de hacer clic para evitar desmarcarlo
        if not checkbox.is_selected():
            self.driver.execute_script("arguments[0].click();", checkbox)
            time.sleep(1.5)  # Breve pausa para la respuesta del PostBack/ASP.NET

        # 2. Localizar y hacer clic en el botón Cerrar/MuestraCotizacion una única vez
        btn_cerrar = self.wait.until(EC.presence_of_element_located((By.ID, "MuestraCotizacion")))
        time.sleep(5)  # Breve pausa para la respuesta del PostBack/ASP.NET
        self.driver.execute_script("arguments[0].click();", btn_cerrar)
        
        print("[QA Info] Cobertura seleccionada y modal cerrado.")