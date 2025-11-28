from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

def search_indeed(keyword, location, page=0):
    url = f"https://it.indeed.com/jobs?q={keyword}&l={location}&start={page*10}"
    print(f"[DEBUG] Indeed URL: {url}")

    jobs = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # headless=True su server
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/118.0.0.0 Safari/537.36"
        )
        page_obj = context.new_page()
        page_obj.goto(url, timeout=30000)
        
        # Attendi che i risultati siano caricati
        try:
            page_obj.wait_for_selector('[data-jk]', timeout=15000)
        except:
            print("[DEBUG] Timeout o blocco Cloudflare")
            page_obj.screenshot(path="blocked.png")
            with open("blocked.html", "w", encoding="utf-8") as f:
                f.write(page_obj.content())
            browser.close()
            return []

        # Salva screenshot e HTML per debug
        page_obj.screenshot(path="indeed_debug.png")
        with open("indeed_debug.html", "w", encoding="utf-8") as f:
            f.write(page_obj.content())

        soup = BeautifulSoup(page_obj.content(), "html.parser")
        cards = soup.select("[data-jk]")
        print(f"[DEBUG] Trovati {len(cards)} card con [data-jk]")

        for card in cards:
            job_id = card.get("data-jk")
            title_tag = card.select_one("h2 span[title]") or card.select_one("h2 span")
            title = title_tag.get("title") if title_tag and title_tag.get("title") else (title_tag.text.strip() if title_tag else "Senza titolo")
            job_url = f"https://it.indeed.com/viewjob?jk={job_id}"
            jobs.append({
                "id": job_id,
                "title": title,
                "url": job_url,
                "desc": "",
                "site": "Indeed"
            })
        
        browser.close()

    return jobs


if __name__ == "__main__":
    results = search_indeed("flutter", "Italia", page=0)
    print(f"Trovati {len(results)} risultati")
    for r in results[:5]:
        print(f"- {r['title']} | {r['url']}")
