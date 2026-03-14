import anthropic
from config import ANTHROPIC_API_KEY

_client = None


def _get_client() -> anthropic.Anthropic:
    global _client
    if _client is None:
        _client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    return _client


def summarize(article: dict) -> str:
    """Generate a 2-3 line AI summary for the article using Claude Haiku."""
    title = article.get("title", "")
    summary = article.get("summary", "")
    source = article.get("source", "")

    prompt = (
        f"Você é um assistente de saúde feminina. Leia o título e o resumo da notícia abaixo "
        f"e escreva um resumo claro e objetivo em 2-3 frases em português, destacando o ponto "
        f"mais relevante para mulheres interessadas em saúde, emagrecimento e fitness.\n\n"
        f"Fonte: {source}\n"
        f"Título: {title}\n"
        f"Resumo original: {summary}\n\n"
        f"Resumo:"
    )

    try:
        client = _get_client()
        message = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=200,
            messages=[{"role": "user", "content": prompt}],
        )
        return message.content[0].text.strip()
    except Exception as e:
        return f"Resumo indisponível: {e}"
