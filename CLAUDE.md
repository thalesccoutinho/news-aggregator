# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Running the app

```bash
pip3 install -r requirements.txt
cp .env.example .env   # then fill in ANTHROPIC_API_KEY
python3 app.py         # serves on http://127.0.0.1:5000
```

Requires Python 3.9+ (uses `from __future__ import annotations` for compatibility).

## Architecture

**Request flow:** Browser → Flask (`app.py`) → in-memory cache (`_cache` dict) → scraper modules → RSS feeds / BeautifulSoup scraping.

**In-memory cache** (`app.py`): Articles are keyed by MD5 of their URL. Cache TTL is 30 minutes. Thread-safe via `_cache_lock`. `_ensure_fresh()` triggers `_refresh_cache()` on first load or after TTL expires.

**Scrapers** (`scrapers/`):
- `base.py` — shared `parse_rss_feed(url, source_name)` used by all RSS scrapers
- `g1.py` — fetches two G1 RSS feeds (saúde + ciência e saúde), deduplicates
- `uol.py` — repurposed to fetch Folha de S.Paulo (RSS feed changed)
- `terra.py` — disabled (returns `[]`), original feed is dead
- `minha_vida.py` — BeautifulSoup scraping (no RSS available)
- `usa.py` — aggregates 7 US health/fitness RSS feeds (Healthline, Women's Health, SELF, Greatist, PopSugar Fitness, MyFitnessPal, HealthyWomen)

**Categorization** (`categorizer.py`): Keyword matching on title+summary text. Categories: Emagrecimento, Fitness, Nutrição, Saúde da Mulher, Wellness (PT + EN keywords). Uncategorized articles fall into "Geral".

**AI summarization** (`analyzer.py`): On-demand via `POST /api/summarize/<id>`. Uses `claude-haiku-4-5-20251001`. Summary is cached back into `_cache` after generation.

**Trending** (`categorizer.py → trending_keywords()`): Counts keyword frequency across all cached articles, returns top 10.

## Key routes

| Route | Description |
|---|---|
| `GET /` | Main page (triggers cache refresh if stale) |
| `GET /api/articles?category=X` | JSON list, optional category filter |
| `POST /api/summarize/<id>` | Generate/return AI summary for one article |
| `POST /api/refresh` | Force cache refresh |
| `GET /api/trending` | Top 10 trending keywords as JSON |

## Adding a new RSS source

1. Add the URL to `RSS_FEEDS` in `config.py`
2. Either add it to `scrapers/usa.py` (for US sources) or create a new scraper module
3. Import and add to the `for module in (...)` loop in `app.py`

## Environment

Single required env var: `ANTHROPIC_API_KEY` in `.env` file. Without it, AI summaries return an error message but the rest of the app works normally.

## GitHub repository

Repo: **https://github.com/thalesccoutinho/news-aggregator**

A `post-commit` hook (`.git/hooks/post-commit`) automatically pushes to `origin main` after every commit. So the workflow to publish changes is simply:

```bash
git add -A
git commit -m "descrição da alteração"
# push happens automatically
```

**Important:** `.env` is in `.gitignore` — never commit it. The `.env.example` file documents the required variable without the real key.
