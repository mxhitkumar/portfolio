# Render Copy-Paste Values

Use this file while deploying on Render. It contains the exact values to paste.

## Recommended: Blueprint Deploy

If you deploy using `render.yaml`, Render fills almost everything automatically.

Paste or confirm these values:

```txt
Blueprint file: render.yaml
Service name: portfolio
Runtime: Python
Plan: Starter
```

Add this secret environment variable manually in Render:

```txt
SECRET_KEY=<generate or paste a long random secret>
DJANGO_SUPERUSER_PASSWORD=S71PT@@nzah*ZznVrR8D
```

If Render does not generate `SECRET_KEY` automatically, the deploy will fail with:

```txt
ImproperlyConfigured: Set SECRET_KEY in the production environment.
```

## Manual Web Service Deploy

Use these values if you create a normal Web Service instead of a Blueprint.

### Service Settings

```txt
Name: portfolio
Runtime: Python
Branch: main
Plan: Starter
```

### Build Command

```bash
./build.sh
```

### Start Command

```bash
./start.sh
```

### Persistent Disk

Optional but recommended for real production data. Create a persistent disk only if your Render plan supports it:

```txt
Name: portfolio-data
Mount Path: /var/data
Size: 1 GB
```

If you do not create a persistent disk, use the default `data/` values below. The site will deploy, but SQLite/media changes can be lost when Render rebuilds or restarts the service.

### Environment Variables

Paste these environment variables:

```txt
DJANGO_SETTINGS_MODULE=config.settings.production
SECRET_KEY=CQCxCLr-xSdRcOTXRzBJWLKu-tYNwNg08OBo5oiJ1SQsvpXON4GWUYfGLpZmG0zinUs
DEBUG=False
PYTHON_VERSION=3.12.3
ALLOWED_HOSTS=.onrender.com
CSRF_TRUSTED_ORIGINS=https://*.onrender.com
SQLITE_DATABASE_NAME=data/db.sqlite3
MEDIA_ROOT=data/media
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=admin@example.com
DJANGO_SUPERUSER_PASSWORD=S71PT@@nzah*ZznVrR8D
```

You can generate one locally with:

```bash
python3 -c "import secrets; print(secrets.token_urlsafe(50))"
```

## After Deploy

Open your site:

```txt
https://your-render-service.onrender.com/
```

Open admin:

```txt
https://your-render-service.onrender.com/admin/
```

Admin login:

```txt
Username: admin
Password: S71PT@@nzah*ZznVrR8D
```

## Custom Domain Values

If you add a custom domain, update these:

```txt
ALLOWED_HOSTS=.onrender.com,yourdomain.com,www.yourdomain.com
CSRF_TRUSTED_ORIGINS=https://*.onrender.com,https://yourdomain.com,https://www.yourdomain.com
```

Replace `yourdomain.com` with your real domain.

## Paid Persistent Disk Values

Use these only after adding a Render persistent disk mounted at `/var/data`:

```txt
SQLITE_DATABASE_NAME=/var/data/db.sqlite3
MEDIA_ROOT=/var/data/media
```

If you use these values without a disk, Render will show:

```txt
mkdir: cannot create directory '/var/data': Permission denied
```
