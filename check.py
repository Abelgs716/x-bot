"""Comprueba que las claves de X funcionan (no publica nada)."""
from common import x_client
me = x_client().get_me().data
print(f"OK: conectado como @{me.username}")
