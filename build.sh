#!/usr/bin/env bash
set -o errexit

export DJANGO_SETTINGS_MODULE="${DJANGO_SETTINGS_MODULE:-config.settings.production}"

python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
python3 manage.py check
python3 manage.py collectstatic --no-input
python3 manage.py migrate --no-input
