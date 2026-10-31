# Estado de la entrevista AgentKit — Serigraf (pausa)

> Este repo es PÚBLICO. Aquí solo va lo que no es sensible.
> Los datos privados (número de Ana, dirección, lista de precios completa)
> NO están aquí: Claudio tiene los archivos `session.yaml` y `precios_2026.md`
> que se le enviaron por el chat, y los vuelve a subir en la sesión nueva.

## Fase actual
Fase 2 de 5 — Entrevista. Falta solo la Pregunta 10 (cuenta Twilio).

## Respuestas confirmadas
- Negocio: Serigraf (Servicios Serigraf® SpA). Fuente base: www.serigraf.cl
- Agente: Seri. Presentación aprobada:
  "Hola! Soy Seri, asistente virtual de Serigraf®️ SpA. Te atiendo mientras Claudio se desocupa,
  y si necesitas algo que yo no pueda resolver, él te responde por aquí mismo."
- Tono: amigable y casual (tutea).
- Casos de uso: FAQ, calificar leads/armar cotización, registrar solicitudes de pedido
  (sin confirmar precio ni fecha), recibir post-venta y escalar (sin inventar estado). Sin agendar.
- Escalamiento (opción 3): Seri avisa por WhatsApp a Ana (número en variable NOTIFICAR_WHATSAPP)
  y por correo a ventas@serigraf.cl. Claudio responde por el mismo chat.
- Horario: L-V 9:00-13:00 y 14:00-18:00 (America/Santiago). Sáb/dom cerrado.
  Colación: "Claudio se desocupa y te atiende". Feriados: atiende solo Seri.
- Pago: transferencia y efectivo.
- Despacho: sin reparto propio; por pagar con la empresa que elija el cliente,
  solo con trabajo terminado y transferencia verificada. Retiro en taller (dirección en archivo privado).
- Precios: Seri SOLO informa montos de trabajo mínimo por técnica. Producción mínima: desde 1 unidad
  hasta completar el mínimo se cobra el trabajo mínimo. Trazado: desde $30.000 neto + IVA.
- Proveedor WhatsApp: Twilio (sandbox para pruebas).

## Pendientes
1. Crear API key Anthropic y cargarla como variable de entorno ANTHROPIC_API_KEY (desde el Mac, claude.ai/code).
2. Cuenta Twilio: TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER como variables de entorno.
3. Variables NOTIFICAR_WHATSAPP y NOTIFICAR_EMAIL en el entorno.
4. Claudio corrige en la web el texto "arte sin costo".
5. Futuro: fichas de clientes/agencias; feriados chilenos.

## Para retomar
Abrir sesión nueva en este repo y decir: "Retoma AgentKit desde onboarding/estado_entrevista.md"
y subir los dos archivos privados.
