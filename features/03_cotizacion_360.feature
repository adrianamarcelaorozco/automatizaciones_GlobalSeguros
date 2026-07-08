# language: es

Característica: Cotización Global Garantizada 360

  Como analista de QA
  Quiero generar una cotización para un cliente recién registrado
  Para validar que el cotizador en línea genera una cotización correctamente

  Escenario: Generar una cotización Global Garantizada 360 para un cliente con cédula de ciudadanía

    Dado que existe un cliente registrado con cédula de ciudadanía
    Cuando el analista se desplaza hasta la sección "Opciones de Cotización"
    Y selecciona el producto "Global Educacion Garantizada 360"
    Entonces el sistema debe abrir la pantalla "Cotizador en Línea"
    Cuando diligencia la información requerida para la cotización
    Y hace clic en el botón "Cotizar"
    Entonces el sistema debe generar la cotización correctamente