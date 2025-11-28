# scrapers/malt.py
import requests
from bs4 import BeautifulSoup
from utils import USER_AGENT, logger

BASE = "https://www.malt.it"

def search(query="flutter", location="Italia", page=1):
    # Template: Malt cambia spesso l'HTML. Adatta i selettori se serve.
    url = f"{BASE}/search?query={query}&location={location}"
    logger.debug("Malt URL: %s", url)
    r = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=15)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    results = []
    for card in soup.select(".profile-card, .search-result"):
        try:
            a = card.select_one("a")
            if not a:
                continue
            title = a.get_text(strip=True)
            href = a.get("href")
            job_id = href.split("/")[-1] if href else title[:40]
            desc = card.get_text(" ", strip=True)
            full_url = href if href and href.startswith("http") else (BASE + href if href else None)
            results.append({
                "id": f"malt-{job_id}",
                "title": title,
                "url": full_url,
                "desc": desc,
                "site": "malt"
            })
        except Exception as e:
            logger.exception("Errore parsing Malt: %s", e)
    return results
