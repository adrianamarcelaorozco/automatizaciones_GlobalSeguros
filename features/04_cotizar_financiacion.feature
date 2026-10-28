# language: es
Característica: Cotizar financiación desde el resumen de la cotización

  Escenario: Cotizar financiación para un beneficiario menor de 5 años sin datos de colegio
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
    # Menor de 5 años: la sección "Datos sobre el colegio" no se diligencia (no es obligatoria)
    Y diligencia la cotización para un beneficiario de 0 años sin datos de colegio
    Y escribe "pruebas" en las observaciones
    Y hace clic en el botón "Cotizar"
    Y selecciona todas las coberturas y da clic en "Continuar"
    Y el sistema debe generar la cotización correctamente
    Cuando da clic en el botón "Cotizar financiación"
    Y ingresa un valor de cuota inicial de "50000000"
    Y calcula la financiación con el botón "Cotizar financiación"
    Entonces el sistema debe mostrar la tabla de financiación para el producto "Global Garantizada 360"
    Y la cuota inicial de la tabla debe ser la ingresada
    Y el valor a financiar debe ser la prima menos la cuota inicial
    Y el porcentaje de cuota inicial debe corresponder a la cuota sobre la prima
    Y todas las cuotas mensuales deben tener valor mayor a cero
    Y cierra la cotización con el botón "Cerrar"
