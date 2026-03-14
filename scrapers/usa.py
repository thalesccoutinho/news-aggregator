from __future__ import annotations
from config import RSS_FEEDS
from scrapers.base import parse_rss_feed

USA_FEEDS = {
    "healthline":       ("Healthline",       RSS_FEEDS["healthline"]),
    "womens_health":    ("Women's Health",   RSS_FEEDS["womens_health"]),
    "self":             ("SELF",             RSS_FEEDS["self"]),
    "greatist":         ("Greatist",         RSS_FEEDS["greatist"]),
    "popsugar_fitness": ("PopSugar Fitness", RSS_FEEDS["popsugar_fitness"]),
    "myfitnesspal":     ("MyFitnessPal",     RSS_FEEDS["myfitnesspal"]),
    "healthywomen":     ("HealthyWomen",     RSS_FEEDS["healthywomen"]),
}


def fetch() -> list[dict]:
    articles: list[dict] = []
    seen: set[str] = set()
    for source_name, url in USA_FEEDS.values():
        for a in parse_rss_feed(url, source_name):
            if a["id"] not in seen:
                seen.add(a["id"])
                articles.append(a)
    return articles
