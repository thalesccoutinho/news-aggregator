import os
from dotenv import load_dotenv

load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")

RSS_FEEDS = {
    # Brasil
    "g1_saude": "https://g1.globo.com/rss/g1/saude/",
    "g1_ciencia": "https://g1.globo.com/rss/g1/ciencia-e-saude/",
    "folha": "https://feeds.folha.uol.com.br/equilibrioesaude/rss091.xml",
    # EUA
    "healthline": "https://www.healthline.com/rss/health-news",
    "womens_health": "https://www.womenshealthmag.com/rss/all.xml/",
    "self": "https://www.self.com/feed/rss",
    "greatist": "https://greatist.com/feed",
    "popsugar_fitness": "https://www.popsugar.com/fitness/feed",
    "myfitnesspal": "https://blog.myfitnesspal.com/feed/",
    "healthywomen": "https://www.healthywomen.org/rss.xml",
}

MINHA_VIDA_URL = "https://www.minhavida.com.br/"

CATEGORIES = {
    "Emagrecimento": [
        "dieta", "emagrecimento", "perda de peso", "emagrecer", "gordura", "calorias", "jejum", "emagre",
        "weight loss", "diet", "fat", "calories", "fasting", "slim", "obesity",
    ],
    "Fitness": [
        "treino", "exercício", "academia", "musculação", "corrida", "fitness", "ginástica", "hiit", "crossfit",
        "workout", "exercise", "training", "gym", "running", "strength",
    ],
    "Nutrição": [
        "alimentação", "proteína", "vitamina", "suplemento", "cardápio", "nutrição", "nutriente", "alimento",
        "nutrition", "protein", "vitamin", "supplement", "meal", "food",
    ],
    "Saúde da Mulher": [
        "menopausa", "hormônio", "ciclo menstrual", "gravidez", "ginecologia", "útero", "ovário", "menstruação", "fertilidade",
        "menopause", "hormone", "menstrual", "pregnancy", "fertility", "women's health", "pcos",
    ],
    "Wellness": [
        "wellness", "mental health", "stress", "sleep", "mindfulness", "anxiety", "self-care", "holistic",
        "bem-estar", "saúde mental", "sono", "ansiedade",
    ],
}

CACHE_TTL_SECONDS = 1800  # 30 minutes
