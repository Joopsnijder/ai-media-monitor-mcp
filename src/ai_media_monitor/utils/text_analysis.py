"""Text analysis utilities for AI content detection."""

import re


def is_ai_related(text: str) -> bool:
    """Check if text contains AI-related keywords"""
    ai_keywords = [
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
    ]

    text_lower = text.lower()
    return any(re.search(pattern, text_lower, re.IGNORECASE) for pattern in ai_keywords)


def extract_ai_topics(text: str) -> list[str]:
    """Extract specific AI topics from text"""
    topic_patterns = {
        "AI in de zorg": [r"zorg", r"gezondheid", r"ziekenhuis", r"patient", r"diagnos"],
        "AI en privacy": [r"privacy", r"AVG", r"GDPR", r"persoonsgegevens", r"data protection"],
        "AI in het onderwijs": [r"onderwijs", r"school", r"student", r"leren", r"educatie"],
        "AI en werkgelegenheid": [r"banen", r"werkgelegenheid", r"arbeidsmarkt", r"werknemers"],
        "AI-wetgeving": [r"wetgeving", r"regulering", r"AI Act", r"toezicht", r"compliance"],
        "AI in de rechtspraak": [r"rechtspraak", r"rechtbank", r"juridisch", r"advocat"],
        "Generative AI": [r"generat", r"ChatGPT", r"GPT", r"LLM", r"chatbot"],
        "AI-ethiek": [r"ethiek", r"ethisch", r"discriminatie", r"bias", r"verantwoord"],
        "AI in retail": [r"retail", r"winkel", r"e-commerce", r"klant", r"verkoop"],
        "AI in finance": [r"bank", r"financi", r"verzekering", r"fintech", r"betaal"],
    }

    found_topics = []
    text_lower = text.lower()

    for topic, patterns in topic_patterns.items():
        if any(re.search(pattern, text_lower) for pattern in patterns):
            found_topics.append(topic)

    return found_topics


def extract_quotes_and_experts(content: str) -> list[dict[str, str]]:
    """Extract quotes and expert names from article content"""
    experts = []

    # Patterns for finding quotes and attributions
    quote_patterns = [
        r'"([^"]+)"[,\s]*(?:zegt|aldus|volgens)\s+([A-Z][a-zA-Z\s\.]+?)(?:\.|,)',
        r'([A-Z][a-zA-Z\s\.]+?)(?:\s+zegt|\s+stelt|\s+vindt)[:\s]*"([^"]+)"',
        r'Volgens\s+([A-Z][a-zA-Z\s\.]+?)[,\s]+"([^"]+)"',
    ]

    for pattern in quote_patterns:
        matches = re.finditer(pattern, content)
        for match in matches:
            if len(match.groups()) == 2:
                quote = match.group(1) if match.group(1)[0] == '"' else match.group(2)
                expert = match.group(2) if match.group(1)[0] == '"' else match.group(1)

                # Clean up expert name
                expert = expert.strip().rstrip(".,")

                # Filter out common false positives
                if len(expert.split()) <= 5 and not any(
                    word in expert.lower() for word in ["het", "de", "een"]
                ):
                    experts.append({"name": expert, "quote": quote.strip('"')})

    return experts
