import cloudscraper
from bs4 import BeautifulSoup

scraper = cloudscraper.create_scraper(
    browser={
        "browser": "chrome",
        "platform": "darwin",
    }
)

def search(keyword, location, page=1):
    url = f"https://it.jooble.org/SearchResult?q={keyword}&l={location}&p={page}"

    html = scraper.get(url).text
    soup = BeautifulSoup(html, "html.parser")
    jobs = []

    for card in soup.select(".result-item"):
        title_el = card.select_one(".result-item__title")
        if not title_el:
            continue

        title = title_el.get_text(strip=True)
        href = title_el.get("href")

        if href and not href.startswith("http"):
            href = "https://it.jooble.org" + href

        jobs.append({
            "id": href,
            "title": title,
            "url": href,
            "desc": "",
            "site": "Jooble"
        })
    
    return jobs
