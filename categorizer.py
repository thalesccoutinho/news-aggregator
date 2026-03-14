from collections import Counter
from config import CATEGORIES


def categorize(article: dict) -> str:
    """Return the best-matching category for an article, or 'Geral'."""
    text = (article.get("title", "") + " " + article.get("summary", "")).lower()
    scores = {}
    for category, keywords in CATEGORIES.items():
        score = sum(1 for kw in keywords if kw.lower() in text)
        if score > 0:
            scores[category] = score
    if not scores:
        return "Geral"
    return max(scores, key=scores.get)


def categorize_all(articles: list[dict]) -> list[dict]:
    for article in articles:
        if not article.get("category"):
            article["category"] = categorize(article)
    return articles


def trending_keywords(articles: list[dict], top_n: int = 10) -> list[tuple[str, int]]:
    """Count keyword mentions across all articles and return top N."""
    counter = Counter()
    all_keywords = [kw for kws in CATEGORIES.values() for kw in kws]
    for article in articles:
        text = (article.get("title", "") + " " + article.get("summary", "")).lower()
        for kw in all_keywords:
            if kw.lower() in text:
                counter[kw] += 1
    return counter.most_common(top_n)
