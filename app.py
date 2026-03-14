from __future__ import annotations
from flask import Flask, jsonify, render_template, request
from datetime import datetime, timedelta
import threading

from scrapers import g1, uol, terra, minha_vida, usa
from categorizer import categorize_all, trending_keywords
from analyzer import summarize

app = Flask(__name__)

# ── In-memory cache ──────────────────────────────────────────────────────────
_cache: dict[str, dict] = {}   # article_id -> article
_last_refresh: datetime | None = None
_cache_lock = threading.Lock()
CACHE_TTL = timedelta(minutes=30)


def _refresh_cache() -> None:
    global _last_refresh
    all_articles: list[dict] = []
    for module in (g1, uol, terra, minha_vida, usa):
        all_articles.extend(module.fetch())

    categorize_all(all_articles)

    with _cache_lock:
        for article in all_articles:
            _cache[article["id"]] = article
        _last_refresh = datetime.utcnow()


def _ensure_fresh() -> None:
    global _last_refresh
    with _cache_lock:
        stale = _last_refresh is None or (datetime.utcnow() - _last_refresh) > CACHE_TTL

    if stale:
        _refresh_cache()


# ── Routes ───────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    _ensure_fresh()
    with _cache_lock:
        articles = list(_cache.values())
    trending = trending_keywords(articles)
    categories = sorted({a["category"] for a in articles if a["category"] != "Geral"})
    return render_template(
        "index.html",
        articles=articles,
        trending=trending,
        categories=categories,
        last_refresh=_last_refresh.strftime("%H:%M:%S") if _last_refresh else "—",
    )


@app.route("/api/articles")
def api_articles():
    _ensure_fresh()
    category = request.args.get("category", "")
    with _cache_lock:
        articles = list(_cache.values())
    if category:
        articles = [a for a in articles if a["category"] == category]
    return jsonify(articles)


@app.route("/api/summarize/<article_id>", methods=["POST"])
def api_summarize(article_id: str):
    with _cache_lock:
        article = _cache.get(article_id)
    if not article:
        return jsonify({"error": "Artigo não encontrado"}), 404

    if article.get("ai_summary"):
        return jsonify({"summary": article["ai_summary"]})

    ai_summary = summarize(article)
    with _cache_lock:
        if article_id in _cache:
            _cache[article_id]["ai_summary"] = ai_summary
    return jsonify({"summary": ai_summary})


@app.route("/api/refresh", methods=["POST"])
def api_refresh():
    _refresh_cache()
    return jsonify({"status": "ok", "count": len(_cache)})


@app.route("/api/trending")
def api_trending():
    _ensure_fresh()
    with _cache_lock:
        articles = list(_cache.values())
    return jsonify(trending_keywords(articles))


if __name__ == "__main__":
    app.run(debug=True, port=5000)
