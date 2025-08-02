"""Text analysis utilities for AI content detection."""

import re

from ..core.config_loader import load_config


def is_ai_related(text: str) -> bool:
    """Check if text contains AI-related keywords"""
    config = load_config()
    ai_keywords = config.ai_keywords

    text_lower = text.lower()
    return any(re.search(pattern, text_lower, re.IGNORECASE) for pattern in ai_keywords)


def extract_ai_topics(text: str) -> list[str]:
    """Extract specific AI topics from text"""
    config = load_config()
    topic_patterns = config.topic_patterns

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
