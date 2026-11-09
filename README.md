# Economía Efectiva – Página web (Django + Docker + Render)

Página de Economía Efectiva (Sogamoso y Bogotá) hecha con Django. Dorado, negro y blanco, botón de accesibilidad, sedes, alianzas de libranza y formulario de contacto. Funciona de tres formas: con Django directo, con Docker y en Render.

## Estructura

```
economia-efectiva-django/
├── manage.py
├── economia_efectiva/      # configuración de Django (settings, urls, wsgi)
├── web/
│   ├── templates/web/index.html   # la página
│   ├── static/web/logo.jpg        # logo
│   ├── views.py                   # inicio, /contacto/ y /salud/
│   └── urls.py
├── Dockerfile              # imagen para Docker y para Render
├── docker-compose.yml      # prueba local con Docker (puerto 8000)

├── render.yaml             # configuración de Render (con Docker)
├── build.sh                # alternativa: Render sin Docker (Python)
├── requirements.txt
├── .env.example
└── README.md
```

## A. Con Django directo (Linux)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
DEBUG=1 python manage.py runserver
```

Abre http://127.0.0.1:8000

## B. Con Docker

Instala Docker si no lo tienes:

```bash
sudo apt install -y docker.io docker-compose-v2
sudo usermod -aG docker $USER
```

Cierra la sesión y vuelve a entrar. Luego, en la carpeta del proyecto:

```bash
cp .env.example .env      # opcional: edita SECRET_KEY y las claves de correo
docker compose up -d --build
```

Abre http://localhost:8000

Comandos útiles:

```bash
docker compose logs -f     # ver registros (aquí salen los mensajes del formulario si no hay claves de correo)
docker compose down        # apagar
```

## C. Publicar en Render

1. Sube el proyecto a GitHub. Ejecuta `git init` dentro de esta carpeta:
   ```bash
   git init
   git add .
   git commit -m "Página Economía Efectiva"
   git branch -M main
   git remote add origin https://github.com/TU_USUARIO/TU_REPO.git
   git push -u origin main
   ```
2. En render.com entra a **New**, luego **Web Service**, y elige el repositorio. No uses *Static Site*.
3. Elige una de las dos formas:

   **Con Docker (recomendada, igual que en tu computador)**
   - **Language:** Docker (usa el `Dockerfile`)
   - **Instance type:** Free

   **Sin Docker (Python)**
   - **Language:** Python 3
   - **Build Command:** `./build.sh`
   - **Start Command:** `gunicorn economia_efectiva.wsgi:application`

4. En **Environment** agrega:
   - `SECRET_KEY`: un texto largo y aleatorio
   - `RESEND_API_KEY`: ver el punto D
5. Pulsa **Create Web Service**. El enlace queda como `https://economia-efectiva.onrender.com`.

Con `render.yaml` (Blueprint), Render toma todo esto automáticamente.

En el plan gratis el servicio se duerme tras unos 15 minutos sin visitas, y la primera visita después puede tardar cerca de un minuto.

## D. Que los mensajes lleguen al correo

El plan gratis de Render bloquea el correo por SMTP, así que el formulario envía por HTTPS con Resend:

1. Crea una cuenta en resend.com **con el correo economiaefectivasogamoso@gmail.com**.
2. En **API Keys** crea una clave y pégala como `RESEND_API_KEY`.
3. Con la cuenta gratis, Resend solo entrega al correo con el que te registraste. Para otros destinatarios hay que verificar un dominio propio.

Si el envío falla, el formulario abre el correo del cliente con el mensaje listo. Sin claves, los mensajes solo se imprimen en la terminal o en los registros de Docker.

## E. WhatsApp

Los botones abren el chat con el mensaje escrito y el cliente solo pulsa enviar. El envío automático por WhatsApp necesita WhatsApp Business API o Twilio, que son de pago.

## F. Dominio propio

En Render: **Settings**, luego **Custom Domains**. Agrega el dominio y crea el registro DNS que te indique. Añade en Environment `DOMINIOS=tudominio.com,www.tudominio.com`.

Si lo publicas en un servidor propio con HTTPS delante (por ejemplo Caddy o Nginx), agrega también `FORZAR_HTTPS=1`.

## Variables

| Variable | Para qué |
|---|---|
| `SECRET_KEY` | Clave de Django (obligatoria en producción) |
| `RESEND_API_KEY` | Envío de correo por HTTPS |
| `CONTACT_EMAIL` | Quién recibe los mensajes (por defecto economiaefectivasogamoso@gmail.com) |
| `DOMINIOS` | Dominios propios, separados por coma |
| `FORZAR_HTTPS` | `1` en servidor propio con HTTPS (en Render ya es automático) |
| `DEBUG` | `1` solo para pruebas locales con runserver |

## G. Integración continua (GitHub Actions)

El archivo `.github/workflows/ci.yml` corre en cada push a `main`, en cada pull request y a mano desde la pestaña **Actions**:

1. `build-check`: instala dependencias, `manage.py check`, `collectstatic` y prueba que `/` y `/salud/` respondan 200.
2. `docker-build`: construye el `Dockerfile` (el mismo de Render), arranca el contenedor y espera a que `/salud/` responda.

En Render, para desplegar solo si todo pasa: **Settings → Build & Deploy → Auto-Deploy → After CI Checks Pass**.
