import os
import sqlite3
from datetime import datetime
import logging
import requests
from dotenv import load_dotenv

load_dotenv()

DB_PATH = os.getenv("DB_PATH", "jobs.db")
USER_AGENT = os.getenv("USER_AGENT", "job-scraper/1.0")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

logger = logging.getLogger("job-scraper")
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
logger.setLevel(LOG_LEVEL)

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS jobs (
        id TEXT PRIMARY KEY,
        title TEXT,
        url TEXT,
        site TEXT,
        found_at TEXT
    )
    """)
    conn.commit()
    conn.close()
    logger.info("DB init at %s", DB_PATH)

def is_new_and_store(job_id, title, url, site):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id FROM jobs WHERE id = ?", (job_id,))
    if c.fetchone():
        conn.close()
        return False
    c.execute("INSERT INTO jobs (id, title, url, site, found_at) VALUES (?, ?, ?, ?, ?)",
              (job_id, title, url, site, datetime.now().isoformat()))
    conn.commit()
    conn.close()
    logger.info("Stored job %s from %s", job_id, site)
    return True

def send_telegram_message(text):
    """
    Invia messaggio Telegram con HTML (più affidabile per URL)
    """
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    
    if not token or not chat_id:
        logger.error("Telegram non configurato: imposta TELEGRAM_BOT_TOKEN e TELEGRAM_CHAT_ID in .env")
        return False
    
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    
    # Usa HTML invece di Markdown per evitare problemi con URL
    data = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML",  # Cambiato da Markdown a HTML
        "disable_web_page_preview": False
    }
    
    try:
        r = requests.post(url, data=data, timeout=15)
        r.raise_for_status()
        logger.info("Messaggio Telegram inviato")
        return True
    except Exception as e:
        logger.exception("Errore invio Telegram: %s", e)
        return False