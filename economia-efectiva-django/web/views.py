import json
import logging
import urllib.request

from django.conf import settings
from django.core.mail import EmailMessage
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST

log = logging.getLogger(__name__)


def inicio(request):
    return render(request, "web/index.html")


def salud(request):
    return HttpResponse("ok")


def _enviar_resend(asunto, texto, responder_a):
    """Envío por HTTPS (funciona en el plan gratis de Render, que bloquea SMTP)."""
    datos = {
        "from": settings.RESEND_FROM,
        "to": [settings.CONTACT_EMAIL],
        "subject": asunto,
        "text": texto,
    }
    if responder_a:
        datos["reply_to"] = responder_a
    req = urllib.request.Request(
        "https://api.resend.com/emails",
        data=json.dumps(datos).encode("utf-8"),
        headers={
            "Authorization": "Bearer " + settings.RESEND_API_KEY,
            "Content-Type": "application/json",
            "User-Agent": "economia-efectiva/1.0",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=15) as r:
        if r.status >= 300:
            raise RuntimeError("Resend respondió " + str(r.status))


@require_POST
def contacto(request):
    try:
        d = json.loads(request.body.decode("utf-8"))
    except (ValueError, UnicodeDecodeError):
        return JsonResponse({"ok": False, "error": "Datos no válidos."}, status=400)

    nombre = str(d.get("nombre", "")).strip()[:120]
    telefono = str(d.get("telefono", "")).strip()[:40]
    correo = str(d.get("correo", "")).strip()[:120]
    tipo = str(d.get("tipo", "")).strip()[:80]
    mensaje = str(d.get("mensaje", "")).strip()[:2000]

    if not nombre or not telefono:
        return JsonResponse({"ok": False, "error": "Falta nombre o teléfono."}, status=400)

    if correo:
        try:
            validate_email(correo)
        except ValidationError:
            correo = ""

    asunto = "Nueva consulta web: " + (tipo or "Economía Efectiva")
    texto = (
        "Nombre: {}\nTeléfono: {}\nCorreo: {}\nMe interesa: {}\n\nMensaje:\n{}\n"
    ).format(nombre, telefono, correo or "No indicado", tipo or "No indicado", mensaje or "Quisiera más información.")
    texto = texto.replace("\r", "")
    asunto = asunto.replace("\n", " ").replace("\r", " ")

    try:
        if settings.RESEND_API_KEY:
            _enviar_resend(asunto, texto, correo)
        else:
            EmailMessage(
                asunto, texto, settings.DEFAULT_FROM_EMAIL,
                [settings.CONTACT_EMAIL], reply_to=[correo] if correo else None,
            ).send(fail_silently=False)
    except Exception:
        log.exception("No se pudo enviar el correo de contacto")
        return JsonResponse({"ok": False, "error": "No se pudo enviar."}, status=502)

    return JsonResponse({"ok": True})
