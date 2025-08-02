# AI Media Monitor MCP Server

An AI Media Monitor MCP (Model Context Protocol) server that scans Dutch media sources for AI-related articles and provides analysis for podcast planning. Specifically designed to support the **AIToday Live** podcast by identifying trending topics, potential guests, and content suggestions.

## Features

- 🔍 **Multi-source Media Monitoring**: Scans Dutch newspapers, trade publications, tech media, and news sites
- 🤖 **AI Content Detection**: Configurable keyword-based detection for AI-related articles
- 📊 **Trend Analysis**: Identifies trending AI topics with sentiment and growth metrics
- 👤 **Expert Identification**: Finds frequently quoted experts as potential podcast guests
- 💡 **Topic Suggestions**: Generates actionable podcast topic ideas with relevance scoring
- 🔓 **Paywall Bypass**: Attempts content access through multiple archive services
- ⚙️ **Configurable**: Fully customizable media sources, keywords, and topic patterns

## Quick Start

### Prerequisites

- Python 3.10 or higher
- [uv](https://github.com/astral-sh/uv) package manager (recommended)

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/ai-media-monitor-mcp.git
   cd ai-media-monitor-mcp
   ```

2. **Install dependencies**:
   ```bash
   uv sync
   ```

3. **Start the MCP server**:
   ```bash
   uv run server
   ```

### Usage with Claude Desktop

1. **Add to Claude Desktop configuration** (`~/.claude_desktop_config.json`):
   ```json
   {
     "mcpServers": {
       "ai-media-monitor": {
         "command": "uv",
         "args": ["run", "server"],
         "cwd": "/path/to/ai-media-monitor-mcp"
       }
     }
   }
   ```

2. **Restart Claude Desktop** and start using the AI Media Monitor tools.

## Available MCP Tools

### 1. `scan_media_sources`

Scans all configured Dutch media sources for AI-related articles.

**Parameters:**
- `hours_back` (int, optional): How many hours back to scan (default: 24)

**Example:**
```
Scan media sources for AI articles from the last 48 hours
```

### 2. `get_trending_topics`

Analyzes trending AI topics in Dutch media with detailed metrics.

**Parameters:**
- `period` (str): Time period - "day", "week", or "month" (default: "week")
- `min_mentions` (int): Minimum mentions required (default: 3)
- `categories` (list[str], optional): Filter by specific categories

**Example:**
```
Get trending AI topics for the last week with at least 5 mentions
```

### 3. `identify_experts`

Identifies potential podcast guests based on media coverage and quotes.

**Parameters:**
- `topic` (str, optional): Focus on specific AI topic
- `period` (str): Time period to analyze (default: "month")
- `min_quotes` (int): Minimum quotes required (default: 2)

**Example:**
```
Find AI experts in healthcare who have been quoted at least 3 times this month
```

### 4. `generate_topic_suggestions`

Generates podcast topic suggestions based on current media trends.

**Parameters:**
- `focus_areas` (list[str], optional): Specific areas to focus on

**Example:**
```
Generate podcast topic suggestions focusing on AI ethics and privacy
```

### 5. `fetch_article`

Fetches full content of a specific article, attempting paywall bypass.

**Parameters:**
- `url` (str): URL of the article to fetch

**Example:**
```
Fetch the full content of this NRC article about AI in healthcare
```

### 6. `get_weekly_report`

Generates a comprehensive weekly report for podcast planning.

**Returns:** Complete analysis including trending topics, expert suggestions, and content recommendations.

## Configuration

The server uses `config.yaml` for configuration. Key sections include:

### Media Sources

Configure Dutch media sources by category:

```yaml
media_sources:
  newspapers:
    - name: "NRC"
      url: "https://www.nrc.nl"
      rss: "https://www.nrc.nl/rss/"
  tech_media:
    - name: "Tweakers"
      url: "https://tweakers.net"
      rss: "https://feeds.feedburner.com/tweakers/mixed"
```

### AI Keywords (Configurable)

Customize AI detection keywords:

```yaml
ai_keywords:
  - "\\bAI\\b"
  - "\\bkunstmatige intelligentie\\b"
  - "\\bmachine learning\\b"
  - "\\bChatGPT\\b"
```

### Topic Patterns (Configurable)

Define topic categorization patterns:

```yaml
topic_patterns:
  "AI in de zorg":
    - "zorg"
    - "gezondheid"
    - "ziekenhuis"
  "AI en privacy":
    - "privacy"
    - "AVG"
    - "GDPR"
```

### Paywall Bypass

Configure paywall bypass services:

```yaml
paywall_bypass:
  services:
    - url: "https://archive.ph"
      method: "POST"
      priority: 1
  retry_attempts: 3
  timeout: 30
```

## Media Sources

The server monitors these Dutch media categories:

### Newspapers
- NRC, Volkskrant, FD, Telegraaf, AD, Trouw

### Trade Publications  
- Computable, AG Connect, MT/Sprout, Emerce

### Tech Media
- Tweakers, Bright, Dutch IT Channel

### News Sites
- NU.nl, RTL Nieuws, NOS

## Development

### Setup Development Environment

```bash
# Install with development dependencies
uv sync --dev

# Run tests
uv run test

# Lint and format code
uv run lint-fix
uv run format

# Check for linting errors
uv run lint
```

### Project Structure

```
src/ai_media_monitor/
├── core/           # Core functionality
│   ├── analyzer.py     # Main analysis engine
│   └── config_loader.py # Configuration loading
├── models/         # Data models
│   ├── article.py      # Article data model
│   ├── expert.py       # Expert data model
│   └── topic.py        # Topic data models
└── utils/          # Utilities
    ├── text_analysis.py # Text processing
    └── web_utils.py     # Web scraping utilities
```

### Code Quality

The project enforces high code quality standards:

- **Ruff** for linting and formatting
- **Pytest** for testing with asyncio support
- **Type hints** throughout the codebase
- **Pre-commit hooks** for automated checks

### Adding New Media Sources

1. Add the source to `config.yaml` under the appropriate category
2. Ensure the RSS feed is accessible
3. Test with `scan_media_sources` tool
4. Update documentation if needed

### Customizing AI Detection

1. Modify `ai_keywords` in `config.yaml` to add/remove detection patterns
2. Update `topic_patterns` to customize topic categorization
3. Test changes with sample articles
4. Validate with the text analysis functions

## Use Cases

### Podcast Planning
- Identify trending AI topics for episode themes
- Find expert guests through quote analysis
- Generate content suggestions based on media coverage
- Monitor media sentiment around AI topics

### Media Research
- Track AI coverage across Dutch media landscape
- Analyze expert opinions and positions
- Monitor emerging AI trends and developments
- Research specific AI topics or companies

### Content Strategy
- Understand public discourse around AI in Netherlands
- Identify content gaps and opportunities
- Track competitor mentions and coverage
- Monitor regulatory and policy developments

## Troubleshooting

### Common Issues

**Server won't start:**
- Check Python version (3.10+ required)
- Ensure all dependencies are installed: `uv sync`
- Verify `config.yaml` syntax

**No articles found:**
- Check internet connection
- Verify RSS feeds are accessible
- Adjust `ai_keywords` if detection is too restrictive

**Paywall bypass not working:**
- Services may be temporarily unavailable
- Try adjusting timeout settings
- Check if specific sites block archive services

### Debug Mode

Run with debug logging:
```bash
uv run python server.py --debug
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes with tests
4. Run linting and tests: `uv run lint && uv run test`
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues and questions:
- Open an issue on GitHub
- Check existing documentation
- Review configuration examples

---

Built with ❤️ for the AIToday Live podcast and the Dutch AI community.