# Portfolio

Django portfolio site.

## Local Development

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
python3 manage.py migrate
python3 manage.py runserver
```

## Render Deployment

This project includes `render.yaml`, `build.sh`, `Procfile`, and production settings for Render.

1. Push the repository to GitHub.
2. In Render, create a new Blueprint and select this repository.
3. After Render creates the service, update these environment variables if you change the service name:
   - `ALLOWED_HOSTS`
   - `CSRF_TRUSTED_ORIGINS`

The build step installs dependencies, collects static files, and runs migrations.
