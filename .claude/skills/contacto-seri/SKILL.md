---
name: contacto-seri
description: Marca un número de WhatsApp como cliente (Seri lo atiende) o personal (Seri no le responde). Úsalo cuando Claudio diga "agrega a X como cliente", "X es personal", "Seri no le conteste a X", "¿X está como cliente?" o "/contacto-seri".
---

# Contacto para Seri

Seri decide a quién atender con dos listas:
- `config/contactos_personales.yaml` — Seri NO responde (familia, amigos, proveedores personales).
- `config/clientes_extra.yaml` — clientes que Seri SÍ atiende aunque estén en la agenda; esta lista manda sobre la otra.
- Un número que no está en ninguna lista = cliente nuevo (Seri lo atiende).

Compara por los últimos 9 dígitos, así que el formato del número da igual.

## Pasos

1. Si falta el número o no está claro si es cliente o personal, pregunta solo eso.
2. Mira dónde está hoy:
   ```bash
   .venv/bin/python .claude/skills/contacto-seri/contacto.py buscar "NUMERO"
   ```
3. Haz el cambio (nunca edites estas listas a mano ni con printf/sed: siempre con este script):
   ```bash
   .venv/bin/python .claude/skills/contacto-seri/contacto.py cliente  "NUMERO" "Nombre (Empresa)"
   .venv/bin/python .claude/skills/contacto-seri/contacto.py personal "NUMERO" "Nombre"
   ```
   Con varios contactos, repite el comando por cada uno.
4. Nunca agregues el número de Serigraf (950594156): es el propio WhatsApp de Seri.
5. Cuéntale a Claudio en una línea qué cambió y recuérdale que **el cambio se activa al
   publicar** (`/publicar-seri`). Si son varios cambios, conviene juntarlos y publicar una vez,
   fuera de horario de atención.
6. Consejo para Claudio: si un cliente nuevo es una empresa, lo ideal a futuro es marcarlo
   como **empresa** en Contactos del iPhone; esta lista es el atajo mientras tanto.
