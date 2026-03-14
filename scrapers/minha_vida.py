import hashlib
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from config import MINHA_VIDA_URL

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}


def fetch() -> list[dict]:
    try:
        resp = requests.get(MINHA_VIDA_URL, headers=HEADERS, timeout=10)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        articles = []

        # Try common card/article selectors
        for tag in soup.find_all("a", href=True):
            href = tag["href"]
            if not href.startswith("http"):
                href = "https://www.minhavida.com.br" + href

            title_tag = tag.find(["h2", "h3", "h4", "span"])
            if not title_tag:
                continue
            title = title_tag.get_text(strip=True)
            if len(title) < 20:
                continue

            article_id = hashlib.md5(href.encode()).hexdigest()
            articles.append({
                "id": article_id,
                "title": title,
                "link": href,
                "summary": "",
                "published": "",
                "source": "Minha Vida",
                "ai_summary": None,
                "category": None,
                "fetched_at": datetime.utcnow().isoformat(),
            })

        # Deduplicate by id
        seen = set()
        unique = []
        for a in articles:
            if a["id"] not in seen:
                seen.add(a["id"])
                unique.append(a)

        return unique[:20]
    except Exception as e:
        print(f"[Minha Vida] scraping error: {e}")
        return []
