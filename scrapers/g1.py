from config import RSS_FEEDS
from scrapers.base import parse_rss_feed


def fetch() -> list[dict]:
    articles = parse_rss_feed(RSS_FEEDS["g1_saude"], "G1")
    articles += parse_rss_feed(RSS_FEEDS["g1_ciencia"], "G1")
    # Deduplicate by id
    seen, unique = set(), []
    for a in articles:
        if a["id"] not in seen:
            seen.add(a["id"])
            unique.append(a)
    return unique
