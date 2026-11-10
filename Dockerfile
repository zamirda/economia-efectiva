# Dockerfile en la RAÍZ del repositorio (Render lo encuentra con la ruta por defecto ./Dockerfile).
# El proyecto Django vive en la carpeta economia-efectiva-django/.
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY economia-efectiva-django/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY economia-efectiva-django/ .

# Recopila los archivos estáticos (la clave aquí es solo temporal para el build)
RUN SECRET_KEY=clave-temporal-de-build python manage.py collectstatic --no-input

RUN useradd --create-home app && chown -R app /app
USER app

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD python -c "import os,urllib.request;urllib.request.urlopen('http://127.0.0.1:'+os.environ.get('PORT','8000')+'/salud/',timeout=3)" || exit 1

# Render define PORT automáticamente; en local se usa 8000
CMD ["sh", "-c", "gunicorn economia_efectiva.wsgi:application --bind 0.0.0.0:${PORT:-8000} --workers 2"]
