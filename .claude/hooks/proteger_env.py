# .claude/hooks/proteger_env.py — Impide que Claude lea, muestre o cambie el .env
#
# El .env tiene las claves de Anthropic, YCloud y Railway. Claude no las necesita
# ver nunca: Seri las lee sola al arrancar.

import json
import os
import re
import sys

# Comandos que solo miran si el archivo existe, sin mostrar su contenido
SOLO_MIRAR = re.compile(r"^\s*(ls|test|\[|stat|git (status|check-ignore|ls-files))\b")
# ".env" como archivo, pero no ".env.example" ni ".envrc"
MENCIONA_ENV = re.compile(r"(^|[\s/'\"=<>])\.env(?![\w.-])")


def es_env(ruta):
    return os.path.basename(ruta or "") == ".env"


evento = json.load(sys.stdin)
herramienta = evento.get("tool_name", "")
entrada = evento.get("tool_input", {})

if herramienta == "Bash":
    comando = entrada.get("command", "")
    bloquear = MENCIONA_ENV.search(comando) and not SOLO_MIRAR.match(comando)
else:
    bloquear = es_env(entrada.get("file_path")) or es_env(entrada.get("path"))

if bloquear:
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": (
                "Bloqueado: el .env tiene las claves de Seri y no se lee ni se modifica "
                "desde Claude. Si hay que cambiar una clave, Claudio la edita a mano."
            ),
        }
    }))
