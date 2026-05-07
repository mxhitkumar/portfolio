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

To populate a fresh database with starter portfolio content:

```bash
python3 manage.py seed_portfolio
```

## Render Deployment

This project includes `render.yaml`, `build.sh`, `Procfile`, and production settings for Render.

See [DEPLOY_RENDER.md](DEPLOY_RENDER.md) for the full deployment checklist.
For exact Render values to paste, see [RENDER_COPY_PASTE.md](RENDER_COPY_PASTE.md).

1. Push the repository to GitHub.
2. In Render, create a new Blueprint and select this repository.
3. Render will use `render.yaml`, generate `SECRET_KEY`, and attach a persistent disk for SQLite.

The build step installs dependencies, checks the Django project, and collects static files. The start command runs migrations against the SQLite database on the mounted disk before starting Gunicorn.

Important production environment variables:

```bash
DJANGO_SETTINGS_MODULE=config.settings.production
DEBUG=False
ALLOWED_HOSTS=.onrender.com
CSRF_TRUSTED_ORIGINS=https://*.onrender.com
SQLITE_DATABASE_NAME=/var/data/db.sqlite3
```

For a custom domain, add the domain to `ALLOWED_HOSTS` and add its `https://` origin to `CSRF_TRUSTED_ORIGINS` in Render.

SQLite data is stored under Render's persistent disk mount at `/var/data`. Do not use the free Render instance type for this setup unless you are okay with data loss, because Render's default filesystem is ephemeral without a persistent disk.
