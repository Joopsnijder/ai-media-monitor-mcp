# Configuration Guide

This guide covers all configuration options for the AI Media Monitor MCP server.

## Configuration File

The server uses `config.yaml` for configuration. If the file is missing or invalid, the server falls back to embedded defaults.

## Configuration Sections

### Media Sources

Configure Dutch media sources by category. Each source requires a `name` and `url`, with optional `rss` feed and `categories`.

```yaml
media_sources:
  newspapers:
    - name: "NRC"
      url: "https://www.nrc.nl"
      rss: "https://www.nrc.nl/rss/"
      categories: ["tech", "economie"]
    - name: "Volkskrant"
      url: "https://www.volkskrant.nl"
      rss: "https://www.volkskrant.nl/voorpagina/rss.xml"
  
  trade_publications:
    - name: "Computable"
      url: "https://www.computable.nl"
      rss: "https://www.computable.nl/rss/nieuws.xml"
  
  tech_media:
    - name: "Tweakers"
      url: "https://tweakers.net"
      rss: "https://feeds.feedburner.com/tweakers/mixed"
  
  news_sites:
    - name: "NU.nl"
      url: "https://www.nu.nl"
      rss: "https://www.nu.nl/rss/Tech"
```

**Field Definitions:**
- `name`: Display name for the media source
- `url`: Base URL of the media source
- `rss`: RSS feed URL (optional, used for automated scanning)
- `categories`: Content categories to focus on (optional)

**Categories:**
- `newspapers`: Major Dutch newspapers
- `trade_publications`: Industry and business publications
- `tech_media`: Technology-focused media outlets
- `news_sites`: General news sites with tech sections

### AI Keywords (Configurable)

Define regular expression patterns for detecting AI-related content. These patterns are case-insensitive.

```yaml
ai_keywords:
  - "\\bAI\\b"                           # Exact match for "AI"
  - "\\bartifici[eë]le intelligentie\\b" # Dutch: artificial intelligence
  - "\\bkunstmatige intelligentie\\b"    # Dutch: artificial intelligence
  - "\\bmachine learning\\b"             # Machine learning
  - "\\bdeep learning\\b"                # Deep learning
  - "\\balgoritm[e|es]\\b"              # Algorithm(s) in Dutch
  - "\\bChatGPT\\b"                     # ChatGPT
  - "\\bGPT\\b"                         # GPT models
  - "\\bLLM\\b"                         # Large Language Models
  - "\\blarge language model\\b"         # Large Language Models (full)
  - "\\bneural[e]? net\\w*\\b"          # Neural networks
  - "\\bdata scien\\w*\\b"              # Data science variations
  - "\\bautomatis\\w*\\b"               # Automation variations
```

**Pattern Guidelines:**
- Use `\\b` for word boundaries to avoid partial matches
- Include Dutch and English variations
- Use character classes `[eë]` for Dutch characters
- Use quantifiers `\\w*` for word variations
- Test patterns with sample text before deployment

### Topic Patterns (Configurable)

Define topic categorization using keyword patterns. Each topic maps to a list of detection keywords.

```yaml
topic_patterns:
  "AI in de zorg":
    - "zorg"
    - "gezondheid"
    - "ziekenhuis"
    - "patient"
    - "diagnos"
  
  "AI en privacy":
    - "privacy"
    - "AVG"
    - "GDPR"
    - "persoonsgegevens"
    - "data protection"
  
  "AI in het onderwijs":
    - "onderwijs"
    - "school"
    - "student"
    - "leren"
    - "educatie"
  
  "AI en werkgelegenheid":
    - "banen"
    - "werkgelegenheid"
    - "arbeidsmarkt"
    - "werknemers"
  
  "AI-wetgeving":
    - "wetgeving"
    - "regulering"
    - "AI Act"
    - "toezicht"
    - "compliance"
  
  "AI in de rechtspraak":
    - "rechtspraak"
    - "rechtbank"
    - "juridisch"
    - "advocat"
  
  "Generative AI":
    - "generat"
    - "ChatGPT"
    - "GPT"
    - "LLM"
    - "chatbot"
  
  "AI-ethiek":
    - "ethiek"
    - "ethisch"
    - "discriminatie"
    - "bias"
    - "verantwoord"
  
  "AI in retail":
    - "retail"
    - "winkel"
    - "e-commerce"
    - "klant"
    - "verkoop"
  
  "AI in finance":
    - "bank"
    - "financi"
    - "verzekering"
    - "fintech"
    - "betaal"
```

**Topic Categories:**
- **Healthcare**: AI applications in medical field
- **Privacy**: Data protection and privacy concerns
- **Education**: AI in learning and educational institutions
- **Employment**: Impact on jobs and labor market
- **Legislation**: AI regulation and compliance
- **Legal**: AI in judicial system
- **Generative AI**: ChatGPT, LLMs, and generative models
- **Ethics**: Ethical considerations and bias issues
- **Retail**: E-commerce and customer applications
- **Finance**: Banking, fintech, and financial services

### Paywall Bypass

Configure services for bypassing paywalls when fetching article content.

```yaml
paywall_bypass:
  services:
    - url: "https://archive.ph"
      method: "POST"
      priority: 1
    - url: "https://1ft.io"
      method: "GET"
      priority: 2
    - url: "https://12ft.io"
      method: "GET"
      priority: 3
    - url: "https://web.archive.org"
      method: "GET"
      priority: 4
  retry_attempts: 3
  timeout: 30
```

**Service Configuration:**
- `url`: Archive service URL
- `method`: HTTP method ("GET" or "POST")
- `priority`: Service priority (1 = highest)
- `retry_attempts`: Number of retry attempts per service
- `timeout`: Request timeout in seconds

**Available Services:**
- **archive.ph**: Fast archiving service
- **1ft.io**: Paywall removal service  
- **12ft.io**: Alternative paywall bypass
- **web.archive.org**: Internet Archive Wayback Machine

## Environment Variables

Override configuration with environment variables:

```bash
export AI_MEDIA_CONFIG_PATH="/path/to/custom/config.yaml"
export AI_MEDIA_RATE_LIMIT="20"
export AI_MEDIA_TIMEOUT="60"
export AI_MEDIA_DEBUG="true"
```

## Validation

The configuration is validated using Pydantic models:

- **MediaSource**: Validates media source structure
- **PaywallService**: Validates paywall service configuration
- **Config**: Main configuration model with defaults

Invalid configurations fall back to embedded defaults with warnings logged.

## Performance Tuning

### Rate Limiting

Adjust concurrent request limits:

```yaml
rate_limit: 10  # Concurrent requests
timeout: 30     # Request timeout (seconds)
retry_attempts: 3  # Retry failed requests
```

### Memory Usage

For large-scale monitoring:

- Increase system memory allocation
- Adjust article retention period
- Limit concurrent source scanning

### Network Optimization

- Use local DNS resolver
- Configure HTTP connection pooling
- Implement request caching

## Security Considerations

### Access Control

- Restrict config file permissions: `chmod 600 config.yaml`
- Use environment variables for sensitive data
- Implement authentication for MCP server

### Content Filtering

- Validate RSS feed URLs
- Sanitize article content
- Filter malicious URLs

### Data Privacy

- Respect robots.txt files
- Implement rate limiting
- Avoid storing personal data

## Troubleshooting

### Common Configuration Issues

**Invalid YAML syntax:**
```bash
# Test YAML validity
python -c "import yaml; yaml.safe_load(open('config.yaml'))"
```

**Missing media sources:**
- Check RSS feed accessibility
- Verify URL formats
- Test with curl/wget

**Keyword detection issues:**
- Test regex patterns in isolation
- Check for typos in Dutch terms
- Validate with sample articles

### Debug Configuration

Enable debug mode for detailed logging:

```yaml
debug: true
log_level: "DEBUG"
```

### Configuration Validation

The server validates configuration on startup and reports issues:

```bash
uv run python -c "
from src.ai_media_monitor.core.config_loader import load_config
config = load_config()
print(f'Loaded {len(config.media_sources)} source categories')
print(f'AI keywords: {len(config.ai_keywords)}')
print(f'Topic patterns: {len(config.topic_patterns)}')
"
```

## Examples

### Minimal Configuration

```yaml
media_sources:
  newspapers:
    - name: "NRC"
      url: "https://www.nrc.nl"
      rss: "https://www.nrc.nl/rss/"

ai_keywords:
  - "\\bAI\\b"
  - "\\bkunstmatige intelligentie\\b"

topic_patterns:
  "AI algemeen":
    - "AI"
    - "kunstmatige intelligentie"
```

### Full Configuration

See the main `config.yaml` file for a complete configuration example with all available options.

### Custom Topic Categories

Add domain-specific topics:

```yaml
topic_patterns:
  "AI in agriculture":
    - "landbouw"
    - "precisielandbouw"
    - "gewasmonitoring"
  
  "AI in transport":
    - "transport"
    - "logistiek"
    - "autonome voertuigen"
    - "verkeer"
```

## Best Practices

1. **Start Simple**: Begin with basic configuration and expand gradually
2. **Test Changes**: Validate keyword patterns with sample content
3. **Monitor Performance**: Track scanning speed and resource usage
4. **Regular Updates**: Keep media sources and patterns current
5. **Backup Configuration**: Version control your config changes
6. **Security First**: Protect configuration files and credentials