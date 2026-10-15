"""Configuración central de la suite.

Cualquier valor se puede sobrescribir con una variable de entorno del mismo nombre,
por ejemplo para correr contra otro ambiente o con otro usuario de pruebas.
"""
import os

PORTAL_URL = os.getenv("PORTAL_URL", "http://10.1.2.33/Portal/ingreso-usuarios.aspx")

# Usuario de pruebas (ambiente QA, sin datos reales)
USUARIO_QA = os.getenv("USUARIO_QA", "NCRUZV")
CLAVE_QA = os.getenv("CLAVE_QA", "Clave123")
