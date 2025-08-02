# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an AI Media Monitor MCP (Model Context Protocol) server that scans Dutch media sources for AI-related articles and provides analysis for podcast planning. It's designed to support the AIToday Live podcast by identifying trending topics, potential guests, and content suggestions.

## Core Architecture

The project is built using FastMCP and follows these patterns:

- **FastMCP Server**: Main entry point in `ai-media-monitor-mcp.py` using `@mcp.tool()` decorators
- **Configuration-driven**: Media sources and settings defined in `config.yaml` with fallback defaults
- **Async Architecture**: Uses `aiohttp` for concurrent web scraping and RSS parsing
- **Data Models**: Pydantic models for Article, Expert, TrendingTopic, TopicSuggestion with Dutch-specific patterns
- **Multi-source Monitoring**: Scans newspapers, trade publications, tech media, and news sites

## Key Components

### Media Source Categories
- `newspapers`: Major Dutch newspapers (NRC, Volkskrant, FD, etc.)
- `trade_publications`: Industry publications (Computable, MT/Sprout, etc.)  
- `tech_media`: Tech-focused outlets (Tweakers, Bright, etc.)
- `news_sites`: General news with tech sections (NU.nl, RTL, NOS)

### Content Analysis
- **AI Detection**: Uses Dutch/English keyword patterns to identify AI-related content
- **Topic Extraction**: Categorizes into specific Dutch AI domains (zorg, privacy, onderwijs, etc.)
- **Expert Identification**: Extracts quotes and attributions using Dutch language patterns
- **Paywall Bypass**: Attempts content access through archive services (archive.ph, 12ft.io, etc.)

### Core Tools
1. `scan_media_sources`: Scans all RSS feeds for recent AI articles
2. `get_trending_topics`: Analyzes topic trends with sentiment and growth
3. `identify_experts`: Finds frequently quoted experts as potential podcast guests
4. `generate_topic_suggestions`: Creates actionable podcast topic ideas
5. `fetch_article`: Retrieves full article content with paywall bypass
6. `get_weekly_report`: Comprehensive weekly analysis report

## Development Commands

```bash
# Run the MCP server
python server.py
# OR using uv scripts
uv run server

# Linting and formatting (ALWAYS run before committing)
uv run lint          # Check for linting errors
uv run lint-fix      # Fix linting errors automatically  
uv run format        # Format code with ruff
uv run test          # Run tests

# Install development dependencies
uv sync --dev
```

## Configuration

- Primary config in `config.yaml` with media sources and paywall services
- Fallback configuration embedded in code for reliability
- Rate limiting and retry logic configurable per source
- Async session management with timeout controls

## Code Quality Standards

**IMPORTANT**: Always run linting and formatting before committing:
- Use `uv run lint-fix` to automatically fix linting errors
- Use `uv run format` to format code consistently
- All code must pass `uv run lint` without errors
- Follow modern Python practices (use `list[str]` instead of `List[str]`, etc.)

## Dutch Language Considerations

The codebase includes Dutch-specific patterns for:
- AI terminology detection (kunstmatige intelligentie, algoritme, etc.)
- Quote attribution patterns (zegt, aldus, volgens)
- Topic categorization using Dutch domain terms
- Sentiment analysis with Dutch keywords