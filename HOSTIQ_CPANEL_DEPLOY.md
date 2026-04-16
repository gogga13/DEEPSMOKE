# Deploy to HostiQ cPanel

This project is prepared for `Setup Python App` in cPanel and follows the HostiQ guide:

- HostiQ Wiki: https://hostiq.ua/wiki/ukr/cpanel-django/

## Project layout for cPanel

- Application root: `app`
- Startup file: `passenger_wsgi.py`
- WSGI module used by Passenger: `app.wsgi`

## What was prepared in code

- Added `app/passenger_wsgi.py` for Passenger/cPanel startup.
- Switched `STATIC_URL` to `/static/` for production-safe static URLs.
- Moved collected static output to `app/static` so cPanel/Apache can serve `/static/` directly.
- Removed duplicate static discovery from Django settings so `collectstatic` can run cleanly.
- Added production safeguards in Django settings:
  - production now requires a real `DJANGO_SECRET_KEY`
  - production now requires `DJANGO_ALLOWED_HOSTS`

## Upload steps in cPanel

1. Upload the repository contents to your domain directory.
2. In `Setup Python App`, create a Python application.
3. Set:
   - Application root: `app`
   - Application URL: your real domain
   - Application startup file: `passenger_wsgi.py`
4. Save the application.

## Environment file

Use the production template from the repo root:

1. Copy `.env.production.example` to `.env`
2. Fill in real values:
   - `DJANGO_SECRET_KEY`
   - `DJANGO_ALLOWED_HOSTS`
   - `DJANGO_CSRF_TRUSTED_ORIGINS`
   - email credentials if you want real email sending
   - Telegram/Nova Poshta keys if needed

Minimum example:

```env
DJANGO_SECRET_KEY=put-a-long-random-secret-here
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=your-domain.com,www.your-domain.com
DJANGO_CSRF_TRUSTED_ORIGINS=https://your-domain.com,https://www.your-domain.com
DJANGO_SECURE_SSL_REDIRECT=True
```

## Install dependencies

For cPanel `Setup Python App`, use the file inside the application root:

- `app/requirements.txt`

It points to the main repo dependencies automatically.

If you use the terminal instead, first enter the virtualenv shown by cPanel, then run:

```bash
pip install -r ~/your-domain/app/requirements.txt
```

Adjust the path to your real cPanel home directory.

## Django commands after upload

Run inside the `app` directory:

```bash
python manage.py migrate
python manage.py collectstatic --noinput
```

Then press `Restart` in `Setup Python App`.

## Important note about the database

The project currently uses SQLite by default:

- database file: `app/db.sqlite3`

This is acceptable for a small site, but for long-term production it is better to move to MySQL in cPanel.

## If the site shows 500/503

Check:

- `app/stderr.log` if cPanel created it
- Python application error log in cPanel

Common causes:

- missing dependency
- invalid `DJANGO_SECRET_KEY`
- empty or wrong `DJANGO_ALLOWED_HOSTS`
- wrong `DJANGO_CSRF_TRUSTED_ORIGINS`
- static files were not collected

## Recommended first launch checklist

- `DJANGO_DEBUG=False`
- real secret key set
- domain added to `DJANGO_ALLOWED_HOSTS`
- HTTPS origins added to `DJANGO_CSRF_TRUSTED_ORIGINS`
- `migrate` completed
- `collectstatic` completed
- app restarted in cPanel
