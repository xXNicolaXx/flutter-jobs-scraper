import os
from scrapfly import ScrapflyClient, ScrapeConfig
from bs4 import BeautifulSoup
from dotenv import load_dotenv
load_dotenv()
# Inizializza Scrapfly con la tua API key dal .env
API_KEY = os.getenv("SCRAPFLY_API_KEY")
client = ScrapflyClient(key=API_KEY)

def search(keyword, location, page=0):
    url = f"https://it.indeed.com/jobs?q={keyword}&l={location}&start={page*10}"
    print(f"[DEBUG] Indeed URL: {url}")

    # Richiesta via Scrapfly
    result = client.scrape(ScrapeConfig(
        url=url,
        asp=True,        # Anti Scraping Protection
        render_js=True,  # Se i job sono caricati via JavaScript
    ))

    html = result.content
    soup = BeautifulSoup(html, "html.parser")
    jobs = []

    for card in soup.select("[data-jk]"):
        job_id = card.get("data-jk")

        # Prova a prendere il titolo corretto
        title_tag = card.select_one("h2.jobTitle span[title]") or card.select_one("h2 span")
        title = title_tag.get("title") if title_tag and title_tag.get("title") else (title_tag.text.strip() if title_tag else "Senza titolo")

        job_url = f"https://it.indeed.com/viewjob?jk={job_id}"

        jobs.append({
            "id": job_id,
            "title": title,
            "url": job_url,
            "desc": "",
            "site": "Indeed"
        })

    return jobs

# Test rapido
if __name__ == "__main__":
    results = search("flutter", "Italia")
    print(f"Trovati {len(results)} risultati")
    for r in results[:5]:
        print(f"- {r['title']} | {r['url']}")
