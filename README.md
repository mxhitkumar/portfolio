# Portfolio

Django portfolio site.

## Local Development

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
cp .env.example .env
python3 manage.py migrate
python3 manage.py runserver
```

## Render Deployment

This project includes `render.yaml`, `build.sh`, `Procfile`, and production settings for Render.

1. Push the repository to GitHub.
2. In Render, create a new Blueprint and select this repository.
3. Render will use `render.yaml`, generate `SECRET_KEY`, and connect the included PostgreSQL database.

The build step installs dependencies, checks the Django project, collects static files, and runs migrations.

Important production environment variables:

```bash
DJANGO_SETTINGS_MODULE=config.settings.production
DEBUG=False
ALLOWED_HOSTS=.onrender.com
CSRF_TRUSTED_ORIGINS=https://*.onrender.com
DATABASE_URL=<Render PostgreSQL connection string>
```

For a custom domain, add the domain to `ALLOWED_HOSTS` and add its `https://` origin to `CSRF_TRUSTED_ORIGINS` in Render.
