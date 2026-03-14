from config import RSS_FEEDS
from scrapers.base import parse_rss_feed


def fetch() -> list[dict]:
    return parse_rss_feed(RSS_FEEDS["folha"], "Folha")
