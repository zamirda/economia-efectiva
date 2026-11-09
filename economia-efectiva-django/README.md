# Economía Efectiva – Página web (Django + Render)

Página de Economía Efectiva (Sogamoso y Bogotá) hecha con Django. Dorado, negro y blanco, botón de accesibilidad, sedes, alianzas de libranza y formulario de contacto.

## Estructura

```
economia-efectiva-django/
├── manage.py
├── economia_efectiva/     # configuración (settings, urls, wsgi)
├── web/
│   ├── templates/web/index.html   # la página
│   ├── static/web/logo.jpg        # logo
│   ├── views.py                   # inicio, /contacto/ y /salud/
│   └── urls.py
├── requirements.txt
├── build.sh                # instala y recopila estáticos (Render)
├── render.yaml             # configuración de Render
├── .env.example
└── README.md
```

## 1. Probar en tu computador (Linux)

```bash
cd economia-efectiva-django
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
DEBUG=1 python manage.py runserver
```

Abre http://127.0.0.1:8000

Sin claves de correo, el mensaje del formulario se imprime en la terminal. Eso es normal en pruebas.

## 2. Subir a GitHub

Crea un repositorio vacío (por ejemplo `economia-efectiva-django`) y, **dentro de esta carpeta**:

```bash
git init
git add .
git commit -m "Página Economía Efectiva con Django"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/economia-efectiva-django.git
git push -u origin main
```

## 3. Publicar en Render

1. Entra a render.com y crea una cuenta con tu GitHub.
2. Pulsa **New**, luego **Web Service**, y elige el repositorio.
3. Render lee `render.yaml`. Si te pide los datos a mano:
   - **Runtime:** Python 3
   - **Build Command:** `./build.sh`
   - **Start Command:** `gunicorn economia_efectiva.wsgi:application`
   - **Plan:** Free
4. En **Environment** agrega:
   - `SECRET_KEY` (cualquier texto largo y aleatorio; con `render.yaml` se genera solo)
   - `RESEND_API_KEY` (ver el punto 4)
5. Pulsa **Create Web Service**. Al terminar, el enlace queda como `https://economia-efectiva.onrender.com`.

Nota: en el plan gratis el servicio se duerme tras unos 15 minutos sin visitas, y la primera visita después puede tardar cerca de un minuto.

## 4. Que los mensajes lleguen al correo

El plan gratis de Render bloquea el correo por SMTP, así que el formulario envía por HTTPS con Resend:

1. Crea una cuenta en resend.com **con el correo economiaefectivasogamoso@gmail.com**.
2. En **API Keys** crea una clave y pégala en Render como `RESEND_API_KEY`.
3. Con la cuenta gratis, Resend solo entrega al correo con el que te registraste. Para enviar a otros correos hay que verificar un dominio propio.

Si el envío falla, el formulario abre el programa de correo del cliente con el mensaje listo.

## 5. WhatsApp

Los botones de WhatsApp abren el chat con el mensaje escrito, y el cliente solo pulsa enviar. El envío automático por WhatsApp necesita WhatsApp Business API o Twilio, que son de pago.

## 6. Dominio propio

En Render: **Settings**, luego **Custom Domains**. Agrega el dominio y crea el registro DNS que te indique. Si usas dominio propio, añade en Environment la variable `DOMINIOS=tudominio.com,www.tudominio.com`.

## Variables

| Variable | Para qué |
|---|---|
| `SECRET_KEY` | Clave de Django (obligatoria en producción) |
| `RESEND_API_KEY` | Envío de correo por HTTPS |
| `CONTACT_EMAIL` | Quién recibe los mensajes (por defecto economiaefectivasogamoso@gmail.com) |
| `DOMINIOS` | Dominios propios, separados por coma |
| `DEBUG` | `1` solo para pruebas locales |
