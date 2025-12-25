# 🚀 Compete CTF - Production Deployment Guide

## Prerequisites

- Python 3.12+
- PostgreSQL 12+ or MySQL 8+
- Nginx or Apache web server
- SSL/TLS certificate (Let's Encrypt recommended)
- Domain name configured

## Step 1: Environment Setup

1. **Copy environment template:**
   ```bash
   cp Compete/.env.example Compete/.env
   ```

2. **Generate a new SECRET_KEY:**
   ```bash
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```

3. **Edit `.env` file with production values:**
   ```bash
   nano Compete/.env
   ```

   Required changes:
   - Set `SECRET_KEY` to the generated value
   - Set `DEBUG=False`
   - Set `ALLOWED_HOSTS` to your domain(s)
   - Set `USE_POSTGRESQL=True`
   - Configure database credentials
   - Set `USE_SMTP_EMAIL=True`
   - Configure email credentials
   - Enable security settings for HTTPS

## Step 2: Install Dependencies

```bash
cd /path/to/Compete
pip install -r requirements.txt
```

## Step 3: Database Setup

1. **Create PostgreSQL database:**
   ```sql
   CREATE DATABASE compete_db;
   CREATE USER compete_user WITH PASSWORD 'your-secure-password';
   ALTER ROLE compete_user SET client_encoding TO 'utf8';
   ALTER ROLE compete_user SET default_transaction_isolation TO 'read committed';
   ALTER ROLE compete_user SET timezone TO 'UTC';
   GRANT ALL PRIVILEGES ON DATABASE compete_db TO compete_user;
   ```

2. **Run migrations:**
   ```bash
   cd Compete
   python manage.py makemigrations
   python manage.py migrate
   ```

3. **Create superuser:**
   ```bash
   python manage.py createsuperuser
   ```

## Step 4: Collect Static Files

```bash
python manage.py collectstatic --noinput
```

## Step 5: Configure Gunicorn

1. **Create systemd service file** `/etc/systemd/system/compete.service`:
   ```ini
   [Unit]
   Description=Compete CTF Gunicorn daemon
   After=network.target

   [Service]
   User=www-data
   Group=www-data
   WorkingDirectory=/path/to/Compete/Compete
   Environment="DJANGO_SETTINGS_MODULE=Compete.production_settings"
   ExecStart=/path/to/venv/bin/gunicorn \
             --workers 3 \
             --bind unix:/run/compete.sock \
             Compete.wsgi:application

   [Install]
   WantedBy=multi-user.target
   ```

2. **Start and enable service:**
   ```bash
   sudo systemctl start compete
   sudo systemctl enable compete
   ```

## Step 6: Configure Nginx

1. **Create nginx configuration** `/etc/nginx/sites-available/compete`:
   ```nginx
   server {
       listen 80;
       server_name yourdomain.com www.yourdomain.com;
       return 301 https://$server_name$request_uri;
   }

   server {
       listen 443 ssl http2;
       server_name yourdomain.com www.yourdomain.com;

       ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
       ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

       ssl_protocols TLSv1.2 TLSv1.3;
       ssl_prefer_server_ciphers on;
       ssl_ciphers HIGH:!aNULL:!MD5;

       client_max_body_size 10M;

       location = /favicon.ico { access_log off; log_not_found off; }

       location /static/ {
           alias /path/to/Compete/Compete/staticfiles/;
           expires 30d;
           add_header Cache-Control "public, immutable";
       }

       location /media/ {
           alias /path/to/Compete/Compete/media/;
       }

       location / {
           include proxy_params;
           proxy_pass http://unix:/run/compete.sock;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
   }
   ```

2. **Enable site and restart nginx:**
   ```bash
   sudo ln -s /etc/nginx/sites-available/compete /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl restart nginx
   ```

## Step 7: SSL Certificate (Let's Encrypt)

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

## Step 8: Set Up Automated Backups

1. **Create backup script** `/usr/local/bin/backup-compete.sh`:
   ```bash
   #!/bin/bash
   DATE=$(date +%Y%m%d_%H%M%S)
   BACKUP_DIR="/backups/compete"
   mkdir -p $BACKUP_DIR

   # Backup database
   pg_dump -U compete_user compete_db | gzip > "$BACKUP_DIR/db_$DATE.sql.gz"

   # Backup media files
   tar -czf "$BACKUP_DIR/media_$DATE.tar.gz" /path/to/Compete/Compete/media/

   # Keep only last 7 days of backups
   find $BACKUP_DIR -name "db_*.sql.gz" -mtime +7 -delete
   find $BACKUP_DIR -name "media_*.tar.gz" -mtime +7 -delete
   ```

2. **Add to crontab** (daily at 2 AM):
   ```bash
   sudo crontab -e
   # Add:
   0 2 * * * /usr/local/bin/backup-compete.sh
   ```

## Step 9: Security Checklist

- [ ] SECRET_KEY is unique and secure
- [ ] DEBUG=False
- [ ] ALLOWED_HOSTS properly configured
- [ ] HTTPS enforced
- [ ] Database uses strong password
- [ ] Email credentials secured
- [ ] Firewall configured (UFW/iptables)
- [ ] SSH key-based authentication
- [ ] Fail2ban installed
- [ ] Regular updates scheduled

## Step 10: Monitoring

1. **Check logs:**
   ```bash
   # Application logs
   tail -f /path/to/Compete/Compete/logs/django_error.log

   # Nginx logs
   tail -f /var/log/nginx/error.log

   # Systemd service
   journalctl -u compete -f
   ```

2. **Install monitoring tools** (optional):
   - Sentry for error tracking
   - Uptime Robot for availability monitoring
   - New Relic or DataDog for performance monitoring

## Common Production Commands

```bash
# Restart application
sudo systemctl restart compete

# Check status
sudo systemctl status compete

# View logs
journalctl -u compete -n 50

# Run management commands
cd /path/to/Compete/Compete
python manage.py <command>

# Collect static files after updates
python manage.py collectstatic --noinput

# Run migrations after updates
python manage.py migrate

# Create database backup manually
/usr/local/bin/backup-compete.sh
```

## Troubleshooting

### Static files not loading
```bash
python manage.py collectstatic --clear --noinput
sudo systemctl restart compete
```

### Database connection errors
- Check PostgreSQL is running: `sudo systemctl status postgresql`
- Verify credentials in .env file
- Check PostgreSQL logs: `sudo tail -f /var/log/postgresql/postgresql-*.log`

### 502 Bad Gateway
- Check Gunicorn is running: `sudo systemctl status compete`
- Check socket file exists: `ls -la /run/compete.sock`
- Verify nginx configuration: `sudo nginx -t`

### Email not sending
- Verify SMTP credentials in .env
- Check firewall allows outbound port 587/465
- Test with: `python manage.py shell` then `from django.core.mail import send_mail`

## Performance Optimization

1. **Enable Redis caching** (optional):
   ```bash
   pip install redis django-redis
   ```

   Add to settings.py:
   ```python
   CACHES = {
       'default': {
           'BACKEND': 'django_redis.cache.RedisCache',
           'LOCATION': 'redis://127.0.0.1:6379/1',
       }
   }
   ```

2. **Increase Gunicorn workers** (based on CPU cores):
   ```bash
   # In /etc/systemd/system/compete.service
   --workers $(( 2 * $(nproc) + 1 ))
   ```

3. **Enable gzip compression** in Nginx (already in config above)

## Updates and Maintenance

```bash
# Pull latest code
cd /path/to/Compete
git pull

# Install new dependencies
pip install -r requirements.txt

# Run migrations
cd Compete
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Restart application
sudo systemctl restart compete
```

## Support

For issues or questions:
- Check logs first
- Review Django documentation
- Contact system administrator

---

**Important:** Always test changes in a staging environment before applying to production!
