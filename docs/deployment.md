# Deployment guide

This guide covers local development and production deployment for Kamate Marketing Studio.

## Local development

### Windows (Git Bash / PowerShell)

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

Use `127.0.0.1:8018` when testing from the local browser on the same machine.

### Linux

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

## Production deployment

### 1. Prepare the Linux server

Create a deployment directory and install Python, pip, Nginx, and Certbot if required.

```bash
sudo apt update
sudo apt install python3 python3-venv python3-pip nginx certbot python3-certbot-nginx -y
```

The example commands assume a typical Ubuntu/Debian VPS. Adapt the commands to the actual server environment.

### 2. Clone or copy the project

```bash
sudo mkdir -p /var/www/marketing-kamate
sudo chown $USER:$USER /var/www/marketing-kamate
cd /var/www/marketing-kamate
git clone <your-repository-url> .
```

If you are deploying a copied working tree, make sure the repository root contains the Django project files and `.env.example`.

### 3. Create a virtual environment and install dependencies

```bash
cd /var/www/marketing-kamate
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
cp .env.example .env
```

Edit `.env` to set production values:

```env
SECRET_KEY=generate-a-long-random-production-secret-key
DEBUG=False
ALLOWED_HOSTS=marketing.kamategroup.online,localhost,127.0.0.1
CSRF_TRUSTED_ORIGINS=https://marketing.kamategroup.online
```

### 4. Run Django checks and collect static files

```bash
source .venv/bin/activate
cd /var/www/marketing-kamate
python manage.py check --deploy
python manage.py collectstatic --noinput
```

This will generate files in `staticfiles/`.

### 5. Test Gunicorn locally before Nginx

```bash
source .venv/bin/activate
cd /var/www/marketing-kamate
gunicorn config.wsgi:application --bind 127.0.0.1:8018 --workers 3
```

Verify the site responds:

```bash
curl -I http://127.0.0.1:8018/
curl -I http://127.0.0.1:8018/health/
```

### 6. Create a systemd service

Example service file:

```ini
[Unit]
Description=Kamate Marketing Studio Gunicorn service
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/marketing-kamate
Environment="PATH=/var/www/marketing-kamate/.venv/bin"
ExecStart=/var/www/marketing-kamate/.venv/bin/gunicorn config.wsgi:application --bind 127.0.0.1:8018 --workers 3
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

Save as `/etc/systemd/system/kamate-marketing-studio.service` and enable it:

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now kamate-marketing-studio
sudo systemctl status kamate-marketing-studio
```

Monitor logs with:

```bash
sudo journalctl -u kamate-marketing-studio -f
```

### 7. Configure Nginx

Example server block for the production subdomain:

```nginx
server {
    listen 80;
    server_name marketing.kamategroup.online;

    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl http2;
    server_name marketing.kamategroup.online;

    ssl_certificate /etc/letsencrypt/live/marketing.kamategroup.online/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/marketing.kamategroup.online/privkey.pem;

    location /static/ {
        alias /var/www/marketing-kamate/staticfiles/;
        expires 30d;
        access_log off;
    }

    location / {
        proxy_pass http://127.0.0.1:8018;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

Save the file in `/etc/nginx/sites-available/marketing.kamategroup.online` and enable it:

```bash
sudo ln -s /etc/nginx/sites-available/marketing.kamategroup.online /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

Do not overwrite an existing Nginx config unless you are sure it is safe to do so. Check current site configuration before touching an active server block.

### 8. HTTPS and TLS

For a valid certificate, use Certbot if the domain is already pointed at the server:

```bash
sudo certbot --nginx -d marketing.kamategroup.online
```

If the certificate is already valid, verify it with:

```bash
sudo certbot certificates
```

The production site should respond to HTTPS on `https://marketing.kamategroup.online`.

### 9. DNS and verification

The DNS record for the subdomain has already been created and pointed to the server, so do not create it again. Verify the DNS record with:

```bash
nslookup marketing.kamategroup.online
```

or:

```bash
getent hosts marketing.kamategroup.online
```

Confirm that Nginx is serving the correct site and that the TLS certificate matches:

```bash
curl -I https://marketing.kamategroup.online/
curl -I https://marketing.kamategroup.online/health/
nginx -t
```

### 10. Firewall and server hardening

Typical hardening considerations include:

- allow only the necessary TCP ports (80 and 443 for web traffic)
- keep the operating system patched
- restrict SSH access to trusted IP addresses
- maintain log rotation
- avoid exposing the Django development server directly to the internet

Example UFW commands:

```bash
sudo ufw allow OpenSSH
sudo ufw allow 'Nginx Full'
sudo ufw enable
```

### 11. Troubleshooting

Common commands:

```bash
sudo systemctl status kamate-marketing-studio
sudo journalctl -u kamate-marketing-studio -n 100 --no-pager
sudo nginx -t
sudo systemctl reload nginx
curl -I http://127.0.0.1:8018/health/
```

Common issues:

- port 8018 is already in use: check with `ss -lntp | grep 8018`
- Nginx configuration error: run `sudo nginx -t`
- certificate missing: run `sudo certbot --nginx -d marketing.kamategroup.online`
- static files not loading: ensure `python manage.py collectstatic --noinput` has been run and the Nginx `alias` points to the correct directory

## Notes

- This implementation intentionally avoids a database for the initial public homepage.
- The Django configuration uses a dummy database backend to prevent accidental SQLite defaulting.
- A real database and authentication system should be added only when application logic requires it.
