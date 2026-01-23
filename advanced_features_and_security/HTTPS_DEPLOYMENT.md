# HTTPS Deployment Configuration

## Overview
This project enforces HTTPS to protect data transmitted between clients and the server.

## Django Configuration
The following settings are enabled in settings.py:
- SECURE_SSL_REDIRECT
- SESSION_COOKIE_SECURE
- CSRF_COOKIE_SECURE
- SECURE_HSTS_SECONDS
- SECURE_HSTS_INCLUDE_SUBDOMAINS
- SECURE_HSTS_PRELOAD

## Web Server Configuration (Nginx Example)

server {
    listen 443 ssl;
    server_name example.com;

    ssl_certificate /etc/ssl/certs/fullchain.pem;
    ssl_certificate_key /etc/ssl/private/privkey.pem;

    location / {
        proxy_pass http://127.0.0.1:8000;
    }
}

## SSL Certificates
Certificates can be obtained using Let's Encrypt via Certbot.

## Notes
All HTTP traffic is redirected to HTTPS to ensure secure communication.
