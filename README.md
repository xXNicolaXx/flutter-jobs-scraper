# Flutter jobs scraper (Italia) - Minimal

Script Python che cerca annunci Flutter in Italia su vari siti e invia notifiche via Telegram. Pensato per girare su DigitalOcean (Droplet) con crontab ogni 6 ore.

## Setup rapido (in droplet)

1. Copia repository in `/root/flutter-jobs-scraper`
2. Copia `.env.template` → `.env` e inserisci `TELEGRAM_BOT_TOKEN` e `TELEGRAM_CHAT_ID`.
3. Rendi eseguibili gli script:
   ```bash
   chmod +x deploy.sh run.sh
   ```
