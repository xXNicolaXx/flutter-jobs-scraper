import os
import json
from datetime import datetime, timedelta
from scrapers import indeed, iprogrammatori
from utils import init_db, is_new_and_store, send_telegram_message, logger
from dotenv import load_dotenv
load_dotenv()

LAST_RUN_FILE = "last_run.json"

# -------------------------------
# FILTRO KEYWORD
# -------------------------------
def match_job(job, keywords):
    """
    Ritorna True se il job contiene almeno un keyword 
    nel titolo o descrizione.
    """
    text = (job.get("title", "") + " " + job.get("desc", "")).lower()
    return any(k.lower() in text for k in keywords)


# -------------------------------
# FILTRO FREELANCE
# -------------------------------
def is_valid_freelance(job):
    url = job.get("url", "").lower()

    # Esclude profili utenti, portfolio ecc.
    if "/profile/" in url or "/freelancer/" in url:
        return False

    # Deve contenere almeno una delle parole chiave
    text = (job.get("title", "") + " " + job.get("desc", "")).lower()
    must = ["freelance", "contract", "contratto", "incarico", "progetto", "project"]

    return any(m in text for m in must)


# -------------------------------
# MAIN
# -------------------------------

def load_last_run():
    if os.path.exists(LAST_RUN_FILE):
        with open(LAST_RUN_FILE, "r") as f:
            return json.load(f)
    return {}

def save_last_run(data):
    with open(LAST_RUN_FILE, "w") as f:
        json.dump(data, f)

def main():
    init_db()

    KEYWORDS = ["flutter", "dart", "mobile"]
    last_run = load_last_run()
    today = datetime.now()

    scrapers_config = [
        {"name": "Indeed", "func": indeed.search, "args": ("flutter", "Italia", 0), "interval_days": 3},
        {"name": "Iprogrammatori", "func": iprogrammatori.search, "args": ("flutter", 1), "interval_days": 0},
    ]

    all_jobs = []
    new_jobs = []

    for config in scrapers_config:
        scraper_name = config["name"]
        interval_days = config.get("interval_days", 0)

        # Controllo se lo scraper deve girare
        last_date_str = last_run.get(scraper_name)
        if last_date_str:
            last_date = datetime.fromisoformat(last_date_str)
            if interval_days > 0 and today < last_date + timedelta(days=interval_days):
                logger.info(f"{scraper_name}: saltato (ultima esecuzione {last_date.date()})")
                continue

        logger.info(f"========== Eseguendo scraper: {scraper_name} ==========")
        try:
            jobs = config["func"](*config["args"])
            logger.info(f"{scraper_name}: trovati {len(jobs)} annunci totali")

            if not jobs:
                logger.warning(f"{scraper_name}: Nessun risultato (controlla HTML selector)")

            # Filtro keyword
            jobs = [j for j in jobs if match_job(j, KEYWORDS)]
            logger.info(f"{scraper_name}: {len(jobs)} annunci dopo filtro keyword {KEYWORDS}")

            # Log & memorizzazione
            for job in jobs:
                logger.info(f"  -> [{job['site']}] {job['title'][:60]} | {job['url']}")
                all_jobs.append(job)
                if is_new_and_store(job["id"], job["title"], job["url"], job["site"]):
                    new_jobs.append(job)
                    logger.info("  ✓ NUOVO annuncio salvato")
                else:
                    logger.debug("  - Annuncio già visto")

            # Aggiorna data ultima esecuzione
            last_run[scraper_name] = today.isoformat()

        except Exception as e:
            logger.exception(f"Errore durante scraping di {scraper_name}: {e}")

    # Salva le ultime esecuzioni
    save_last_run(last_run)

    # Riepilogo
    logger.info("\n========== RIEPILOGO ==========")
    logger.info(f"Totale annunci trovati: {len(all_jobs)}")
    logger.info(f"Nuovi annunci: {len(new_jobs)}")

    # Telegram
    if new_jobs:
        msg = f"🔔 <b>Nuovi annunci Flutter</b> ({len(new_jobs)})\n\n"
        for job in new_jobs:
            title = job['title'].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            site = job['site'].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            msg += (
                f"📌 <b>{title}</b>\n"
                f"🌐 {site}\n"
                f"🔗 <a href=\"{job['url']}\">Apri annuncio</a>\n\n"
            )
        send_telegram_message(msg)
    else:
        logger.info(f"Nessun nuovo annuncio trovato ({today.isoformat()})")


if __name__ == "__main__":
    main()
