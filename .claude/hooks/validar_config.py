# .claude/hooks/validar_config.py — Revisa config/*.yaml cada vez que Claude lo edita
#
# Si el archivo quedó con formato roto, avisa a Claude (código 2) para que lo
# arregle antes de seguir. Así un error nunca llega a Railway.

import json
import os
import sys

import yaml


def numeros_ok(datos, clave):
    """La lista de contactos/clientes debe ser una lista de fichas con 'numero'."""
    lista = (datos or {}).get(clave)
    if not isinstance(lista, list):
        return f"falta la lista '{clave}:'"
    for i, c in enumerate(lista, 1):
        if not isinstance(c, dict) or not str(c.get("numero", "")).strip():
            return f"la ficha n.º {i} de '{clave}' no tiene 'numero'"
    return None


evento = json.load(sys.stdin)
ruta = (evento.get("tool_response") or {}).get("filePath") or evento.get("tool_input", {}).get("file_path", "")
raiz = os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())
relativa = os.path.relpath(ruta, raiz) if ruta else ""

if not relativa.startswith("config" + os.sep) or not relativa.endswith((".yaml", ".yml")):
    sys.exit(0)

try:
    with open(ruta, encoding="utf-8") as f:
        datos = yaml.safe_load(f)
except Exception as e:
    print(f"⚠️ {relativa} quedó con el formato roto y Seri no podría leerlo: {e}", file=sys.stderr)
    sys.exit(2)

nombre = os.path.basename(ruta)
problema = None
if nombre == "contactos_personales.yaml":
    problema = numeros_ok(datos, "contactos")
elif nombre == "clientes_extra.yaml":
    problema = numeros_ok(datos, "clientes")
elif nombre in ("business.yaml", "prompts.yaml") and not isinstance(datos, dict):
    problema = "el archivo quedó vacío o sin secciones"

if problema:
    print(f"⚠️ {relativa}: {problema}. Corrígelo antes de publicar.", file=sys.stderr)
    sys.exit(2)
