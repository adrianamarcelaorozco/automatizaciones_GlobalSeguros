import pytest
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from pages.cliente_nuevo_page import BusquedaClientePage, TipoDocumento

class TestClienteNuevo:

    # Mantenimiento automático: lee directamente las opciones del Enum
    @pytest.mark.parametrize("tipo_doc_evaluado", list(TipoDocumento))
    def test_crear_nuevos_clientes_flujo_completo(self, login_autenticado, tipo_doc_evaluado):
        """Caso de prueba maestro: Genera y registra un cliente aleatorio único por cada tipo de documento."""
        driver = login_autenticado
        
        print(f"\n============= INICIANDO FLUJO: {tipo_doc_evaluado.name} =============")
        
        # 1. Resetear contexto de iframes y enfocar el área de trabajo
        driver.switch_to.default_content()
        WebDriverWait(driver, 15).until(
            EC.frame_to_be_available_and_switch_to_it((By.ID, "contenido"))
        )
        
        pagina_busqueda = BusquedaClientePage(driver)
        
        # GENERACIÓN DINÁMICA DE DATOS ÚNICOS POR ITERACIÓN
        # Tomamos el timestamp actual como base para evitar colisiones
        tiempo_actual = str(int(time.time()))
        
        # Asignación de prefijos y longitudes según reglas estrictas del negocio colombiano
        if tipo_doc_evaluado == TipoDocumento.CIUDADANIA:
            # CC: Prefijo "10" + 7 dígitos = 9 dígitos en total
            semilla_numerica = tiempo_actual[-7:]
            documento_ramdom = "10" + semilla_numerica
        elif tipo_doc_evaluado == TipoDocumento.EXTRANJERIA:
            # CE: Prefijo "90" + 7 dígitos = 9 dígitos en total
            semilla_numerica = tiempo_actual[-7:]
            documento_ramdom = "90" + semilla_numerica
        else:
            # 📌 PPT: Exige entre 5 y 7 dígitos. 
            # Prefijo "5" + 5 dígitos extraídos del tiempo = 6 dígitos en total (Pasa la regla perfectamente)
            semilla_numerica = tiempo_actual[-5:]
            documento_ramdom = "5" + semilla_numerica

        # El correo y celular usan la semilla generada para mantener la unicidad del caso
        correo_dinamico = f"qa_global_{tipo_doc_evaluado.name.lower()}_{semilla_numerica}@globaleguros.com"
        celular_dinamico = "312" + tiempo_actual[-7:]
        
        # 2. Primera Búsqueda (Verifica que el cliente no exista)
        pagina_busqueda.ingresar_y_buscar_cliente(
            numero_documento=documento_ramdom, 
            tipo_documento=tipo_doc_evaluado
        )
        
        # 3. Avanzar al Formulario de Creación
        pagina_busqueda.click_nuevo_cliente()
        
        # 4. Diligenciar el formulario completo usando datos geográficos exactos del HTML
        pagina_busqueda.completar_datos_personales(
            numero_documento=documento_ramdom,
            tipo_documento=tipo_doc_evaluado,
            correo=correo_dinamico,
            celular=celular_dinamico,
            departamento="DISTRITO CAPITAL",  # Mapeado al texto exacto de tu lista
            ciudad="BOGOTA"
        )
        
        # 5. Captura y validación (Assert) del popup de confirmación exitosa
        mensaje_capturado = pagina_busqueda.obtener_mensaje_exito_y_cerrar()
        
        assert "Grabación realizada correctamente" in mensaje_capturado, \
            f"Error de Negocio: No se confirmó el guardado. Mensaje en pantalla: '{mensaje_capturado}'"
        
        print(f"[QA Info] Registro exitoso verificado para {tipo_doc_evaluado.name} con documento {documento_ramdom}.")
        print(f"============= FINALIZADO FLUJO: {tipo_doc_evaluado.name} =============\n")