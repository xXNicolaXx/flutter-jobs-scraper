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
    html = scraper.get(url).text
    soup = BeautifulSoup(html, "html.parser")
    jobs = []

    for card in soup.select("[data-jk]"):
        job_id = card.get("data-jk")
        
        # Selettore corretto trovato
        title_tag = card.select_one("h2.jobTitle span[title]")
        title = title_tag.get("title") if title_tag else "Senza titolo"
        
        url = "https://it.indeed.com/viewjob?jk=" + job_id
        
        jobs.append({
            "id": job_id,
            "title": title,
            "url": url,
            "desc": "",
            "site": "Indeed"
        })
    
    return jobs