import os
from scrapfly import ScrapflyClient, ScrapeConfig
from bs4 import BeautifulSoup

API_KEY = os.getenv("SCRAPFLY_API_KEY")
client = ScrapflyClient(key=API_KEY)

def search_indeed(keyword, location, page=0):
    url = f"https://it.indeed.com/jobs?q={keyword}&l={location}&start={page*10}"
    print(f"[DEBUG] Indeed URL: {url}")

    result = client.scrape(ScrapeConfig(
        url=url,
        asp=True,  # Anti Scraping Protection
        render_js=True,  # necessario se i job sono caricati via JS
    ))

    html = result.content
    soup = BeautifulSoup(html, "html.parser")
    jobs = []

    for card in soup.select("[data-jk]"):
        job_id = card.get("data-jk")
        title_tag = card.select_one("h2 span[title]") or card.select_one("h2 span")
        title = title_tag.get("title") if title_tag and title_tag.get("title") else (title_tag.text.strip() if title_tag else "Senza titolo")
        jobs.append({
            "id": job_id,
            "title": title,
            "url": f"https://it.indeed.com/viewjob?jk={job_id}",
            "desc": "",
            "site": "Indeed"
        })

    return jobs

# Test
if __name__ == "__main__":
    results = search_indeed("flutter", "Italia")
    print(f"Trovati {len(results)} risultati")
    for r in results[:5]:
        print(f"- {r['title']} | {r['url']}")
