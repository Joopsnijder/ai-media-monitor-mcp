"""Unit tests for text analysis utilities."""

from src.ai_media_monitor.utils.text_analysis import (
    extract_ai_topics,
    extract_quotes_and_experts,
    is_ai_related,
)


class TestIsAiRelated:
    """Tests for AI-related text detection."""

    def test_detects_ai_keyword(self):
        """Test detection of AI keyword."""
        assert is_ai_related("This article discusses AI technology")
        assert is_ai_related("Artificial intelligence is transforming healthcare")
        assert is_ai_related("ChatGPT heeft een grote impact")

    def test_detects_dutch_ai_terms(self):
        """Test detection of Dutch AI terminology."""
        assert is_ai_related("Kunstmatige intelligentie in de zorg")
        assert is_ai_related("Algoritme helpt bij diagnose")
        assert is_ai_related("Machine learning verbetert resultaten")

    def test_case_insensitive_detection(self):
        """Test case-insensitive detection."""
        assert is_ai_related("ai technology")
        assert is_ai_related("ARTIFICIAL INTELLIGENCE")
        assert is_ai_related("ChatGpt is populair")

    def test_rejects_non_ai_content(self):
        """Test rejection of non-AI content."""
        assert not is_ai_related("This is about regular technology")
        assert not is_ai_related("Weather forecast for tomorrow")
        assert not is_ai_related("Sports news and results")

    def test_word_boundaries(self):
        """Test that word boundaries are respected."""
        assert not is_ai_related("Waistline problems")  # Contains 'ai' but not AI
        assert is_ai_related("The AI system works well")


class TestExtractAiTopics:
    """Tests for AI topic extraction."""

    def test_extracts_healthcare_topic(self):
        """Test extraction of healthcare AI topic."""
        text = "AI in de zorg helpt artsen bij diagnose van patiënten"
        topics = extract_ai_topics(text)
        assert "AI in de zorg" in topics

    def test_extracts_education_topic(self):
        """Test extraction of education AI topic."""
        text = "Scholen gebruiken AI voor personaliseerd leren van studenten"
        topics = extract_ai_topics(text)
        assert "AI in het onderwijs" in topics

    def test_extracts_privacy_topic(self):
        """Test extraction of privacy AI topic."""
        text = "AVG regels voor AI en privacy van persoonsgegevens"
        topics = extract_ai_topics(text)
        assert "AI en privacy" in topics

    def test_extracts_multiple_topics(self):
        """Test extraction of multiple topics."""
        text = "AI in de zorg en privacy zorgen voor ethische discussies"
        topics = extract_ai_topics(text)
        assert "AI in de zorg" in topics
        assert "AI en privacy" in topics
        assert "AI-ethiek" in topics

    def test_no_topics_in_non_ai_text(self):
        """Test no topics extracted from non-AI text."""
        text = "Regular news about sports and weather"
        topics = extract_ai_topics(text)
        assert len(topics) == 0


class TestExtractQuotesAndExperts:
    """Tests for quote and expert extraction."""

    def test_extracts_simple_quote(self):
        """Test extraction of simple quote pattern."""
        content = '"Dit is een belangrijke ontwikkeling", zegt Jan de Vries.'
        experts = extract_quotes_and_experts(content)
        assert len(experts) == 1
        assert experts[0]["name"] == "Jan de Vries"
        assert experts[0]["quote"] == "Dit is een belangrijke ontwikkeling"

    def test_extracts_volgens_pattern(self):
        """Test extraction of 'volgens' pattern."""
        content = 'Volgens Prof. dr. Maria van der Berg, "AI verandert alles".'
        experts = extract_quotes_and_experts(content)
        assert len(experts) == 1
        assert experts[0]["name"] == "Prof. dr. Maria van der Berg"
        assert experts[0]["quote"] == "AI verandert alles"

    def test_extracts_expert_first_pattern(self):
        """Test extraction when expert name comes first."""
        content = 'Directeur Piet Janssen stelt: "We investeren in AI technologie".'
        experts = extract_quotes_and_experts(content)
        assert len(experts) == 1
        assert experts[0]["name"] == "Directeur Piet Janssen"
        assert experts[0]["quote"] == "We investeren in AI technologie"

    def test_filters_false_positives(self):
        """Test filtering of common false positives."""
        content = '"Het probleem is complex", zegt het rapport.'
        experts = extract_quotes_and_experts(content)
        assert len(experts) == 0  # "het rapport" should be filtered out

    def test_multiple_experts(self):
        """Test extraction of multiple experts."""
        content = """
        "AI is de toekomst", zegt CEO Anna Bakker.
        Volgens wetenschapper Dr. Tom Peters, "We moeten voorzichtig zijn".
        """
        experts = extract_quotes_and_experts(content)
        assert len(experts) == 2
        names = [expert["name"] for expert in experts]
        assert "CEO Anna Bakker" in names
        assert "Dr. Tom Peters" in names

    def test_empty_content(self):
        """Test handling of empty content."""
        experts = extract_quotes_and_experts("")
        assert len(experts) == 0

    def test_no_quotes_found(self):
        """Test content with no quotes."""
        content = "This is regular text without any quotes or experts mentioned."
        experts = extract_quotes_and_experts(content)
        assert len(experts) == 0
