# language: es
Característica: Flujo Completo de Registro y Cotización en el Portal

  Escenario: Registrar un nuevo cliente con cédula de ciudadanía y generarle una cotización 360
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
    Entonces el sistema debe generar la cotización correctamente
    Y cierra la cotización con el botón "Cerrar"
