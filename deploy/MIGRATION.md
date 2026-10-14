# Moving SeedBot onto the AP Alerts VM

This runbook moves SeedBot (Django site, Discord bot, Celery worker) off its own
GCP VM and onto the VM that already runs AP Alerts. Apache + mod_wsgi is replaced
by gunicorn behind the nginx that AP Alerts already uses.

| Piece | Old VM | New VM |
|---|---|---|
| Web server | Apache + mod_wsgi | nginx (shared) → gunicorn on `127.0.0.1:8000` (`seedbot-web`) |
| Celery | systemd | `seedbot-celery`, broker on host Redis `127.0.0.1:6379/0` |
| Discord bot | systemd | `seedbot-bot` |
| Redis | host | `redis-server` package on the host. AP Alerts' Redis is inside Docker and not published, so the two never meet. |
| App directory | (check) | `/srv/seedbot`, owned by user `seedbot` |
| TLS | Certbot (Apache) | Certbot webroot, cert included through `/etc/nginx/snippets/seedbot-tls.conf` |

Files in this folder:

- `systemd/seedbot-web.service`, `systemd/seedbot-celery.service`, `systemd/seedbot-bot.service`
- `nginx/seedbot.net.conf` (the site), `nginx/seedbot-tls-copied.conf` and `nginx/seedbot-tls-letsencrypt.conf` (the two cert snippets)

Shell variables used below; set them in your own terminal:

```bash
OLD_VM=<seedbot vm name>    OLD_ZONE=<its zone>
NEW_VM=<ap alerts vm name>  NEW_ZONE=<its zone>
NEW_IP=<ap alerts vm external IP>
```

The order matters in two places: **the old bot is stopped before the new one
starts** (two bots on one token both answer every command), and **the SQLite
file is copied after the old site and worker are stopped** (otherwise writes
made in between are lost).

---

## 0. A day ahead

1. **Lower the DNS TTL** of the `seedbot.net` and `www.seedbot.net` A records
   to 300 seconds, so the cutover propagates in minutes. Leave
   `ap-alerts.seedbot.net` alone; it already points at the AP Alerts VM.
2. **Check the AP Alerts VM has room.** AP Alerts' Compose limits reserve up to
   2.5 CPU and 4.5 GB, and seed rolls are CPU-heavy subprocesses.
   ```bash
   gcloud compute instances describe $NEW_VM --zone $NEW_ZONE --format='value(machineType)'
   ```
   Celery is capped at `--concurrency=2` in `seedbot-celery.service` for this reason.
3. **Find out how SeedBot reaches Firestore.** On the old VM:
   ```bash
   grep GOOGLE_APPLICATION_CREDENTIALS /path/to/seedbot/.env
   curl -s -H 'Metadata-Flavor: Google' \
     http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/email
   ```
   If `.env` sets `GOOGLE_APPLICATION_CREDENTIALS`, the key file moves with
   `data/` and nothing else is needed. If it does not, Firestore has been using
   the old VM's attached service account, and on the new VM it would silently use
   the AP Alerts VM's account instead. Fix it one of two ways before cutover:
   - create a key for the old VM's service account, put it in `/srv/seedbot/data/`
     and set `GOOGLE_APPLICATION_CREDENTIALS` in `.env` to its full path; or
   - grant the AP Alerts VM's service account `roles/datastore.user` in
     SeedBot's GCP project (and check the VM's access scopes allow it).

## 1. Inventory the old VM

On the old VM, collect what is not in git. Keep these for reference even where
the new VM uses its own versions.

```bash
cd /path/to/seedbot                       # the current BASE_DIR
python3 --version; .venv/bin/python --version
sudo cat /etc/apache2/sites-enabled/*     # vhost: note any extra Alias/redirects
systemctl list-units --type=service | grep -iE 'seed|celery|bot'
systemctl cat <bot unit> <celery unit>    # note the celery --pool / --concurrency
crontab -l; sudo crontab -l               # expect sync_to_bq and cleanup_seeds
openssl x509 -noout -subject -ext subjectAltName -enddate \
  -in /etc/letsencrypt/live/seedbot.net/fullchain.pem   # covers www? expiry?
```

If the Apache vhost does anything the nginx site does not (extra aliases,
redirects, headers), add it to `nginx/seedbot.net.conf` before going further.
If the old Celery unit uses a specific `--pool`, copy it into
`seedbot-celery.service`.

Package what moves. This first copy is for testing; the database is copied
again at cutover.

```bash
sqlite3 seeDBot.sqlite ".backup /tmp/seeDBot.sqlite"   # consistent copy while live
sudo cp -L /etc/letsencrypt/live/seedbot.net/fullchain.pem \
           /etc/letsencrypt/live/seedbot.net/privkey.pem /tmp/
sudo chown $USER /tmp/fullchain.pem /tmp/privkey.pem
tar czf /tmp/seedbot-files.tgz .env data/ff3.smc data/seedbot-metrics-*.json data/seeds
```

Then from your own machine, move them to the new VM:

```bash
for f in seedbot-files.tgz seeDBot.sqlite fullchain.pem privkey.pem; do
  gcloud compute scp $OLD_VM:/tmp/$f /tmp/ --zone $OLD_ZONE
  gcloud compute scp /tmp/$f $NEW_VM:/tmp/ --zone $NEW_ZONE
done
```

Delete `/tmp/privkey.pem` from both VMs and your machine once step 4 is done.

## 2. Prepare the new VM

```bash
sudo apt update
sudo apt install -y git python3-venv python3-dev build-essential sqlite3 redis-server
sudo useradd --system --no-create-home --home-dir /srv/seedbot --shell /usr/sbin/nologin seedbot
sudo usermod -aG seedbot www-data          # lets nginx read static/ and seeds
```

**Redis.** Debian's `redis-server` listens on `127.0.0.1:6379` only, which is
what `settings.py` defaults to. Confirm it is local-only and is not clashing
with Docker:

```bash
sudo ss -ltnp | grep 6379    # expect 127.0.0.1:6379 and [::1]:6379, owned by redis-server
redis-cli ping               # PONG
```

**Code and venv.** Debian 12 ships Python 3.11; SeedBot was developed on 3.10.
Try 3.11 first. If anything in the test pass (step 5) fails because of the
version, install 3.10 with pyenv and rebuild the venv with it.

```bash
sudo git clone --recurse-submodules https://github.com/wrjones104/seedbot2000.git /srv/seedbot
sudo chown -R seedbot:seedbot /srv/seedbot
sudo chmod 750 /srv/seedbot
sudo -u seedbot -H bash -c 'cd /srv/seedbot &&
  python3 -m venv .venv &&
  .venv/bin/pip install --upgrade pip &&
  .venv/bin/pip install -r requirements.txt'
```

**Restore files.**

```bash
sudo tar xzf /tmp/seedbot-files.tgz -C /srv/seedbot
sudo cp /tmp/seeDBot.sqlite /srv/seedbot/
sudo mkdir -p /srv/seedbot/logs /srv/seedbot/data/seeds
sudo chown -R seedbot:seedbot /srv/seedbot
sudo chmod 600 /srv/seedbot/.env /srv/seedbot/data/seedbot-metrics-*.json
```

Edit `/srv/seedbot/.env`: keep `ENVIRONMENT=prod`, and fix any path in it that
pointed at the old BASE_DIR (for example `GOOGLE_APPLICATION_CREDENTIALS`).
`CELERY_BROKER_URL` and `CELERY_RESULT_BACKEND` can be left unset.

**Migrate and collect static.**

```bash
sudo -u seedbot -H bash -c 'cd /srv/seedbot &&
  .venv/bin/python manage.py migrate &&
  .venv/bin/python manage.py collectstatic --noinput &&
  .venv/bin/python manage.py check --deploy'
```

`check --deploy` will print warnings about HSTS and secure cookies; those were
true on the old VM too and are not part of this move.

## 3. Start the web app and worker (not the bot)

```bash
sudo cp /srv/seedbot/deploy/systemd/seedbot-*.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now seedbot-web seedbot-celery
# Do NOT enable seedbot-bot yet.
curl -sI -H 'Host: seedbot.net' http://127.0.0.1:8000/ | head -1   # expect 200
journalctl -u seedbot-web -u seedbot-celery -n 50 --no-pager
```

## 4. Add the nginx site

Use the cert copied from the old VM for now; the real one is issued after DNS
moves (step 7).

```bash
sudo install -d -m 755 /var/www/letsencrypt
sudo install -d -m 700 /etc/ssl/seedbot-copied
sudo mv /tmp/fullchain.pem /tmp/privkey.pem /etc/ssl/seedbot-copied/
sudo cp /srv/seedbot/deploy/nginx/seedbot-tls-*.conf /etc/nginx/snippets/
sudo ln -sf /etc/nginx/snippets/seedbot-tls-copied.conf /etc/nginx/snippets/seedbot-tls.conf
sudo cp /srv/seedbot/deploy/nginx/seedbot.net.conf /etc/nginx/sites-available/seedbot.net
sudo ln -s /etc/nginx/sites-available/seedbot.net /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx   # reload also picks up www-data's new group
```

Check AP Alerts is unaffected:

```bash
curl -sI https://archipelagoalerts.com/ | head -1
curl -sI https://ap-alerts.seedbot.net/ | head -1
```

## 5. Test before touching DNS

On your own machine, add a hosts-file line so the browser reaches the new VM
while everyone else still uses the old one:

```
<NEW_IP>  seedbot.net www.seedbot.net
```

(`/etc/hosts` on macOS/Linux, `C:\Windows\System32\drivers\etc\hosts` on Windows.
Flush the browser's DNS cache or use a private window.)

Work through:

- [ ] Home page loads over HTTPS, and CSS/JS load (`/static/`).
- [ ] `http://seedbot.net` and `https://www.seedbot.net` both land on `https://seedbot.net`.
- [ ] Log in with Discord. A CSRF error or a Discord "invalid redirect_uri" here
      means the `X-Forwarded-Proto` handling is wrong.
- [ ] Roll a preset from the site. It should finish (Celery + Redis + the ROM + the
      randomizer submodules) and the zip download should work (`/media/`).
- [ ] Tune-Up upload of a ROM works (checks `client_max_body_size`).
- [ ] `https://seedbot.net/media/temp_roms/` returns 404.
- [ ] Anything that writes to Firestore or Sheets works.

Anything written during this test goes into the test copy of the database and
is replaced at cutover. Remove the hosts-file line when done.

## 6. Cutover

Pick a quiet time. The site is down from the moment the old services stop until
DNS reaches people (a few minutes with the 300s TTL).

**On the old VM, stop everything that writes, bot first:**

```bash
sudo systemctl disable --now <bot unit>
sudo systemctl disable --now <celery unit>
sudo systemctl stop apache2
crontab -e            # comment out the SeedBot entries so nothing writes later
cd /path/to/seedbot
sqlite3 seeDBot.sqlite ".backup /tmp/seeDBot.sqlite"
tar czf /tmp/seeds.tgz data/seeds
```

Copy both to the new VM (same `gcloud compute scp` loop as step 1, with
`seeDBot.sqlite` and `seeds.tgz`).

**On the new VM:**

```bash
sudo systemctl stop seedbot-web seedbot-celery
sudo cp /tmp/seeDBot.sqlite /srv/seedbot/seeDBot.sqlite
sudo tar xzf /tmp/seeds.tgz -C /srv/seedbot
sudo chown -R seedbot:seedbot /srv/seedbot/seeDBot.sqlite /srv/seedbot/data/seeds
sudo -u seedbot -H bash -c 'cd /srv/seedbot && .venv/bin/python manage.py migrate'
sudo systemctl start seedbot-web seedbot-celery
sudo systemctl enable --now seedbot-bot
journalctl -u seedbot-bot -f      # wait for it to log in to Discord
```

**Change DNS:** point the `seedbot.net` and `www.seedbot.net` A records at
`NEW_IP`. Do not touch `ap-alerts.seedbot.net`.

```bash
dig +short seedbot.net @8.8.8.8      # repeat until it shows NEW_IP
```

Quick check in Discord (run a roll command) and on the site.

## 7. Issue the certificate on the new VM

Once `dig` shows the new IP from outside:

```bash
sudo certbot certonly --webroot -w /var/www/letsencrypt \
  -d seedbot.net -d www.seedbot.net \
  --deploy-hook 'systemctl reload nginx'
sudo ln -sf /etc/nginx/snippets/seedbot-tls-letsencrypt.conf /etc/nginx/snippets/seedbot-tls.conf
sudo nginx -t && sudo systemctl reload nginx
sudo certbot renew --dry-run
sudo rm -r /etc/ssl/seedbot-copied /etc/nginx/snippets/seedbot-tls-copied.conf
```

## 8. Scheduled jobs

Recreate the old crontab entries for the `seedbot` user with the new paths,
for example:

```bash
sudo crontab -u seedbot -e
# 0 4 * * *  cd /srv/seedbot && .venv/bin/python manage.py cleanup_seeds
# 15 4 * * * cd /srv/seedbot && .venv/bin/python manage.py sync_to_bq
```

Use the schedules from the old crontab, not these examples.

## 9. Afterwards

- Raise the DNS TTL back up once everything has run cleanly for a day.
- Update `deploy/nginx/sites-enabled.conf` in the ap-tracker repo, which is a
  copy of everything in `/etc/nginx/sites-enabled/` on this VM and now needs the
  SeedBot site in it.
- Keep the old VM stopped (not deleted) for a week, then snapshot its disk and
  delete it.

## Rolling back

Until the old VM is deleted, rollback is:

1. On the new VM: `sudo systemctl disable --now seedbot-bot seedbot-celery seedbot-web`.
2. Copy `/srv/seedbot/seeDBot.sqlite` (via `.backup`) and `data/seeds` back to the old VM.
3. On the old VM: start Apache, Celery and the bot again, and restore the crontab.
4. Point the A records back at the old VM's IP.
