import cloudscraper
from bs4 import BeautifulSoup

scraper = cloudscraper.create_scraper(
    browser={
        "browser": "chrome",
        "platform": "linux",
        "mobile": False
    }
)


def search(keyword, location, page=0):
    url = f"https://it.indeed.com/jobs?q={keyword}&l={location}&start={page*10}"
    print(f"[DEBUG] Indeed URL: {url}")
    
    html = scraper.get(url).text
    with open("debug_indeed.html", "w") as f:
        f.write(html)
        print("Salvato debug_indeed.html con la risposta Indeed")
    soup = BeautifulSoup(html, "html.parser")
    
    # Salva l'HTML per debug (opzionale)
    # with open("indeed_debug.html", "w", encoding="utf-8") as f:
    #     f.write(html)
    
    jobs = []
    
    # Prova diversi selettori comuni per Indeed
    cards = soup.select("[data-jk]")
    print(f"[DEBUG] Trovati {len(cards)} card con [data-jk]")
    
    for card in cards:
        job_id = card.get("data-jk")
        
        # Prova diversi selettori per il titolo
        title = None
        title_selectors = [
            "h2.jobTitle span[title]",  # Nuovo formato
            "h2 span[title]",
            "h2 a span",
            ".jobTitle span",
            "h2.jobTitle",
            "h2 a"
        ]
        
        for selector in title_selectors:
            title_tag = card.select_one(selector)
            if title_tag:
                # Prova prima l'attributo title, poi il testo
                title = title_tag.get("title") or title_tag.text.strip()
                if title:
                    print(f"[DEBUG] Titolo trovato con selector '{selector}': {title}")
                    break
        
        if not title:
            title = "Senza titolo"
            print(f"[DEBUG] Nessun titolo trovato per job_id: {job_id}")
            # Stampa l'HTML del card per debug
            print(f"[DEBUG] HTML card:\n{card.prettify()[:500]}")
        
        url = "https://it.indeed.com/viewjob?jk=" + job_id
        
        jobs.append({
            "id": job_id,
            "title": title,
            "url": url,
            "desc": "",
            "site": "Indeed"
        })
    
    return jobs


# Test diretto
if __name__ == "__main__":
    print("Testing Indeed scraper...")
    results = search("flutter", "Italia", page=0)
    print(f"\nTrovati {len(results)} risultati")
    for job in results[:3]:
        print(f"- {job['title']} | {job['url']}")