# language: es
Característica: Registro de nuevos clientes en el portal

  Esquema del escenario: Verificar visualización de opciones y registro de nuevo cliente
    Dado que el analista de QA ha iniciado sesión en el portal
    Cuando navega a la sección de cotizaciones
    Y el sistema debe mostrar las opciones de "Mis Cotizaciones" y "Adición de Semestre"
    Y busca un documento único para el tipo "<tipo_doc_key>"
    Entonces el sistema debe habilitar la opción para registrar al nuevo cliente   
    
    Ejemplos:
      | tipo_doc_key         |
      | CIUDADANIA           |
      | EXTRANJERIA          |
      | PROTECCION_TEMPORAL  |

    