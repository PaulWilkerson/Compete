"""
Production settings for Compete CTF
Use this file by setting DJANGO_SETTINGS_MODULE=Compete.production_settings
"""

from .settings import *

# Override development settings with production-safe values

# Security - Force HTTPS
DEBUG = False
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True

# Database - Must use PostgreSQL in production
if not config('USE_POSTGRESQL', default=False, cast=bool):
    raise ValueError(
        "Production environment must use PostgreSQL. "
        "Set USE_POSTGRESQL=True in your .env file and configure database credentials."
    )

# Email - Must use SMTP in production
if not config('USE_SMTP_EMAIL', default=False, cast=bool):
    raise ValueError(
        "Production environment must use SMTP email backend. "
        "Set USE_SMTP_EMAIL=True in your .env file and configure email credentials."
    )

# Security checks
if not config('SECRET_KEY', default='').startswith('your-secret'):
    pass  # Good - using a custom secret key
else:
    raise ValueError(
        "Production environment requires a secure SECRET_KEY. "
        "Generate one with: python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'"
    )

# Validate ALLOWED_HOSTS is properly configured
allowed_hosts = config('ALLOWED_HOSTS', default='', cast=Csv())
if not allowed_hosts or 'localhost' in allowed_hosts:
    raise ValueError(
        "Production environment requires proper ALLOWED_HOSTS configuration. "
        "Set ALLOWED_HOSTS in your .env file with your actual domain(s)."
    )

# Additional production settings
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Static files - ensure collectstatic has been run
if not os.path.exists(STATIC_ROOT):
    import warnings
    warnings.warn(
        f"STATIC_ROOT directory '{STATIC_ROOT}' does not exist. "
        "Run 'python manage.py collectstatic' before deploying."
    )

# Create logs directory if it doesn't exist
logs_dir = os.path.join(BASE_DIR, 'logs')
if not os.path.exists(logs_dir):
    os.makedirs(logs_dir)

print("=" * 60)
print("PRODUCTION SETTINGS LOADED")
print("=" * 60)
print(f"DEBUG: {DEBUG}")
print(f"ALLOWED_HOSTS: {ALLOWED_HOSTS}")
print(f"DATABASE: PostgreSQL")
print(f"EMAIL: SMTP")
print(f"HTTPS: Enforced")
print(f"STATIC_ROOT: {STATIC_ROOT}")
print("=" * 60)
