web: python3 manage.py migrate --no-input && python3 manage.py seed_portfolio && python3 manage.py ensure_admin && gunicorn config.wsgi:application --bind 0.0.0.0:$PORT
