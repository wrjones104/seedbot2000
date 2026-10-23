# Deploying SeedBot with nginx and gunicorn

How to set up SeedBot (Django site, Discord bot, Celery worker) on a Debian or
Ubuntu server, with nginx terminating TLS and gunicorn running Django. This is
an alternative to the Apache + mod_wsgi setup production uses today; nothing
here is needed to keep that running.

| Piece | How it runs |
|---|---|
| Web | nginx → gunicorn on `127.0.0.1:8000` (`seedbot-web`) |
| Celery | `seedbot-celery`, broker on Redis `127.0.0.1:6379/0` |
| Discord bot | `seedbot-bot` |
| Redis | `redis-server` package on the host |
| App directory | `/var/www/seedbot_project`, owned by user `seedbot` |
| Python | 3.12 in a uv venv |
| TLS | Certbot (webroot) |

Files in this folder:

- `systemd/seedbot-web.service`, `systemd/seedbot-celery.service`, `systemd/seedbot-bot.service`
- `nginx/seedbot.net-http.conf` (port 80: ACME challenges and the HTTPS redirect)
- `nginx/seedbot.net.conf` (port 443: the site)

## 1. Packages, user and Redis

```bash
sudo apt update
sudo apt install -y git build-essential sqlite3 redis-server nginx certbot curl
sudo useradd --system --no-create-home --home-dir /var/www/seedbot_project --shell /usr/sbin/nologin seedbot
sudo usermod -aG seedbot www-data          # lets nginx read static/ and seeds
```

The `redis-server` package listens on `127.0.0.1:6379` only, which is what
`settings.py` defaults to:

```bash
sudo ss -ltnp | grep 6379    # expect 127.0.0.1:6379 (and [::1]:6379)
redis-cli ping               # PONG
```

## 2. Code and venv

SeedBot runs on Python 3.12. Distro Pythons vary, so use uv to install 3.12.
uv and its Python go under `/usr/local/bin` and `/opt/uv` so they don't land
inside the app directory.

```bash
curl -LsSf https://astral.sh/uv/install.sh | sudo env UV_INSTALL_DIR=/usr/local/bin sh
sudo env UV_PYTHON_INSTALL_DIR=/opt/uv/python uv python install 3.12
sudo git clone --recurse-submodules https://github.com/wrjones104/seedbot2000.git /var/www/seedbot_project
sudo chown -R seedbot:seedbot /var/www/seedbot_project
sudo chmod 750 /var/www/seedbot_project
sudo -u seedbot -H env UV_PYTHON_INSTALL_DIR=/opt/uv/python UV_CACHE_DIR=/tmp/uv-cache-seedbot \
  bash -c 'cd /var/www/seedbot_project &&
  uv venv --python 3.12 .venv &&
  uv pip install --python .venv/bin/python -r requirements.txt'
/var/www/seedbot_project/.venv/bin/python --version   # expect 3.12.x
```

The randomizer forks are git submodules that the bot runs as subprocesses, so
`--recurse-submodules` is required.

## 3. Files that aren't in git

Put these in `/var/www/seedbot_project`:

- `.env` with `SECRET_KEY`, `DISCORD_TOKEN`, `new_api_key`, `dev_api_key`,
  `ENVIRONMENT=prod`, and `GOOGLE_APPLICATION_CREDENTIALS` (full path to the
  Firestore key). Optional: `SOTW_API_KEY`, `GTM_ID`, `PUBLIC_BASE_URL`,
  `FAILURE_WEBHOOK_URL` (a Discord webhook that failed rolls are reported to;
  unset means no reporting — see [Failure alerts](#failure-alerts)).
  **Add `TRUST_X_FORWARDED_PROTO=1`.** Behind nginx, Django sees plain HTTP
  from gunicorn; without this it can't tell requests were HTTPS, so every form
  POST fails the CSRF check and Discord login builds an `http://` callback.
- `seeDBot.sqlite` (or let `migrate` create an empty one).
- `data/ff3.smc`, the base ROM every roll needs.
- `data/seedbot-metrics-*.json` and the Firestore key named in `.env`.
- `data/seeds/`, existing seed zips if carrying them over.

To copy a live database, take a consistent snapshot rather than copying the
file: `sqlite3 seeDBot.sqlite ".backup /tmp/seeDBot.sqlite"`.

Then fix ownership and create the log directory (Django fails to start without it):

```bash
cd /var/www/seedbot_project
sudo mkdir -p logs data/seeds
sudo chown -R seedbot:seedbot .
sudo chmod 600 .env data/*.json
```

## 4. Migrate and collect static

```bash
sudo -u seedbot -H bash -c 'cd /var/www/seedbot_project &&
  .venv/bin/python manage.py migrate &&
  .venv/bin/python manage.py collectstatic --noinput &&
  .venv/bin/python manage.py check --deploy'
```

`check --deploy` warns about HSTS and secure cookies; those settings aren't
part of this setup.

## 5. Start the services

**Only one copy of the bot may run per `DISCORD_TOKEN`**: two copies both
answer every command. If SeedBot is running anywhere else, stop its bot before
enabling `seedbot-bot` here.

```bash
sudo cp /var/www/seedbot_project/deploy/systemd/seedbot-*.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now seedbot-web seedbot-celery
curl -sI -H 'Host: seedbot.net' http://127.0.0.1:8000/ | head -1   # expect 200
sudo systemctl enable --now seedbot-bot
journalctl -u seedbot-web -u seedbot-celery -u seedbot-bot -n 50 --no-pager
```

## 6. nginx and TLS

The `seedbot.net` and `www.seedbot.net` A records must point at this server
before Certbot can issue the certificate.

```bash
sudo install -d -m 755 /var/www/letsencrypt
sudo cp /var/www/seedbot_project/deploy/nginx/seedbot.net-http.conf /etc/nginx/sites-available/seedbot.net-http
sudo ln -s /etc/nginx/sites-available/seedbot.net-http /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx

sudo certbot certonly --webroot -w /var/www/letsencrypt \
  -d seedbot.net -d www.seedbot.net \
  --deploy-hook 'systemctl reload nginx'

sudo cp /var/www/seedbot_project/deploy/nginx/seedbot.net.conf /etc/nginx/sites-available/seedbot.net
sudo ln -s /etc/nginx/sites-available/seedbot.net /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx
sudo certbot renew --dry-run
```

What the site config does beyond proxying:

- `http://` and `www.` both redirect to `https://seedbot.net`.
- `/static/` is served from `staticfiles/`, and `/media/` from `data/seeds/`
  (Django only serves media when `DEBUG` is on).
- `/media/temp_roms/` returns 404. Tune-Up uploads wait there for Celery and
  must never be downloadable.
- `client_max_body_size 16m`, because nginx's 1 MB default rejects ROM uploads.

## 7. Check it

- [ ] Home page loads over HTTPS, and CSS/JS load.
- [ ] `http://seedbot.net` and `https://www.seedbot.net` land on `https://seedbot.net`.
- [ ] Log in with Discord. A CSRF error or a Discord "invalid redirect_uri"
      means `TRUST_X_FORWARDED_PROTO` isn't set.
- [ ] Roll a preset from the site; it finishes and the zip downloads.
- [ ] Tune-Up accepts a ROM upload.
- [ ] `https://seedbot.net/media/temp_roms/` returns 404.
- [ ] The bot answers a roll command in Discord.

## 8. Scheduled jobs

Run the maintenance commands from the `seedbot` user's crontab:

```bash
sudo crontab -u seedbot -e
# 0 4 * * *  cd /var/www/seedbot_project && .venv/bin/python manage.py cleanup_seeds
# 15 4 * * * cd /var/www/seedbot_project && .venv/bin/python manage.py sync_to_bq
```

Pick schedules to taste; these are examples.

## Failure alerts

When a roll fails, the bot posts it to a Discord webhook: the reference the
user was given, the command, who ran it and in which server, the fork and its
commit, the API's error and request ID, and the randomizer's last line, with
the full report attached.

To turn it on, make a webhook in the channel you want the reports in (channel
**Edit Channel → Integrations → Webhooks → New Webhook → Copy Webhook URL**),
then add it to `.env` and restart:

```bash
sudo -u seedbot tee -a /var/www/seedbot_project/.env <<'EOF'
FAILURE_WEBHOOK_URL=https://discord.com/api/webhooks/...
EOF
sudo systemctl restart seedbot-bot
```

Use a channel only staff can read: the attached report contains tracebacks and
server paths. Leaving `FAILURE_WEBHOOK_URL` unset disables reporting, and
nothing else about a failed roll changes.

Identical failures collapse into one post per minute, so an API outage
produces a handful of reports rather than one per roll. The post that goes out
says how many it stands for.

## Updating

```bash
cd /var/www/seedbot_project
sudo -u seedbot git pull --recurse-submodules
sudo -u seedbot -H env UV_PYTHON_INSTALL_DIR=/opt/uv/python UV_CACHE_DIR=/tmp/uv-cache-seedbot \
  uv pip install --python .venv/bin/python -r requirements.txt
sudo -u seedbot .venv/bin/python manage.py migrate
sudo -u seedbot .venv/bin/python manage.py collectstatic --noinput
sudo systemctl restart seedbot-web seedbot-celery seedbot-bot
```
