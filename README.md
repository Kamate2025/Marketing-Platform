# Kamate Marketing Studio

Kamate Marketing Studio is the public marketing platform homepage for Kamate Group Ltd. It presents a premium, modern SaaS landing page for an AI-powered social media marketing and publishing platform intended for creators, businesses, NGOs, and marketing teams.

## Purpose

The current implementation provides the Django project foundation and a polished public homepage. It is designed for future expansion with AI content generation, campaign planning, social publishing workflows, and media organization features.

## Current scope

This version intentionally does not include:

- a real authentication system
- user accounts or login flows
- database-backed persistence
- AI integrations
- social media API integrations
- payment processing

The homepage communicates those planned capabilities without claiming they are already operational.

## Technology stack

- Python 3.12+
- Django 5.1.3
- Gunicorn
- python-dotenv
- HTML, CSS, and vanilla JavaScript

## Project structure

```text
MarketingKGLtd/
├── config/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── views.py
│   ├── asgi.py
│   └── wsgi.py
├── docs/
│   └── deployment.md
├── static/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── main.js
│   └── images/
├── templates/
│   ├── base.html
│   └── home.html
├── .env.example
├── .gitignore
├── manage.py
├── README.md
├── requirements.txt
└── staticfiles/
```

## Local setup

### Windows

```bash
cd /c/kd/Projects/MarketingKGLtd
python -m venv .venv
source .venv/Scripts/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
cp .env.example .env
python manage.py check
python manage.py runserver 0.0.0.0:8018
```

### Linux or macOS

```bash
cd /path/to/MarketingKGLtd
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
cp .env.example .env
python manage.py check
python manage.py runserver 0.0.0.0:8018
```

## Environment configuration

Copy the example environment file and adjust the values:

```bash
cp .env.example .env
```

Recommended values:

```env
SECRET_KEY=replace-with-a-long-random-secret-string
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,[::1]
CSRF_TRUSTED_ORIGINS=http://localhost:8018,http://127.0.0.1:8018,https://marketing.kamategroup.online
```

Generate a secure Django secret key with:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

## Run the site locally

Start the development server:

```bash
python manage.py runserver 0.0.0.0:8018
```

Open:

- http://127.0.0.1:8018/
- http://127.0.0.1:8018/health/

## Static files

Static files are configured in `static/` and collected into `staticfiles/` for production. The project uses Django's staticfiles app and keeps the source and collection directories separate.

## Production overview

For production, the app should run behind Nginx using Gunicorn on `127.0.0.1:8018`. Static files are served by Nginx, while Gunicorn handles the Django WSGI application. Detailed instructions are available in [docs/deployment.md](docs/deployment.md).

## Deployment notes

- This project intentionally does not use a database in the initial version.
- The Django settings explicitly configure a dummy database backend so that the app does not silently default to SQLite.
- Production deployment should set `DEBUG=False`, configure `ALLOWED_HOSTS`, and use a secure `SECRET_KEY`.
- Login and sign-up actions remain placeholder links until real authentication and user flows are implemented.

## Current limitations

This is a public marketing landing page and project foundation, not a full SaaS platform. The current implementation is intentionally limited to secure, maintainable Django basics and a polished homepage experience.
