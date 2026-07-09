# language: es
Característica: Flujo Completo de Registro y Cotización en el Portal

  Escenario: Registrar un nuevo cliente con cédula de ciudadanía y generarle una cotización 360
    Dado que el analista de QA nuevo ha iniciado sesión en el portal
    Cuando navega a la sección de cotizaciones del nuevo flujo
    Y busca un documento único para el nuevo tipo "CIUDADANIA"
    Y avanza al formulario para registrar al nuevo cliente unificado
    Y completa los datos personales y geográficos para el nuevo tipo "CIUDADANIA"
    Y el sistema debe confirmar que la grabación del nuevo cliente se realizó correctamente
    Y el analista se desplaza hasta la sección "Opciones de Cotización" del nuevo flujo
    Y selecciona el producto "Global Educacion Garantizada 360"
    Y el sistema debe abrir la pantalla "Cotizador en Línea"
    Y diligencia la información requerida para la cotización
    Y hace clic en el botón "Cotizar"
    Entonces el sistema debe generar la cotización correctamente