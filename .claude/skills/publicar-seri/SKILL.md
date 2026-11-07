---
name: publicar-seri
description: Publica los cambios de Seri en Railway de forma segura - revisa horario, formato de config y código, sube, confirma que responde y respalda en iCloud. Úsalo cuando Claudio diga "publica", "sube los cambios", "deploy" o "/publicar-seri".
disable-model-invocation: true
---

# Publicar Seri

Claudio es principiante: explica cada paso en español simple, uno a la vez, y marca
[Seguro]/[Probable]/[No lo sé]. Nunca muestres ni leas el `.env`.

Sigue estos pasos EN ORDEN. Si uno falla, para, explica qué pasó y no sigas.

## 1. ¿Es buen momento?

```bash
TZ=America/Santiago date "+%A %H:%M"
```

Mientras Railway reinicia (1-2 min), los mensajes que estén esperando el minuto de
Seri se pierden. Si es lunes a viernes entre 9:00-13:00 o 14:00-18:00, avísale a
Claudio y pregúntale si publica igual o espera. Fuera de horario, sigue.

## 2. Revisar que todo esté sano

```bash
for f in config/*.yaml; do echo "{\"tool_input\":{\"file_path\":\"$PWD/$f\"}}" | CLAUDE_PROJECT_DIR=$PWD .venv/bin/python .claude/hooks/validar_config.py && echo "OK $f"; done
.venv/bin/python -m py_compile agent/*.py agent/providers/*.py && echo "código OK"
```

Todo debe decir OK. (`session.yaml` no se sube; si falla solo ese, avisa pero sigue.)

## 3. Contarle a Claudio qué se va a subir

Resume en 2-4 líneas qué cambió desde la última publicación (precios, contactos,
reglas, código). Pídele un "sí" antes de seguir.

## 4. Publicar

```bash
./deploy.sh
```

Debe listar los archivos y terminar sin error. Nunca subir por GitHub (el repo es público).

## 5. Confirmar que Seri quedó viva

Espera ~90 segundos y revisa:

```bash
curl -s -o /dev/null -w "%{http_code}\n" https://seri-production.up.railway.app/
railway logs --service seri 2>/dev/null | tail -20
```

Debe responder `200` y en los logs debe aparecer que arrancó sin errores
(`Traceback` o `Error` = algo falló → avisa y propone volver atrás).

## 6. Respaldo en iCloud

Un solo respaldo vigente: `respaldos/` local (con fecha) y
`iCloud Drive/Claude/Respaldo-Air-2026-11-01/Seri-agente-WhatsApp.zip`.
Armar fuera de iCloud, verificar, copiar con `ditto` y comparar huellas.

```bash
N=seri-respaldo-$(TZ=America/Santiago date +%Y-%m-%d-%H%M).zip
I="$HOME/Library/Mobile Documents/com~apple~CloudDocs/Claude/Respaldo-Air-2026-11-01"
zip -qr "respaldos/$N" . -x '.venv/*' '.deploy/*' 'respaldos/*' '.git/*' '*__pycache__*' '*.DS_Store'
unzip -tq "respaldos/$N" \
  && ditto "respaldos/$N" "$I/Seri-agente-WhatsApp.zip" \
  && shasum -a 256 "respaldos/$N" "$I/Seri-agente-WhatsApp.zip"
```

Las dos huellas deben ser iguales. Después borra los respaldos locales anteriores
(deja solo el nuevo), mostrando primero cuáles son:

```bash
ls respaldos/
find respaldos -name 'seri-respaldo-*.zip' ! -name "$N" -delete
```

Recuérdale que el zip incluye las claves: es privado, no se comparte.

## 7. Cierre

Dile a Claudio en 3 líneas: qué se publicó, que Seri responde, y dónde quedó el respaldo.
