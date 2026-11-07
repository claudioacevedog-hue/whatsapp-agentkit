# .claude/skills/contacto-seri/contacto.py — Marca un número como cliente o personal para Seri
#
# Uso (desde la carpeta del proyecto):
#   .venv/bin/python .claude/skills/contacto-seri/contacto.py buscar   "+56 9 1234 5678"
#   .venv/bin/python .claude/skills/contacto-seri/contacto.py cliente  "+56 9 1234 5678" "Juan Pérez (Empresa X)"
#   .venv/bin/python .claude/skills/contacto-seri/contacto.py personal "+56 9 1234 5678" "Tío Juan"
#   Agrega --prueba al final para ver qué haría sin guardar nada.
#
# Escribe con yaml (nunca a mano) y conserva los comentarios de arriba de cada archivo.

import sys

import yaml

PERSONALES = ("config/contactos_personales.yaml", "contactos")
CLIENTES = ("config/clientes_extra.yaml", "clientes")


def digitos(numero):
    """Últimos 9 dígitos: así compara Seri (agent/tools.py)."""
    return "".join(c for c in str(numero) if c.isdigit())[-9:]


def leer(archivo):
    with open(archivo, encoding="utf-8") as f:
        texto = f.read()
    cabecera = "".join(l for l in texto.splitlines(keepends=True) if l.startswith("#"))
    return cabecera, yaml.safe_load(texto) or {}


def guardar(archivo, cabecera, datos):
    cuerpo = yaml.safe_dump(datos, allow_unicode=True, sort_keys=False)
    yaml.safe_load(cuerpo)  # si esto falla, no se escribe nada
    with open(archivo, "w", encoding="utf-8") as f:
        f.write(cabecera + cuerpo)


def buscar(num):
    for archivo, clave in (PERSONALES, CLIENTES):
        _, datos = leer(archivo)
        for c in datos.get(clave) or []:
            if digitos(c.get("numero")) == num:
                print(f"- en {archivo}: {c.get('nombre')}")


def main():
    args = [a for a in sys.argv[1:] if a != "--prueba"]
    prueba = "--prueba" in sys.argv
    if len(args) < 2 or args[0] not in ("buscar", "cliente", "personal"):
        print(__doc__ or "uso: buscar|cliente|personal NUMERO [NOMBRE] [--prueba]")
        sys.exit(1)

    accion, num = args[0], digitos(args[1])
    nombre = args[2] if len(args) > 2 else "Sin nombre"
    if len(num) < 8:
        print(f"El número '{args[1]}' no parece válido (muy pocos dígitos).")
        sys.exit(1)

    print("Antes:")
    buscar(num)

    if accion == "buscar":
        return

    # Cliente: va a clientes_extra (que manda sobre la lista de personales).
    # Personal: va a personales y sale de clientes_extra si estaba ahí.
    destino, otro = (CLIENTES, PERSONALES) if accion == "cliente" else (PERSONALES, CLIENTES)

    cab, datos = leer(destino[0])
    lista = datos.setdefault(destino[1], [])
    if any(digitos(c.get("numero")) == num for c in lista):
        print(f"Ya estaba en {destino[0]}; no se agrega de nuevo.")
    else:
        lista.append({"nombre": nombre, "numero": num})
        print(f"+ se agrega a {destino[0]}: {nombre}")
        if not prueba:
            guardar(destino[0], cab, datos)

    if accion == "personal":
        cab, datos = leer(otro[0])
        antes = datos.get(otro[1]) or []
        despues = [c for c in antes if digitos(c.get("numero")) != num]
        if len(despues) != len(antes):
            print(f"- se quita de {otro[0]}")
            datos[otro[1]] = despues
            if not prueba:
                guardar(otro[0], cab, datos)

    print("(prueba: no se guardó nada)" if prueba else "Guardado. Falta publicar con /publicar-seri.")


if __name__ == "__main__":
    main()
