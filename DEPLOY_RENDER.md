# Deploying to Render

This project is configured for Render with Django, Gunicorn, WhiteNoise, and SQLite on a persistent disk.

For a short copy-paste checklist, see `RENDER_COPY_PASTE.md`.

## Prerequisites

- A GitHub repository containing this project.
- A Render account.
- The project should include these files:
  - `render.yaml`
  - `build.sh`
  - `Procfile`
  - `requirements.txt`
  - `config/settings/production.py`

## Important SQLite Note

Render's normal service filesystem is ephemeral. This project stores production SQLite data on a persistent disk mounted at:

```bash
/var/data
```

The production database file is:

```bash
/var/data/db.sqlite3
```

Because persistent disks are not available on Render's free web service plan, `render.yaml` uses:

```yaml
plan: starter
```

Do not change the service to the free plan unless you are okay with losing production database changes after restarts or deploys.

## Deploy With `render.yaml`

1. Push the project to GitHub.

2. Log in to Render.

3. Create a new Blueprint.

4. Select the GitHub repository for this project.

5. Render will read `render.yaml` and create the web service.

6. Confirm the generated settings:

```bash
DJANGO_SETTINGS_MODULE=config.settings.production
DEBUG=False
PYTHON_VERSION=3.12.3
ALLOWED_HOSTS=.onrender.com
CSRF_TRUSTED_ORIGINS=https://*.onrender.com
SQLITE_DATABASE_NAME=/var/data/db.sqlite3
MEDIA_ROOT=/var/data/media
```

7. Render will automatically generate `SECRET_KEY`.

8. Deploy the service.

## What Render Runs

During build, Render runs:

```bash
./build.sh
```

That script:

```bash
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
python3 manage.py check
python3 manage.py collectstatic --no-input
```

During startup, Render runs:

```bash
./start.sh
```

The startup script creates the SQLite/media directories, runs migrations, seeds starter data, optionally creates the admin user, and then starts Gunicorn. These runtime steps happen after the persistent disk is mounted. The seed command is idempotent and does not overwrite content you edit later in Django admin.

To create the admin user automatically on Render, add this secret environment variable in the Render dashboard:

```bash
DJANGO_SUPERUSER_PASSWORD=<your strong password>
```

`render.yaml` already sets:

```bash
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=admin@example.com
```

## Custom Domain

After adding a custom domain in Render, update these environment variables:

```bash
ALLOWED_HOSTS=.onrender.com,yourdomain.com,www.yourdomain.com
CSRF_TRUSTED_ORIGINS=https://*.onrender.com,https://yourdomain.com,https://www.yourdomain.com
```

Render automatically provides HTTPS certificates for configured custom domains.

## Admin User

After the first successful deploy, open the Render Shell and create a Django admin user:

```bash
python3 manage.py createsuperuser
```

Then visit:

```bash
https://your-render-url.onrender.com/admin/
```

## Local Production Check

Before pushing, you can run:

```bash
DJANGO_SETTINGS_MODULE=config.settings.production \
SECRET_KEY=local-production-check-secret-key-1234567890 \
ALLOWED_HOSTS=.onrender.com \
CSRF_TRUSTED_ORIGINS=https://*.onrender.com \
SECURE_SSL_REDIRECT=True \
SESSION_COOKIE_SECURE=True \
CSRF_COOKIE_SECURE=True \
SQLITE_DATABASE_NAME=/tmp/render-sqlite-check/db.sqlite3 \
MEDIA_ROOT=/tmp/render-sqlite-check/media \
.venv/bin/python manage.py check --deploy --fail-level ERROR
```

## Troubleshooting

If static files do not load:

- Confirm `whitenoise` is installed from `requirements.txt`.
- Confirm `config.settings.production` includes `WhiteNoiseMiddleware`.
- Redeploy after checking that `collectstatic` completed successfully.

If database changes disappear:

- Confirm the service is using a persistent disk.
- Confirm the disk mount path is `/var/data`.
- Confirm `SQLITE_DATABASE_NAME=/var/data/db.sqlite3`.
- Confirm the service is not using Render's free plan.

If CSRF errors appear after adding a domain:

- Add the exact `https://` domain to `CSRF_TRUSTED_ORIGINS`.
- Add the hostname to `ALLOWED_HOSTS`.

If deploy fails because `SECRET_KEY` is missing:

- Confirm Render generated `SECRET_KEY`, or add one manually in the service environment variables.
