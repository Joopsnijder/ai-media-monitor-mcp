# Development Guide

This guide covers development setup, architecture, and contribution guidelines for the AI Media Monitor MCP server.

## Development Setup

### Prerequisites

- Python 3.10 or higher
- [uv](https://github.com/astral-sh/uv) package manager
- Git

### Environment Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/ai-media-monitor-mcp.git
   cd ai-media-monitor-mcp
   ```

2. **Install dependencies:**
   ```bash
   uv sync --dev
   ```

3. **Activate virtual environment:**
   ```bash
   source .venv/bin/activate  # Linux/macOS
   # or
   .venv\Scripts\activate     # Windows
   ```

4. **Verify installation:**
   ```bash
   uv run test
   uv run lint
   ```

## Project Architecture

### Directory Structure

```
ai-media-monitor-mcp/
├── src/ai_media_monitor/        # Main package
│   ├── core/                    # Core functionality
│   │   ├── analyzer.py          # Media analysis engine
│   │   └── config_loader.py     # Configuration loading
│   ├── models/                  # Data models
│   │   ├── article.py           # Article data model
│   │   ├── config.py            # Configuration model
│   │   ├── expert.py            # Expert data model
│   │   └── topic.py             # Topic models
│   ├── utils/                   # Utility functions
│   │   ├── text_analysis.py     # Text processing
│   │   └── web_utils.py         # Web scraping utilities
│   └── __init__.py
├── tests/                       # Test suite
│   ├── fixtures/                # Test data
│   ├── integration/             # Integration tests
│   └── unit/                    # Unit tests
├── docs/                        # Documentation
├── config.yaml                  # Configuration file
├── server.py                    # MCP server entry point
├── pyproject.toml               # Project configuration
└── README.md                    # Main documentation
```

### Key Components

#### Core Components

**MediaAnalyzer** (`src/ai_media_monitor/core/analyzer.py`)
- Main analysis engine
- Orchestrates scanning, analysis, and reporting
- Manages async operations and error handling

**ConfigLoader** (`src/ai_media_monitor/core/config_loader.py`)
- Loads and validates configuration
- Provides fallback defaults
- Supports environment variable overrides

#### Data Models

**Article** (`src/ai_media_monitor/models/article.py`)
- Represents news articles with AI content
- Includes metadata, content, and analysis results

**Expert** (`src/ai_media_monitor/models/expert.py`)
- Represents identified AI experts
- Tracks quotes, topics, and media appearances

**TrendingTopic** (`src/ai_media_monitor/models/topic.py`)
- Represents trending AI topics
- Includes metrics and analysis data

#### Utilities

**TextAnalysis** (`src/ai_media_monitor/utils/text_analysis.py`)
- AI keyword detection
- Topic extraction
- Expert quote parsing

**WebUtils** (`src/ai_media_monitor/utils/web_utils.py`)
- RSS feed parsing
- Web scraping
- Paywall bypass functionality

## Development Workflow

### Code Quality Standards

The project enforces strict code quality:

```bash
# Linting (must pass)
uv run lint

# Auto-fix linting issues
uv run lint-fix

# Format code
uv run format

# Run tests
uv run test

# Type checking (via mypy in ruff)
uv run lint --select=E,F,W,I,B,C4,UP
```

### Pre-commit Hooks

Install pre-commit hooks for automatic code quality checks:

```bash
uv run pre-commit install
```

This ensures all commits meet quality standards.

### Testing Strategy

**Unit Tests**
- Test individual functions and classes
- Mock external dependencies
- Fast execution (< 1 second each)

**Integration Tests**
- Test MCP tool functionality
- Use real network requests (with mocking)
- Test configuration loading

**Fixtures**
- Sample RSS feeds
- Mock HTTP responses  
- Test configuration data

### Running Tests

```bash
# All tests
uv run test

# Specific test file
uv run pytest tests/unit/test_text_analysis.py

# With coverage
uv run pytest --cov=src/ai_media_monitor

# Verbose output
uv run pytest -v
```

## Contributing Guidelines

### Code Style

**Python Style:**
- Follow PEP 8 (enforced by Ruff)
- Use type hints throughout
- Prefer `list[str]` over `List[str]` (modern Python)
- Use f-strings for string formatting

**Naming Conventions:**
- Functions: `snake_case`
- Classes: `PascalCase`
- Constants: `UPPER_CASE`
- Private methods: `_underscore_prefix`

**Documentation:**
- Docstrings for all public functions/classes
- Type hints for all parameters and returns
- Inline comments for complex logic

### Git Workflow

**Branch Naming:**
- `feature/description` - New features
- `fix/description` - Bug fixes
- `docs/description` - Documentation updates
- `refactor/description` - Code refactoring

**Commit Messages:**
```
type: brief description

More detailed explanation if needed.

- List specific changes
- Reference issues: #123
```

**Pull Request Process:**
1. Create feature branch from `main`
2. Make changes with tests
3. Ensure all checks pass
4. Submit PR with description
5. Address review feedback
6. Merge after approval

### Adding New Features

#### 1. Add New Media Source

1. **Update configuration:**
   ```yaml
   # config.yaml
   media_sources:
     new_category:
       - name: "Source Name"
         url: "https://example.com"
         rss: "https://example.com/rss"
   ```

2. **Test the source:**
   ```bash
   uv run python -c "
   from src.ai_media_monitor.core.analyzer import MediaAnalyzer
   analyzer = MediaAnalyzer()
   result = await analyzer.scan_media_sources()
   print(result)
   "
   ```

3. **Add tests:**
   ```python
   # tests/unit/test_new_source.py
   def test_new_source_parsing():
       # Test RSS parsing
       # Test content extraction
       pass
   ```

#### 2. Add New AI Topic Pattern

1. **Update configuration:**
   ```yaml
   # config.yaml
   topic_patterns:
     "New AI Topic":
       - "keyword1"
       - "keyword2"
   ```

2. **Test pattern matching:**
   ```python
   from src.ai_media_monitor.utils.text_analysis import extract_ai_topics
   
   test_text = "Sample article text with keywords"
   topics = extract_ai_topics(test_text)
   assert "New AI Topic" in topics
   ```

#### 3. Add New MCP Tool

1. **Define tool in server.py:**
   ```python
   @mcp.tool(
       name="new_tool",
       description="Description of what the tool does"
   )
   async def new_tool(ctx: Context, param: str) -> dict[str, Any]:
       """Tool implementation"""
       # Implementation here
       return {"result": "data"}
   ```

2. **Add to analyzer if needed:**
   ```python
   # src/ai_media_monitor/core/analyzer.py
   async def new_analysis_method(self, param: str) -> dict:
       """New analysis functionality"""
       pass
   ```

3. **Add comprehensive tests:**
   ```python
   # tests/integration/test_new_tool.py
   @pytest.mark.asyncio
   async def test_new_tool():
       # Test the tool functionality
       pass
   ```

4. **Update documentation:**
   - Add to `docs/API.md`
   - Update `README.md`
   - Add usage examples

### Code Review Checklist

**Functionality:**
- [ ] Code works as intended
- [ ] Edge cases handled
- [ ] Error handling implemented
- [ ] Performance considerations addressed

**Code Quality:**
- [ ] Follows project style guide
- [ ] Type hints present
- [ ] Docstrings added
- [ ] No code duplication

**Testing:**
- [ ] Unit tests added/updated
- [ ] Integration tests pass
- [ ] Test coverage adequate
- [ ] Edge cases tested

**Documentation:**
- [ ] README updated if needed
- [ ] API docs updated
- [ ] Code comments clear
- [ ] Examples provided

## Debugging

### Local Development

**Debug Mode:**
```bash
# Enable debug logging
export AI_MEDIA_DEBUG=true
uv run server
```

**Interactive Testing:**
```python
# Python REPL
import asyncio
from src.ai_media_monitor.core.analyzer import MediaAnalyzer

analyzer = MediaAnalyzer()
result = asyncio.run(analyzer.scan_media_sources(hours_back=1))
print(result)
```

**Configuration Testing:**
```bash
# Test configuration loading
uv run python -c "
from src.ai_media_monitor.core.config_loader import load_config
config = load_config()
print(f'Sources: {len(config.media_sources)}')
print(f'Keywords: {len(config.ai_keywords)}')
"
```

### Common Issues

**Import Errors:**
- Check Python path: `export PYTHONPATH=src:$PYTHONPATH`
- Verify virtual environment is activated
- Ensure dependencies are installed

**Network Issues:**
- Check RSS feed URLs are accessible
- Verify rate limiting configuration
- Test paywall bypass services

**Configuration Issues:**
- Validate YAML syntax
- Check file permissions
- Test with minimal configuration

### Performance Profiling

**Memory Usage:**
```bash
# Memory profiling
pip install memory-profiler
python -m memory_profiler server.py
```

**Async Performance:**
```python
import asyncio
import time

start = time.time()
result = await analyzer.scan_media_sources()
print(f"Scan took {time.time() - start:.2f} seconds")
```

## Release Process

### Version Management

1. **Update version in pyproject.toml**
2. **Create changelog entry**
3. **Tag release:**
   ```bash
   git tag v1.1.0
   git push origin v1.1.0
   ```

### Distribution

**Build package:**
```bash
uv build
```

**Test installation:**
```bash
pip install dist/ai_media_monitor_mcp-*.whl
```

## Contributing

### Getting Started

1. **Fork the repository**
2. **Set up development environment**
3. **Read existing code and tests**
4. **Start with small contributions**
5. **Ask questions in issues or discussions**

### Areas for Contribution

**High Priority:**
- Additional Dutch media sources
- Improved AI keyword patterns
- Performance optimizations
- Additional paywall bypass methods

**Medium Priority:**
- Enhanced topic categorization
- Sentiment analysis improvements
- Expert contact information extraction
- Multi-language support

**Documentation:**
- Usage examples
- Tutorial content
- API documentation improvements
- Configuration guides

### Support

- **Issues:** GitHub Issues for bugs and feature requests
- **Discussions:** GitHub Discussions for questions
- **Documentation:** Check existing docs first
- **Code:** Follow the style guide and add tests

---

Thank you for contributing to the AI Media Monitor! Your contributions help support the Dutch AI community and the AIToday Live podcast.