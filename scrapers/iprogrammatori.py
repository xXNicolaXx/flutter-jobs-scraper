# scrapers/iprogrammatori.py
import requests
from bs4 import BeautifulSoup
from utils import USER_AGENT, logger

BASE = "https://www.iprogrammatori.it"

def search(query="flutter", page=1):
    # Iprogrammatori usa spesso search via parametro 's'
    url = f"{BASE}/lavoro/s/{query}"
    print(url);
    logger.debug("Iprogrammatori URL: %s", url)
    r = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=15)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    results = []
    
    # Selector corretto: le righe della tabella (senza tbody!)
    # La tabella ha direttamente i <tr> sotto <table>
    rows = soup.select("table.tablesaw tr")
    
    # Rimuovi l'header (primo tr è il thead)
    if rows:
        rows = rows[1:]  # Salta la prima riga (header)
    
    logger.debug(f"Iprogrammatori: trovati {len(rows)} annunci")
    
    for row in rows:
        try:
            # Le celle sono semplici <td> senza classi speciali
            cells = row.find_all("td")
            
            if len(cells) < 4:
                continue
            
            # Colonna 1: Data
            date = cells[0].get_text(strip=True)
            
            # Colonna 2: Azienda
            company = cells[1].get_text(strip=True)
            
            # Colonna 3: Titolo e link
            title_link = cells[2].find("a")
            if not title_link:
                continue
            
            title = title_link.get_text(strip=True)
            href = title_link.get("href")
            
            if not href:
                continue
            
            # Colonna 4: Location
            location = cells[3].get_text(strip=True)
            
            # Crea ID unico dall'URL
            job_id = href.split("_")[-1].replace(".aspx", "") if "_" in href else href.split("/")[-1]
            
            # Full URL
            full_url = href if href.startswith("http") else (BASE + href)
            
            # Componi titolo completo con azienda
            full_title = f"{title} @ {company}" if company else title
            
            # Componi descrizione
            desc_parts = []
            if date:
                desc_parts.append(f"Data: {date}")
            if location:
                desc_parts.append(f"Luogo: {location}")
            desc = " | ".join(desc_parts)
            
            results.append({
                "id": f"iprogrammatori-{job_id}",
                "title": full_title,
                "url": full_url,
                "desc": desc,
                "site": "Iprogrammatori"
            })
            
        except Exception as e:
            logger.exception("Errore parsing iprogrammatori row: %s", e)
            continue
    
    return results

if __name__ == "__main__":
    print("Testing Iprogrammatori...\n")
    results = search("flutter", 1)
    print(f"Trovati {len(results)} risultati\n")
    
    for r in results[:5]:
        print(f"  ✓ {r['title']}")
        print(f"    {r['url']}")
        print(f"    {r['desc']}\n")