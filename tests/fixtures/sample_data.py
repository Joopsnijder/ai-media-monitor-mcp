"""Sample data fixtures for testing."""

from datetime import datetime, timedelta

# Sample RSS feed data
SAMPLE_RSS_FEEDS = {
    "nrc": """<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
    <channel>
        <title>NRC Tech</title>
        <description>Technology news from NRC</description>
        <item>
            <title>Kunstmatige intelligentie revolutioneert de Nederlandse zorg</title>
            <link>https://www.nrc.nl/nieuws/2024/01/01/ai-zorg-revolutie</link>
            <description>Ziekenhuizen in Nederland maken steeds meer gebruik van AI-technologie voor diagnoses en behandelingen.</description>
            <pubDate>Mon, 01 Jan 2024 10:00:00 GMT</pubDate>
        </item>
        <item>
            <title>Privacy-zorgen rond ChatGPT in het onderwijs</title>
            <link>https://www.nrc.nl/nieuws/2024/01/01/chatgpt-privacy-onderwijs</link>
            <description>Scholen worstelen met privacy-vragen bij het gebruik van AI-tools zoals ChatGPT.</description>
            <pubDate>Mon, 01 Jan 2024 09:30:00 GMT</pubDate>
        </item>
    </channel>
</rss>""",
    "volkskrant": """<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
    <channel>
        <title>de Volkskrant Tech</title>
        <description>Technology news from de Volkskrant</description>
        <item>
            <title>AI-systemen discrimineren nog steeds bij sollicitaties</title>
            <link>https://www.volkskrant.nl/nieuws/2024/01/01/ai-discriminatie-sollicitaties</link>
            <description>Onderzoek toont aan dat AI-systemen voor personeelsselectie vooroordelen kunnen versterken.</description>
            <pubDate>Mon, 01 Jan 2024 11:15:00 GMT</pubDate>
        </item>
    </channel>
</rss>""",
}

# Sample article content
SAMPLE_ARTICLES = {
    "ai_healthcare": {
        "title": "Kunstmatige intelligentie revolutioneert de Nederlandse zorg",
        "url": "https://www.nrc.nl/nieuws/2024/01/01/ai-zorg-revolutie",
        "source": "NRC",
        "date": datetime(2024, 1, 1, 10, 0),
        "content": """
Nederlandse ziekenhuizen omarmen kunstmatige intelligentie in een ongekend tempo.
Het Erasmus MC in Rotterdam gebruikt AI-systemen voor het analyseren van medische beelden,
terwijl het AMC in Amsterdam experimenten met AI-gestuurde medicijntoediening.

"AI stelt ons in staat om veel preciezere diagnoses te stellen," zegt Prof. Dr. Marie van der Berg,
hoofd radiologie bij het Erasmus MC. "We kunnen nu patronen herkennen die voor het menselijk oog
onzichtbaar zijn."

Het LUMC in Leiden heeft recent een AI-systeem geïmplementeerd dat helpt bij het voorspellen
van patiëntuitkomsten. Dr. Jan Pieterse, cardioloog bij het LUMC, legt uit: "Deze technologie
stelt ons in staat om veel eerder in te grijpen bij risicovolle situaties."

De Nederlandse AI-coalitie voor de zorg, opgericht in 2023, telt inmiddels 45 ziekenhuizen
als lid. Het doel is om kennis te delen en ethische richtlijnen te ontwikkelen voor AI in de zorg.

Echter, niet iedereen is even enthousiast. Privacy-expert Dr. Lisa Janssen van de Universiteit
van Amsterdam waarschuwt: "We moeten ervoor zorgen dat de privacy van patiënten gewaarborgd blijft
bij deze nieuwe ontwikkelingen."
        """.strip(),
        "summary": "Ziekenhuizen in Nederland maken steeds meer gebruik van AI-technologie voor diagnoses en behandelingen.",
        "mentions_ai": True,
        "ai_topics": ["AI in de zorg", "Medische AI", "AI-diagnose"],
        "quoted_experts": [
            {
                "name": "Prof. Dr. Marie van der Berg",
                "quote": "AI stelt ons in staat om veel preciezere diagnoses te stellen",
            },
            {
                "name": "Dr. Jan Pieterse",
                "quote": "Deze technologie stelt ons in staat om veel eerder in te grijpen bij risicovolle situaties",
            },
            {
                "name": "Dr. Lisa Janssen",
                "quote": "We moeten ervoor zorgen dat de privacy van patiënten gewaarborgd blijft bij deze nieuwe ontwikkelingen",
            },
        ],
    },
    "ai_education": {
        "title": "Privacy-zorgen rond ChatGPT in het onderwijs",
        "url": "https://www.nrc.nl/nieuws/2024/01/01/chatgpt-privacy-onderwijs",
        "source": "NRC",
        "date": datetime(2024, 1, 1, 9, 30),
        "content": """
Onderwijsinstellingen in Nederland worstelen met privacy-vraagstukken rond het gebruik van
AI-tools zoals ChatGPT. Verschillende universiteiten hebben richtlijnen opgesteld, maar
een landelijke aanpak ontbreekt nog.

De Autoriteit Persoonsgegevens (AP) heeft vorige maand waarschuwingen uitgegeven over
het gebruik van AI-chatbots in het onderwijs. "Studentengegevens mogen niet zomaar
worden gedeeld met Amerikaanse techbedrijven," aldus AP-voorzitter Aleid Wolfsen.

Professor AI-ethiek Sarah de Wit van de TU Delft pleit voor een genuanceerde benadering:
"We moeten de voordelen van AI in het onderwijs niet wegwuiven vanwege privacy-zorgen,
maar wel zorgvuldige afwegingen maken."

Het ministerie van Onderwijs werkt samen met universiteiten aan een landelijk kader
voor AI-gebruik in het onderwijs. Dit moet eind 2024 gereed zijn.
        """.strip(),
        "summary": "Scholen worstelen met privacy-vragen bij het gebruik van AI-tools zoals ChatGPT.",
        "mentions_ai": True,
        "ai_topics": ["AI in onderwijs", "Privacy", "ChatGPT"],
        "quoted_experts": [
            {
                "name": "Aleid Wolfsen",
                "quote": "Studentengegevens mogen niet zomaar worden gedeeld met Amerikaanse techbedrijven",
            },
            {
                "name": "Professor Sarah de Wit",
                "quote": "We moeten de voordelen van AI in het onderwijs niet wegwuiven vanwege privacy-zorgen, maar wel zorgvuldige afwegingen maken",
            },
        ],
    },
    "ai_discrimination": {
        "title": "AI-systemen discrimineren nog steeds bij sollicitaties",
        "url": "https://www.volkskrant.nl/nieuws/2024/01/01/ai-discriminatie-sollicitaties",
        "source": "de Volkskrant",
        "date": datetime(2024, 1, 1, 11, 15),
        "content": """
Een groot onderzoek van de Universiteit Utrecht toont aan dat AI-systemen die worden
gebruikt voor personeelsselectie nog steeds discrimineren op basis van geslacht,
etniciteit en leeftijd.

Het onderzoek, geleid door Dr. Ahmed Hassan, analyseerde 50 verschillende AI-systemen
die door Nederlandse bedrijven worden gebruikt. "We zien systematische vooroordelen
die vaak sterker zijn dan bij menselijke recruiters," concludeert Hassan.

Mensenrechtenorganisatie Amnesty International roept op tot strengere regulering.
Woordvoerder Dagmar Oudshoorn stelt: "Bedrijven gebruiken AI om objectiever te zijn,
maar het tegenovergestelde gebeurt."

De Tweede Kamer behandelt binnenkort een motie voor scherpere toezicht op AI in
de werving en selectie. VVD-Kamerlid Sophie Hermans is voorstander: "We kunnen niet
toestaan dat AI discriminatie institutionaliseert."
        """.strip(),
        "summary": "Onderzoek toont aan dat AI-systemen voor personeelsselectie vooroordelen kunnen versterken.",
        "mentions_ai": True,
        "ai_topics": ["AI-discriminatie", "HR-technologie", "Algoritmische bias"],
        "quoted_experts": [
            {
                "name": "Dr. Ahmed Hassan",
                "quote": "We zien systematische vooroordelen die vaak sterker zijn dan bij menselijke recruiters",
            },
            {
                "name": "Dagmar Oudshoorn",
                "quote": "Bedrijven gebruiken AI om objectiever te zijn, maar het tegenovergestelde gebeurt",
            },
            {
                "name": "Sophie Hermans",
                "quote": "We kunnen niet toestaan dat AI discriminatie institutionaliseert",
            },
        ],
    },
}

# Sample experts database
SAMPLE_EXPERTS = [
    {
        "name": "Prof. Dr. Marie van der Berg",
        "title": "Professor",
        "organization": "Erasmus MC Rotterdam",
        "expertise": ["AI in de zorg", "Medische beeldanalyse", "Radiologie"],
        "recent_quotes": 3,
        "articles": ["ai_healthcare"],
        "contact_hints": ["Erasmus MC website", "LinkedIn profiel"],
    },
    {
        "name": "Dr. Jan Pieterse",
        "title": "Cardioloog",
        "organization": "LUMC Leiden",
        "expertise": ["AI in de zorg", "Cardiologie", "Voorspellende analyse"],
        "recent_quotes": 2,
        "articles": ["ai_healthcare"],
        "contact_hints": ["LUMC website"],
    },
    {
        "name": "Dr. Lisa Janssen",
        "title": "Privacy-expert",
        "organization": "Universiteit van Amsterdam",
        "expertise": ["Privacy", "AI-ethiek", "Gegevensbescherming"],
        "recent_quotes": 4,
        "articles": ["ai_healthcare", "ai_education"],
        "contact_hints": ["UvA website", "Twitter @lisajanssen"],
    },
    {
        "name": "Professor Sarah de Wit",
        "title": "Professor AI-ethiek",
        "organization": "TU Delft",
        "expertise": ["AI-ethiek", "Onderwijs technologie", "Filosofie"],
        "recent_quotes": 5,
        "articles": ["ai_education"],
        "contact_hints": ["TU Delft website", "Researchgate profiel"],
    },
    {
        "name": "Dr. Ahmed Hassan",
        "title": "Onderzoeker",
        "organization": "Universiteit Utrecht",
        "expertise": ["Algoritmische bias", "AI-discriminatie", "Data science"],
        "recent_quotes": 3,
        "articles": ["ai_discrimination"],
        "contact_hints": ["UU website"],
    },
    {
        "name": "Aleid Wolfsen",
        "title": "Voorzitter",
        "organization": "Autoriteit Persoonsgegevens",
        "expertise": ["Privacy", "Gegevensbescherming", "Toezicht"],
        "recent_quotes": 2,
        "articles": ["ai_education"],
        "contact_hints": ["AP website", "Persberichten"],
    },
]

# Sample trending topics
SAMPLE_TRENDING_TOPICS = [
    {
        "topic": "AI in de zorg",
        "mentions": 15,
        "sources": ["NRC", "Volkskrant", "FD", "Tweakers"],
        "sentiment": "positive",
        "key_articles": ["ai_healthcare"],
        "suggested_angle": "Nederlandse ziekenhuizen lopen voorop in AI-adoptie",
        "growth_percentage": 35.2,
    },
    {
        "topic": "AI-ethiek",
        "mentions": 12,
        "sources": ["NRC", "Volkskrant", "Trouw"],
        "sentiment": "mixed",
        "key_articles": ["ai_education", "ai_discrimination"],
        "suggested_angle": "Ethische dilemma's van AI in de praktijk",
        "growth_percentage": 22.8,
    },
    {
        "topic": "Privacy en AI",
        "mentions": 10,
        "sources": ["NRC", "Tweakers", "Bright"],
        "sentiment": "concerned",
        "key_articles": ["ai_education"],
        "suggested_angle": "Balans tussen innovatie en privacy",
        "growth_percentage": 18.5,
    },
    {
        "topic": "AI-discriminatie",
        "mentions": 8,
        "sources": ["Volkskrant", "Trouw", "FD"],
        "sentiment": "negative",
        "key_articles": ["ai_discrimination"],
        "suggested_angle": "Onbedoelde gevolgen van AI-systemen",
        "growth_percentage": 45.1,
    },
]

# Sample topic suggestions
SAMPLE_TOPIC_SUGGESTIONS = [
    {
        "topic": "AI-regulering in Nederland",
        "relevance_score": 9.2,
        "reason": "Hoge activiteit rond nieuwe wetgeving en veel expertuitspraken",
        "potential_guests": ["Dr. Lisa Janssen", "Sophie Hermans"],
        "unique_angle": "Nederlandse aanpak vs Europese AI Act",
        "questions": [
            "Hoe verschilt de Nederlandse aanpak van andere EU-landen?",
            "Welke uitdagingen zien jullie bij de implementatie?",
            "Is de huidige wetgeving toereikend?",
        ],
    },
    {
        "topic": "AI in de zorg: vooruitgang vs privacy",
        "relevance_score": 8.8,
        "reason": "Sterke groei in nieuwsberichtgeving en beschikbare experts",
        "potential_guests": ["Prof. Dr. Marie van der Berg", "Dr. Jan Pieterse"],
        "unique_angle": "Concrete Nederlandse succesverhalen en uitdagingen",
        "questions": [
            "Welke AI-toepassingen zijn het meest veelbelovend?",
            "Hoe wordt patiëntprivacy gewaarborgd?",
            "Wat zijn de praktische uitdagingen bij implementatie?",
        ],
    },
    {
        "topic": "Algoritmische discriminatie in de praktijk",
        "relevance_score": 8.5,
        "reason": "Recent onderzoek en maatschappelijke relevantie",
        "potential_guests": ["Dr. Ahmed Hassan", "Dagmar Oudshoorn"],
        "unique_angle": "Van theorie naar praktijk: echte gevallen uit Nederland",
        "questions": [
            "Welke sectoren zijn het meest kwetsbaar?",
            "Hoe kunnen bedrijven dit voorkomen?",
            "Wat moet er veranderen in de wetgeving?",
        ],
    },
]

# Sample configuration data
SAMPLE_CONFIG = {
    "media_sources": {
        "newspapers": [
            {
                "name": "NRC",
                "url": "https://www.nrc.nl",
                "rss": "https://www.nrc.nl/rss/",
                "categories": ["tech", "politics", "economy"],
            },
            {
                "name": "de Volkskrant",
                "url": "https://www.volkskrant.nl",
                "rss": "https://www.volkskrant.nl/rss.xml",
                "categories": ["tech", "society"],
            },
        ],
        "tech_media": [
            {
                "name": "Tweakers",
                "url": "https://tweakers.net",
                "rss": "https://feeds.feedburner.com/tweakers/mixed",
                "categories": ["tech", "hardware", "software"],
            },
            {
                "name": "Bright",
                "url": "https://www.bright.nl",
                "rss": "https://www.bright.nl/feed",
                "categories": ["tech", "innovation"],
            },
        ],
    },
    "paywall_services": [
        {"url": "https://archive.ph", "method": "POST", "priority": 1},
        {"url": "https://12ft.io", "method": "GET", "priority": 2},
    ],
    "retry_attempts": 3,
    "timeout": 30,
    "rate_limit": 10,
}


# Time-based test data
def get_sample_articles_by_timeframe(hours_back: int = 24) -> list[dict]:
    """Get sample articles filtered by timeframe."""
    cutoff_time = datetime.now() - timedelta(hours=hours_back)
    return [article for article in SAMPLE_ARTICLES.values() if article["date"] >= cutoff_time]


def get_sample_experts_by_topic(topic: str | None = None) -> list[dict]:
    """Get sample experts filtered by topic."""
    if not topic:
        return SAMPLE_EXPERTS

    return [
        expert
        for expert in SAMPLE_EXPERTS
        if any(topic.lower() in expertise.lower() for expertise in expert["expertise"])
    ]


def get_sample_trending_topics_by_period(period: str = "week") -> list[dict]:
    """Get sample trending topics filtered by period."""
    period_multipliers = {"day": 1, "week": 7, "month": 30}
    multiplier = period_multipliers.get(period, 7)

    # Simulate different data volumes based on period
    return SAMPLE_TRENDING_TOPICS[: int(len(SAMPLE_TRENDING_TOPICS) * (multiplier / 7))]
