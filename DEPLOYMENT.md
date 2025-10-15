# Deployment Guide

## Admin UI Configuration

The admin UI is designed to be served at an obscure subdomain (e.g., `salt.gair.dev`) with multiple layers of security.

### Architecture

- **Backend**: Binds to `127.0.0.1:8001` (localhost only, not accessible externally)
- **Reverse Proxy**: Nginx or similar terminates TLS and adds security layers
- **Security Layers**:
  1. Basic Auth at reverse proxy level
  2. Optional IP allowlist at reverse proxy level
  3. Session-based login with CSRF protection at application level
  4. HTTPOnly cookies with SameSite=Strict

### Nginx Configuration Example

```nginx
# Admin subdomain configuration
server {
    listen 443 ssl http2;
    server_name salt.gair.dev;

    # TLS configuration
    ssl_certificate /path/to/ssl/cert.pem;
    ssl_certificate_key /path/to/ssl/key.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    # Basic Authentication (first layer)
    auth_basic "Admin Area";
    auth_basic_user_file /etc/nginx/.htpasswd;

    # Optional: IP allowlist (second layer)
    # allow 203.0.113.0/24;  # Your office IP range
    # deny all;

    # Proxy to admin backend
    location / {
        proxy_pass http://127.0.0.1:8001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Security headers
        add_header X-Frame-Options "DENY" always;
        add_header X-Content-Type-Options "nosniff" always;
        add_header X-XSS-Protection "1; mode=block" always;
        add_header Referrer-Policy "no-referrer" always;
    }
}

# Redirect HTTP to HTTPS
server {
    listen 80;
    server_name salt.gair.dev;
    return 301 https://$server_name$request_uri;
}
```

### Creating Basic Auth Credentials

```bash
# Install htpasswd utility (if not installed)
sudo apt-get install apache2-utils

# Create password file
sudo htpasswd -c /etc/nginx/.htpasswd admin

# Add additional users (without -c flag)
sudo htpasswd /etc/nginx/.htpasswd anotheruser
```

### Application Configuration

Set environment variables in `.env`:

```env
ADMIN_TOKEN=your-secret-admin-token-here
ADMIN_USERNAME=admin
ADMIN_PASSWORD=your-secure-password-here
```

### Running the Admin Server

```bash
# Start the admin server (binds to 127.0.0.1:8001)
python main.py

# Or with systemd service
sudo systemctl start portfolio-admin
```

### Systemd Service Example

Create `/etc/systemd/system/portfolio-admin.service`:

```ini
[Unit]
Description=Portfolio Admin Backend
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/var/www/portfolio
Environment="PATH=/var/www/portfolio/venv/bin"
ExecStart=/var/www/portfolio/venv/bin/python main.py
Restart=on-failure
RestartSec=5s

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable portfolio-admin
sudo systemctl start portfolio-admin
```

### Security Best Practices

1. **Never expose port 8001** directly to the internet
2. **Use strong passwords** for both Basic Auth and application login
3. **Enable IP allowlist** if you have a static IP
4. **Monitor access logs** regularly
5. **Use HTTPS only** - no HTTP access
6. **Keep subdomain name obscure** (not "admin.gair.dev")
7. **Regular security updates** for all dependencies
8. **Enable fail2ban** for login attempt monitoring

### Robots.txt

The application automatically serves a robots.txt that disallows crawling of admin routes:

```
User-agent: *
Disallow: /admin/
Disallow: /admin-login/
Disallow: /admin-logout/
```

Admin pages also include `<meta name="robots" content="noindex, nofollow">` tags.

### Session Management

- Sessions are stored in-memory (use Redis for production with multiple servers)
- Session cookies are HTTPOnly and SameSite=Strict
- CSRF tokens are required for all state-changing operations
- Sessions expire after 24 hours of inactivity

### Monitoring

Monitor these logs for suspicious activity:
- Nginx access logs: `/var/log/nginx/access.log`
- Nginx error logs: `/var/log/nginx/error.log`
- Application logs: Check systemd journal with `journalctl -u portfolio-admin`

### Public Site

The public portfolio site runs on port 8000 and can be proxied normally:

```nginx
server {
    listen 443 ssl http2;
    server_name gair.dev www.gair.dev;

    ssl_certificate /path/to/ssl/cert.pem;
    ssl_certificate_key /path/to/ssl/key.pem;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```
