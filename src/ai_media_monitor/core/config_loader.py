"""Configuration loading functionality."""

import yaml

from ..models.config import Config


def load_config() -> Config:
    """Load configuration from file or use defaults"""
    default_config = {
        "media_sources": {
            "newspapers": [
                {"name": "NRC", "url": "https://www.nrc.nl", "rss": "https://www.nrc.nl/rss/"},
                {
                    "name": "Volkskrant",
                    "url": "https://www.volkskrant.nl",
                    "rss": "https://www.volkskrant.nl/voorpagina/rss.xml",
                },
                {"name": "FD", "url": "https://fd.nl", "rss": "https://fd.nl/rss"},
                {
                    "name": "Telegraaf",
                    "url": "https://www.telegraaf.nl",
                    "rss": "https://www.telegraaf.nl/rss",
                },
                {"name": "AD", "url": "https://www.ad.nl", "rss": "https://www.ad.nl/tech/rss.xml"},
                {
                    "name": "Trouw",
                    "url": "https://www.trouw.nl",
                    "rss": "https://www.trouw.nl/cs-b7d0a82a.xml",
                },
            ],
            "trade_publications": [
                {
                    "name": "Computable",
                    "url": "https://www.computable.nl",
                    "rss": "https://www.computable.nl/rss/nieuws.xml",
                },
                {"name": "AG Connect", "url": "https://www.agconnect.nl"},
                {"name": "MT/Sprout", "url": "https://www.mt.nl", "rss": "https://www.mt.nl/feed"},
                {
                    "name": "Emerce",
                    "url": "https://www.emerce.nl",
                    "rss": "https://www.emerce.nl/feed",
                },
            ],
            "tech_media": [
                {
                    "name": "Tweakers",
                    "url": "https://tweakers.net",
                    "rss": "https://feeds.feedburner.com/tweakers/mixed",
                },
                {
                    "name": "Bright",
                    "url": "https://www.bright.nl",
                    "rss": "https://www.bright.nl/rss",
                },
                {
                    "name": "Dutch IT Channel",
                    "url": "https://dutchitchannel.nl",
                    "rss": "https://dutchitchannel.nl/feed",
                },
            ],
            "news_sites": [
                {"name": "NU.nl", "url": "https://www.nu.nl", "rss": "https://www.nu.nl/rss/Tech"},
                {
                    "name": "RTL Nieuws",
                    "url": "https://www.rtlnieuws.nl",
                    "rss": "https://www.rtlnieuws.nl/rss.xml",
                },
                {
                    "name": "NOS",
                    "url": "https://nos.nl",
                    "rss": "https://feeds.nos.nl/nosnieuwstech",
                },
            ],
        },
        "paywall_services": [
            {"url": "https://archive.ph", "method": "POST", "priority": 1},
            {"url": "https://1ft.io", "method": "GET", "priority": 2},
            {"url": "https://12ft.io", "method": "GET", "priority": 3},
            {"url": "https://web.archive.org/save", "method": "GET", "priority": 4},
        ],
        "retry_attempts": 3,
        "timeout": 30,
        "rate_limit": 10,
        "ai_keywords": [
            r"\bAI\b",
            r"\bartifici[eë]le intelligentie\b",
            r"\bkunstmatige intelligentie\b",
            r"\bmachine learning\b",
            r"\bdeep learning\b",
            r"\balgoritm[e|es]\b",
            r"\bChatGPT\b",
            r"\bGPT\b",
            r"\bLLM\b",
            r"\blarge language model\b",
            r"\bneural[e]? net\w*\b",
            r"\bdata scien\w*\b",
            r"\bautomatis\w*\b",
        ],
        "topic_patterns": {
            "AI in de zorg": ["zorg", "gezondheid", "ziekenhuis", "patient", "diagnos"],
            "AI en privacy": ["privacy", "AVG", "GDPR", "persoonsgegevens", "data protection"],
            "AI in het onderwijs": ["onderwijs", "school", "student", "leren", "educatie"],
            "AI en werkgelegenheid": ["banen", "werkgelegenheid", "arbeidsmarkt", "werknemers"],
            "AI-wetgeving": ["wetgeving", "regulering", "AI Act", "toezicht", "compliance"],
            "AI in de rechtspraak": ["rechtspraak", "rechtbank", "juridisch", "advocat"],
            "Generative AI": ["generat", "ChatGPT", "GPT", "LLM", "chatbot"],
            "AI-ethiek": ["ethiek", "ethisch", "discriminatie", "bias", "verantwoord"],
            "AI in retail": ["retail", "winkel", "e-commerce", "klant", "verkoop"],
            "AI in finance": ["bank", "financi", "verzekering", "fintech", "betaal"],
        },
    }

    # Try to load from config.yaml if it exists
    try:
        with open("config.yaml") as f:
            config_data = yaml.safe_load(f)
            return Config(**config_data)
    except (FileNotFoundError, yaml.YAMLError, TypeError, ValueError):
        return Config(**default_config)
