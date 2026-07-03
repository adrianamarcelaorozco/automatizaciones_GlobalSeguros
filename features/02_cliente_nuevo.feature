# language: es
Característica: Registro de nuevos clientes en el portal

  Esquema del escenario: Crear nuevos clientes de forma exitosa por tipo de documento
    Dado que el analista de QA ha iniciado sesión y navegado a la sección de cotizaciones
    Cuando busca un documento único para el tipo "<tipo_doc_key>"
    Y avanza al formulario para registrar al nuevo cliente
    Y completa los datos personales y geográficos para el tipo "<tipo_doc_key>"
    Entonces el sistema debe confirmar que la grabación se realizó correctamente

    Ejemplos:
      | tipo_doc_key        |
      | CIUDADANIA          |
      | EXTRANJERIA         |
      | PROTECCION_TEMPORAL |