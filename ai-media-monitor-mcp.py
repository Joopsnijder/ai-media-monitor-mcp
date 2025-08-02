import asyncio
import aiohttp
import feedparser
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any
from collections import Counter
import re
import json
from urllib.parse import urljoin, urlparse
from fastmcp import FastMCP, Context
from pydantic import BaseModel, Field
import yaml
from bs4 import BeautifulSoup
import hashlib

# Initialize FastMCP server
mcp = FastMCP("AI Media Monitor", version="1.0.0")

# Configuration models
class MediaSource(BaseModel):
    name: str
    url: str
    rss: Optional[str] = None
    categories: List[str] = []

class PaywallService(BaseModel):
    url: str
    method: str = "GET"
    priority: int = 1

class Config(BaseModel):
    media_sources: Dict[str, List[MediaSource]]
    paywall_services: List[PaywallService]
    retry_attempts: int = 3
    timeout: int = 30
    rate_limit: int = 10

# Data models
class Article(BaseModel):
    title: str
    url: str
    source: str
    date: datetime
    content: Optional[str] = None
    summary: Optional[str] = None
    mentions_ai: bool = False
    ai_topics: List[str] = []
    quoted_experts: List[Dict[str, str]] = []

class TrendingTopic(BaseModel):
    topic: str
    mentions: int
    sources: List[str]
    sentiment: str = "neutral"
    key_articles: List[Article] = []
    suggested_angle: Optional[str] = None
    growth_percentage: Optional[float] = None

class Expert(BaseModel):
    name: str
    title: Optional[str] = None
    organization: Optional[str] = None
    expertise: List[str] = []
    recent_quotes: int = 0
    articles: List[Article] = []
    contact_hints: List[str] = []

class TopicSuggestion(BaseModel):
    topic: str
    relevance_score: float
    reason: str
    potential_guests: List[Expert] = []
    unique_angle: str
    questions: List[str] = []

# Load configuration
def load_config() -> Config:
    """Load configuration from file or use defaults"""
    default_config = {
        "media_sources": {
            "newspapers": [
                {"name": "NRC", "url": "https://www.nrc.nl", "rss": "https://www.nrc.nl/rss/"},
                {"name": "Volkskrant", "url": "https://www.volkskrant.nl", "rss": "https://www.volkskrant.nl/voorpagina/rss.xml"},
                {"name": "FD", "url": "https://fd.nl", "rss": "https://fd.nl/rss"},
                {"name": "Telegraaf", "url": "https://www.telegraaf.nl", "rss": "https://www.telegraaf.nl/rss"},
                {"name": "AD", "url": "https://www.ad.nl", "rss": "https://www.ad.nl/tech/rss.xml"},
                {"name": "Trouw", "url": "https://www.trouw.nl", "rss": "https://www.trouw.nl/cs-b7d0a82a.xml"}
            ],
            "trade_publications": [
                {"name": "Computable", "url": "https://www.computable.nl", "rss": "https://www.computable.nl/rss/nieuws.xml"},
                {"name": "AG Connect", "url": "https://www.agconnect.nl"},
                {"name": "MT/Sprout", "url": "https://www.mt.nl", "rss": "https://www.mt.nl/feed"},
                {"name": "Emerce", "url": "https://www.emerce.nl", "rss": "https://www.emerce.nl/feed"}
            ],
            "tech_media": [
                {"name": "Tweakers", "url": "https://tweakers.net", "rss": "https://feeds.feedburner.com/tweakers/mixed"},
                {"name": "Bright", "url": "https://www.bright.nl", "rss": "https://www.bright.nl/rss"},
                {"name": "Dutch IT Channel", "url": "https://dutchitchannel.nl", "rss": "https://dutchitchannel.nl/feed"}
            ],
            "news_sites": [
                {"name": "NU.nl", "url": "https://www.nu.nl", "rss": "https://www.nu.nl/rss/Tech"},
                {"name": "RTL Nieuws", "url": "https://www.rtlnieuws.nl", "rss": "https://www.rtlnieuws.nl/rss.xml"},
                {"name": "NOS", "url": "https://nos.nl", "rss": "https://feeds.nos.nl/nosnieuwstech"}
            ]
        },
        "paywall_services": [
            {"url": "https://archive.ph", "method": "POST", "priority": 1},
            {"url": "https://1ft.io", "method": "GET", "priority": 2},
            {"url": "https://12ft.io", "method": "GET", "priority": 3},
            {"url": "https://web.archive.org/save", "method": "GET", "priority": 4}
        ],
        "retry_attempts": 3,
        "timeout": 30,
        "rate_limit": 10
    }
    
    # Try to load from config.yaml if it exists
    try:
        with open("config.yaml", "r") as f:
            config_data = yaml.safe_load(f)
            return Config(**config_data)
    except:
        return Config(**default_config)

# Global config
config = load_config()

# Helper functions
def is_ai_related(text: str) -> bool:
    """Check if text contains AI-related keywords"""
    ai_keywords = [
        r'\bAI\b', r'\bartifici[eë]le intelligentie\b', r'\bkunstmatige intelligentie\b',
        r'\bmachine learning\b', r'\bdeep learning\b', r'\balgoritm[e|es]\b',
        r'\bChatGPT\b', r'\bGPT\b', r'\bLLM\b', r'\blarge language model\b',
        r'\bneural[e]? net\w*\b', r'\bdata scien\w*\b', r'\bautomatis\w*\b'
    ]
    
    text_lower = text.lower()
    return any(re.search(pattern, text_lower, re.IGNORECASE) for pattern in ai_keywords)

def extract_ai_topics(text: str) -> List[str]:
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
        "AI in finance": [r"bank", r"financi", r"verzekering", r"fintech", r"betaal"]
    }
    
    found_topics = []
    text_lower = text.lower()
    
    for topic, patterns in topic_patterns.items():
        if any(re.search(pattern, text_lower) for pattern in patterns):
            found_topics.append(topic)
    
    return found_topics

def extract_quotes_and_experts(content: str) -> List[Dict[str, str]]:
    """Extract quotes and expert names from article content"""
    experts = []
    
    # Patterns for finding quotes and attributions
    quote_patterns = [
        r'"([^"]+)"[,\s]*(?:zegt|aldus|volgens)\s+([A-Z][a-zA-Z\s\.]+?)(?:\.|,)',
        r'([A-Z][a-zA-Z\s\.]+?)(?:\s+zegt|\s+stelt|\s+vindt)[:\s]*"([^"]+)"',
        r'Volgens\s+([A-Z][a-zA-Z\s\.]+?)[,\s]+"([^"]+)"'
    ]
    
    for pattern in quote_patterns:
        matches = re.finditer(pattern, content)
        for match in matches:
            if len(match.groups()) == 2:
                quote = match.group(1) if match.group(1)[0] == '"' else match.group(2)
                expert = match.group(2) if match.group(1)[0] == '"' else match.group(1)
                
                # Clean up expert name
                expert = expert.strip().rstrip('.,')
                
                # Filter out common false positives
                if len(expert.split()) <= 5 and not any(word in expert.lower() for word in ['het', 'de', 'een']):
                    experts.append({
                        "name": expert,
                        "quote": quote.strip('"')
                    })
    
    return experts

async def fetch_with_retry(session: aiohttp.ClientSession, url: str, retries: int = 3) -> Optional[str]:
    """Fetch URL with retry logic"""
    for attempt in range(retries):
        try:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=30)) as response:
                if response.status == 200:
                    return await response.text()
        except Exception as e:
            if attempt == retries - 1:
                print(f"Failed to fetch {url}: {e}")
            await asyncio.sleep(2 ** attempt)  # Exponential backoff
    return None

async def bypass_paywall(session: aiohttp.ClientSession, url: str) -> Optional[str]:
    """Try to bypass paywall using configured services"""
    for service in sorted(config.paywall_services, key=lambda x: x.priority):
        try:
            if service.url == "https://archive.ph":
                # Archive.ph requires special handling
                async with session.post(
                    f"{service.url}/submit/",
                    data={"url": url},
                    allow_redirects=False
                ) as response:
                    if response.status in [302, 301]:
                        archive_url = response.headers.get('Location')
                        if archive_url:
                            return await fetch_with_retry(session, archive_url)
            
            elif service.url == "https://web.archive.org/save":
                # Wayback Machine
                archive_url = f"https://web.archive.org/web/{url}"
                return await fetch_with_retry(session, archive_url)
            
            else:
                # Generic GET services like 12ft.io, 1ft.io
                bypass_url = f"{service.url}/{url}"
                return await fetch_with_retry(session, bypass_url)
                
        except Exception as e:
            print(f"Paywall bypass failed with {service.url}: {e}")
            continue
    
    return None

async def fetch_article_content(session: aiohttp.ClientSession, url: str) -> Optional[str]:
    """Fetch article content, using paywall bypass if needed"""
    # First try direct fetch
    content = await fetch_with_retry(session, url)
    
    if content and ("paywall" in content.lower() or "subscriber" in content.lower() or len(content) < 1000):
        # Likely paywalled, try bypass
        bypassed_content = await bypass_paywall(session, url)
        if bypassed_content:
            content = bypassed_content
    
    return content

async def parse_article(session: aiohttp.ClientSession, item: Dict, source_name: str) -> Optional[Article]:
    """Parse RSS item into Article object"""
    try:
        # Extract basic info
        title = item.get('title', '')
        url = item.get('link', '')
        
        # Skip if not AI-related
        if not is_ai_related(title + item.get('summary', '')):
            return None
        
        # Parse date
        date_str = item.get('published', item.get('updated', ''))
        try:
            date = datetime.strptime(date_str, '%a, %d %b %Y %H:%M:%S %z')
        except:
            date = datetime.now()
        
        # Fetch full content
        content = await fetch_article_content(session, url)
        
        # Extract AI topics and experts
        full_text = title + (content or item.get('summary', ''))
        ai_topics = extract_ai_topics(full_text)
        quoted_experts = extract_quotes_and_experts(content) if content else []
        
        return Article(
            title=title,
            url=url,
            source=source_name,
            date=date,
            content=content[:5000] if content else None,  # Limit content length
            summary=item.get('summary', ''),
            mentions_ai=True,
            ai_topics=ai_topics,
            quoted_experts=quoted_experts
        )
    except Exception as e:
        print(f"Error parsing article: {e}")
        return None

# MCP Tool implementations
@mcp.tool(
    name="scan_media_sources",
    description="Scan all configured Dutch media sources for AI-related articles"
)
async def scan_media_sources(ctx: Context, hours_back: int = 24) -> Dict[str, Any]:
    """Scan all media sources for recent AI articles"""
    articles = []
    since_date = datetime.now() - timedelta(hours=hours_back)
    
    async with aiohttp.ClientSession() as session:
        for category, sources in config.media_sources.items():
            for source_data in sources:
                source = MediaSource(**source_data)
                if not source.rss:
                    continue
                
                try:
                    # Fetch RSS feed
                    rss_content = await fetch_with_retry(session, source.rss)
                    if not rss_content:
                        continue
                    
                    # Parse feed
                    feed = feedparser.parse(rss_content)
                    
                    # Process entries
                    for entry in feed.entries[:20]:  # Limit to recent 20
                        article = await parse_article(session, entry, source.name)
                        if article and article.date >= since_date:
                            articles.append(article)
                    
                    # Rate limiting
                    await asyncio.sleep(0.5)
                    
                except Exception as e:
                    print(f"Error processing {source.name}: {e}")
    
    # Extract trending topics
    topic_counter = Counter()
    for article in articles:
        for topic in article.ai_topics:
            topic_counter[topic] += 1
    
    trending_topics = [
        {"topic": topic, "count": count}
        for topic, count in topic_counter.most_common(10)
    ]
    
    # Extract potential guests
    expert_counter = Counter()
    expert_details = {}
    for article in articles:
        for expert in article.quoted_experts:
            name = expert['name']
            expert_counter[name] += 1
            if name not in expert_details:
                expert_details[name] = {
                    "quotes": [],
                    "articles": []
                }
            expert_details[name]["quotes"].append(expert['quote'])
            expert_details[name]["articles"].append({
                "title": article.title,
                "source": article.source,
                "url": article.url
            })
    
    potential_guests = []
    for name, count in expert_counter.most_common(10):
        if count >= 2:  # Mentioned at least twice
            potential_guests.append({
                "name": name,
                "mentions": count,
                "recent_quotes": expert_details[name]["quotes"][:3],
                "articles": expert_details[name]["articles"][:3]
            })
    
    return {
        "scan_date": datetime.now().isoformat(),
        "hours_scanned": hours_back,
        "total_articles": len(articles),
        "articles": [article.dict() for article in articles[:50]],  # Limit response
        "trending_topics": trending_topics,
        "potential_guests": potential_guests
    }

@mcp.tool(
    name="get_trending_topics",
    description="Get trending AI topics in Dutch media with detailed analysis"
)
async def get_trending_topics(
    ctx: Context, 
    period: str = "week", 
    min_mentions: int = 3,
    categories: Optional[List[str]] = None
) -> Dict[str, List[TrendingTopic]]:
    """Analyze trending AI topics in Dutch media"""
    # Determine time period
    hours_map = {"day": 24, "week": 168, "month": 720}
    hours = hours_map.get(period, 168)
    
    # Get articles
    scan_result = await scan_media_sources(ctx, hours_back=hours)
    articles = [Article(**a) for a in scan_result["articles"]]
    
    # Group by topic
    topic_articles = {}
    topic_sources = {}
    
    for article in articles:
        for topic in article.ai_topics:
            if categories and topic not in categories:
                continue
                
            if topic not in topic_articles:
                topic_articles[topic] = []
                topic_sources[topic] = set()
            
            topic_articles[topic].append(article)
            topic_sources[topic].add(article.source)
    
    # Create trending topics
    trending = []
    for topic, articles_list in topic_articles.items():
        if len(articles_list) >= min_mentions:
            # Sort articles by date
            articles_list.sort(key=lambda x: x.date, reverse=True)
            
            # Determine sentiment (simplified)
            positive_words = ["succes", "doorbraak", "innovatie", "verbetering", "kans"]
            negative_words = ["risico", "gevaar", "probleem", "zorgen", "kritiek"]
            
            sentiment_score = 0
            for article in articles_list:
                text = (article.title + (article.summary or "")).lower()
                sentiment_score += sum(1 for word in positive_words if word in text)
                sentiment_score -= sum(1 for word in negative_words if word in text)
            
            sentiment = "positive" if sentiment_score > 0 else "negative" if sentiment_score < 0 else "neutral"
            
            # Create suggested angle based on content
            if "privacy" in topic.lower():
                angle = "Praktische oplossingen voor privacy-uitdagingen"
            elif "zorg" in topic.lower():
                angle = "Succesverhalen uit Nederlandse ziekenhuizen"
            elif "wetgeving" in topic.lower():
                angle = "Wat betekent nieuwe regelgeving voor jouw organisatie?"
            else:
                angle = f"De realiteit achter {topic} in Nederland"
            
            trending.append(TrendingTopic(
                topic=topic,
                mentions=len(articles_list),
                sources=list(topic_sources[topic]),
                sentiment=sentiment,
                key_articles=articles_list[:5],
                suggested_angle=angle,
                growth_percentage=None  # Would need historical data
            ))
    
    # Sort by mentions
    trending.sort(key=lambda x: x.mentions, reverse=True)
    
    return {
        "period": period,
        "topics": [t.dict() for t in trending]
    }

@mcp.tool(
    name="identify_experts",
    description="Identify potential podcast guests based on media coverage"
)
async def identify_experts(
    ctx: Context,
    topic: Optional[str] = None,
    period: str = "month",
    min_quotes: int = 2
) -> Dict[str, List[Expert]]:
    """Find experts quoted in Dutch media about AI topics"""
    hours_map = {"week": 168, "month": 720, "quarter": 2160}
    hours = hours_map.get(period, 720)
    
    # Get articles
    scan_result = await scan_media_sources(ctx, hours_back=hours)
    articles = [Article(**a) for a in scan_result["articles"]]
    
    # Filter by topic if specified
    if topic:
        articles = [a for a in articles if topic in a.ai_topics]
    
    # Collect expert information
    expert_data = {}
    
    for article in articles:
        for expert_quote in article.quoted_experts:
            name = expert_quote['name']
            
            if name not in expert_data:
                expert_data[name] = {
                    "quotes": [],
                    "articles": [],
                    "topics": set(),
                    "organizations": []
                }
            
            expert_data[name]["quotes"].append(expert_quote['quote'])
            expert_data[name]["articles"].append(article)
            expert_data[name]["topics"].update(article.ai_topics)
            
            # Try to extract organization from article
            org_pattern = rf"{name}[,\s]+(?:van|bij|CEO|CTO|directeur|professor|hoogleraar)\s+([A-Z][a-zA-Z\s]+)"
            org_match = re.search(org_pattern, article.content or article.summary or "")
            if org_match:
                expert_data[name]["organizations"].append(org_match.group(1))
    
    # Create Expert objects
    experts = []
    for name, data in expert_data.items():
        if len(data["quotes"]) >= min_quotes:
            # Determine title and organization
            organizations = list(set(data["organizations"]))
            organization = organizations[0] if organizations else None
            
            # Create contact hints
            contact_hints = []
            if organization:
                contact_hints.append(f"Via {organization}")
            contact_hints.append("LinkedIn zoeken op naam + AI")
            
            experts.append(Expert(
                name=name,
                organization=organization,
                expertise=list(data["topics"]),
                recent_quotes=len(data["quotes"]),
                articles=data["articles"][:5],
                contact_hints=contact_hints
            ))
    
    # Sort by number of quotes
    experts.sort(key=lambda x: x.recent_quotes, reverse=True)
    
    return {
        "period": period,
        "topic_filter": topic,
        "experts": [e.dict() for e in experts[:20]]  # Top 20
    }

@mcp.tool(
    name="generate_topic_suggestions",
    description="Generate podcast topic suggestions based on media trends"
)
async def generate_topic_suggestions(
    ctx: Context,
    focus_areas: Optional[List[str]] = None
) -> Dict[str, List[TopicSuggestion]]:
    """Generate actionable podcast topic suggestions"""
    # Get recent trends
    trends = await get_trending_topics(ctx, period="week", min_mentions=2)
    trending_topics = [TrendingTopic(**t) for t in trends["topics"]]
    
    # Get experts
    experts_result = await identify_experts(ctx, period="month", min_quotes=1)
    available_experts = [Expert(**e) for e in experts_result["experts"]]
    
    suggestions = []
    
    for trend in trending_topics[:10]:
        # Skip if not in focus areas
        if focus_areas and not any(area in trend.topic for area in focus_areas):
            continue
        
        # Find relevant experts
        topic_experts = [
            e for e in available_experts 
            if any(topic in e.expertise for topic in [trend.topic])
        ]
        
        # Calculate relevance score
        relevance_score = min(10, trend.mentions * 0.5 + len(topic_experts) * 2)
        
        # Generate questions based on topic
        questions = []
        if "privacy" in trend.topic.lower():
            questions = [
                "Hoe ga je praktisch om met privacy bij AI-implementaties?",
                "Wat zijn de grootste misverstanden over AI en privacy?",
                "Welke concrete stappen moet een organisatie zetten?"
            ]
        elif "zorg" in trend.topic.lower():
            questions = [
                "Wat zijn succesvolle AI-toepassingen in jullie ziekenhuis?",
                "Hoe krijg je artsen mee in AI-innovaties?",
                "Wat zijn de grootste uitdagingen bij AI in de zorg?"
            ]
        elif "wetgeving" in trend.topic.lower():
            questions = [
                "Wat betekent de AI Act concreet voor Nederlandse bedrijven?",
                "Waar moeten organisaties nu al mee beginnen?",
                "Welke sectoren worden het meest geraakt?"
            ]
        else:
            questions = [
                f"Wat is de realiteit van {trend.topic} in Nederland?",
                "Wat zijn de grootste uitdagingen die je tegenkomt?",
                "Welke kansen zie je voor de toekomst?"
            ]
        
        suggestion = TopicSuggestion(
            topic=trend.topic,
            relevance_score=relevance_score,
            reason=f"{trend.mentions} artikelen deze week, {len(topic_experts)} beschikbare experts",
            potential_guests=topic_experts[:3],
            unique_angle=trend.suggested_angle or f"Praktijkervaringen met {trend.topic}",
            questions=questions
        )
        
        suggestions.append(suggestion)
    
    # Sort by relevance
    suggestions.sort(key=lambda x: x.relevance_score, reverse=True)
    
    return {
        "generated_date": datetime.now().isoformat(),
        "suggestions": [s.dict() for s in suggestions]
    }

@mcp.tool(
    name="fetch_article",
    description="Fetch full content of a specific article, bypassing paywall if needed"
)
async def fetch_article(ctx: Context, url: str) -> Dict[str, Any]:
    """Fetch and analyze a specific article"""
    async with aiohttp.ClientSession() as session:
        content = await fetch_article_content(session, url)
        
        if content:
            # Extract metadata
            soup = BeautifulSoup(content, 'html.parser')
            
            # Try to find title
            title = ""
            if soup.find('h1'):
                title = soup.find('h1').get_text().strip()
            elif soup.find('title'):
                title = soup.find('title').get_text().strip()
            
            # Extract text content
            text_content = soup.get_text()
            
            # Analyze
            is_ai = is_ai_related(text_content)
            topics = extract_ai_topics(text_content) if is_ai else []
            experts = extract_quotes_and_experts(text_content) if is_ai else []
            
            return {
                "url": url,
                "title": title,
                "content_preview": text_content[:2000],
                "is_ai_related": is_ai,
                "ai_topics": topics,
                "quoted_experts": experts,
                "fetch_successful": True
            }
        else:
            return {
                "url": url,
                "fetch_successful": False,
                "error": "Could not fetch article content"
            }

@mcp.tool(
    name="get_weekly_report",
    description="Generate a comprehensive weekly report for AIToday Live podcast planning"
)
async def get_weekly_report(ctx: Context) -> Dict[str, Any]:
    """Generate weekly media monitoring report"""
    # Gather all data
    trends = await get_trending_topics(ctx, period="week")
    experts = await identify_experts(ctx, period="week", min_quotes=1)
    suggestions = await generate_topic_suggestions(ctx)
    
    # Create summary
    summary = {
        "report_date": datetime.now().isoformat(),
        "week_number": datetime.now().isocalendar()[1],
        "highlights": {
            "top_trending_topic": trends["topics"][0] if trends["topics"] else None,
            "most_quoted_expert": experts["experts"][0] if experts["experts"] else None,
            "best_topic_suggestion": suggestions["suggestions"][0] if suggestions["suggestions"] else None
        },
        "statistics": {
            "trending_topics_count": len(trends["topics"]),
            "identified_experts_count": len(experts["experts"]),
            "topic_suggestions_count": len(suggestions["suggestions"])
        },
        "trends": trends,
        "experts": experts,
        "suggestions": suggestions
    }
    
    return summary

# Run the server
if __name__ == "__main__":
    mcp.run()
