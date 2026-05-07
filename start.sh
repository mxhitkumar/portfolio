#!/usr/bin/env bash
set -o errexit

export DJANGO_SETTINGS_MODULE="${DJANGO_SETTINGS_MODULE:-config.settings.production}"
export PORT="${PORT:-8000}"
PYTHON_BIN="${PYTHON_BIN:-python3}"

echo "Starting portfolio service..."
echo "DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE}"
echo "SQLITE_DATABASE_NAME=${SQLITE_DATABASE_NAME:-db.sqlite3}"
echo "MEDIA_ROOT=${MEDIA_ROOT:-media}"

if [ -n "${SQLITE_DATABASE_NAME}" ]; then
  mkdir -p "$(dirname "${SQLITE_DATABASE_NAME}")"
fi

if [ -n "${MEDIA_ROOT}" ]; then
  mkdir -p "${MEDIA_ROOT}"
fi

echo "Running migrations..."
"${PYTHON_BIN}" manage.py migrate --no-input

echo "Seeding portfolio content..."
"${PYTHON_BIN}" manage.py seed_portfolio

echo "Ensuring admin user..."
"${PYTHON_BIN}" manage.py ensure_admin

echo "Starting Gunicorn..."
gunicorn config.wsgi:application --bind "0.0.0.0:${PORT}"
