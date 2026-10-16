# language: es
Característica: Volver a Cotizar desde el resumen de la cotización

  # Antecedentes: pasos que se ejecutan ANTES de cada escenario de este archivo.
  # Dejan un cliente nuevo con una cotización Global Garantizada 360 en la pantalla de resumen.
  Antecedentes: Cliente nuevo con una cotización Global Garantizada 360 en el resumen
    Dado que el analista de QA ha iniciado sesión en el portal
    Cuando navega a la sección de cotizaciones
    Y ingresa a "Mis Cotizaciones"
    Y busca un documento único para el tipo "CIUDADANIA"
    Y avanza al formulario para registrar al nuevo cliente
    Y completa los datos personales y geográficos para el tipo "CIUDADANIA"
    Y el sistema debe confirmar que la grabación del nuevo cliente se realizó correctamente
    Y el analista se desplaza hasta la sección "Opciones de Cotización"
    Y selecciona el producto "Global Educacion Garantizada 360"
    Y el sistema debe abrir la pantalla "Cotizador en Línea"
    Y diligencia la información requerida para la cotización
    Y hace clic en el botón "Cotizar"
    Y selecciona todas las coberturas y da clic en "Continuar"
    Y el sistema debe generar la cotización correctamente

  Escenario: Volver a cotizar con otro año de ingreso y solo algunas coberturas
    Cuando da clic en el botón "Volver a Cotizar"
    Y el analista se desplaza hasta la sección "Opciones de Cotización"
    Y selecciona el producto "Global Educacion Garantizada 360"
    Y el sistema debe abrir la pantalla "Cotizador en Línea"
    Y diligencia la información de la cotización sumando 1 al año de ingreso calculado
    Y hace clic en el botón "Cotizar"
    Y selecciona solo las coberturas "Vida Protección Familiar, Renta Bienestar Universitaria" y da clic en "Continuar"
    Entonces el sistema debe generar la cotización correctamente
    Y cierra la cotización con el botón "Cerrar"
