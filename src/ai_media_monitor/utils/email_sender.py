"""Email functionality for AI Media Monitor reports.

This module is kept separate from other utils to avoid circular imports.
"""

import os
import smtplib
from datetime import datetime
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
from typing import Any

import yaml
from dotenv import load_dotenv


class EmailSender:
    """Handle email sending for AI Media Monitor reports."""

    def __init__(self, config_path: str = "config/email_config.yaml"):
        """Initialize email sender with configuration."""
        # Load .env file first
        load_dotenv()
        
        self.config_path = config_path
        self.config = self._load_config()

    def _load_config(self) -> dict[str, Any]:
        """Load email configuration from YAML file."""
        config_file = Path(self.config_path)

        if not config_file.exists():
            raise FileNotFoundError(
                f"Email config file not found: {config_file}\n"
                f"Please copy config/email_config.yaml.example to {config_file} and configure it."
            )

        with open(config_file, encoding='utf-8') as f:
            config = yaml.safe_load(f)

        # Replace environment variables in config
        config = self._replace_env_vars(config)

        return config

    def _replace_env_vars(self, obj: Any) -> Any:
        """Recursively replace ${VAR} patterns with environment variables."""
        if isinstance(obj, dict):
            return {k: self._replace_env_vars(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._replace_env_vars(item) for item in obj]
        elif isinstance(obj, str) and obj.startswith("${") and obj.endswith("}"):
            env_var = obj[2:-1]
            
            # Get environment variable with sensible defaults
            defaults = {
                "EMAIL_SMTP_SERVER": "smtp.gmail.com",
                "EMAIL_SMTP_PORT": "587",
                "EMAIL_USE_TLS": "true",
                "EMAIL_FROM_NAME": "AI Media Monitor"
            }
            
            value = os.getenv(env_var, defaults.get(env_var, obj))
            
            # Convert port to int and use_tls to boolean
            if env_var == "EMAIL_SMTP_PORT":
                try:
                    return int(value)
                except (ValueError, TypeError):
                    return 587
            elif env_var == "EMAIL_USE_TLS":
                return value.lower() in ("true", "1", "yes", "on")
            
            return value
        else:
            return obj

    def _generate_html_content(self, report_data: dict[str, Any]) -> str:
        """Generate HTML email content from report data."""
        # Get basic statistics
        stats = report_data.get('statistics', {})
        week_number = datetime.now().isocalendar()[1]
        year = datetime.now().year

        # Generate highlights HTML
        highlights_html = self._generate_highlights_html(report_data.get('highlights', {}))

        # Generate trending topics HTML
        trending_topics_html = self._generate_trending_topics_html(
            report_data.get('trends', {}).get('topics', [])
        )

        # Generate experts HTML
        experts_html = self._generate_experts_html(
            report_data.get('experts', {}).get('experts', [])
        )

        # Generate suggestions HTML
        suggestions_html = self._generate_suggestions_html(
            report_data.get('suggestions', {}).get('suggestions', [])
        )

        # Fill template
        html_template = self.config['email']['html_template']
        html_content = html_template.format(
            week_number=week_number,
            year=year,
            trending_topics_count=stats.get('trending_topics_count', 0),
            experts_count=stats.get('identified_experts_count', 0),
            suggestions_count=stats.get('topic_suggestions_count', 0),
            generation_date=datetime.now().strftime('%d-%m-%Y %H:%M'),
            highlights_html=highlights_html,
            trending_topics_html=trending_topics_html,
            experts_html=experts_html,
            suggestions_html=suggestions_html
        )

        return html_content

    def _generate_highlights_html(self, highlights: dict[str, Any]) -> str:
        """Generate HTML for highlights section."""
        if not highlights:
            return ""

        html = ['<div class="highlights">', '<h2>🌟 Highlights</h2>']

        top_topic = highlights.get('top_trending_topic')
        if top_topic:
            html.append('<div class="topic">')
            html.append(f'<h3>🔥 Top Trending: {top_topic.get("topic", "N/A")}</h3>')
            html.append(f'<p><strong>Vermeldingen:</strong> {top_topic.get("mentions", 0)}</p>')
            html.append(f'<p><strong>Sentiment:</strong> {top_topic.get("sentiment", "neutral")}</p>')
            html.append(f'<p><strong>Invalshoek:</strong> {top_topic.get("suggested_angle", "N/A")}</p>')
            html.append('</div>')

        top_expert = highlights.get('most_quoted_expert')
        if top_expert:
            html.append('<div class="expert">')
            html.append(f'<h3>👤 Top Expert: {top_expert.get("name", "N/A")}</h3>')
            org = top_expert.get('organization')
            if org:
                html.append(f'<p><strong>Organisatie:</strong> {org}</p>')
            html.append(f'<p><strong>Recente quotes:</strong> {top_expert.get("recent_quotes", 0)}</p>')
            html.append('</div>')

        html.append('</div>')
        return '\n'.join(html)

    def _generate_trending_topics_html(self, topics: list[dict[str, Any]]) -> str:
        """Generate HTML for trending topics section."""
        if not topics:
            return ""

        html = ['<div class="trending-topics">', '<h2>📈 Trending Topics</h2>']

        for i, topic in enumerate(topics[:5], 1):
            html.append('<div class="topic">')
            html.append(f'<h3>{i}. {topic.get("topic", "N/A")}</h3>')
            html.append(f'<p><strong>Vermeldingen:</strong> {topic.get("mentions", 0)}</p>')
            html.append(f'<p><strong>Bronnen:</strong> {", ".join(topic.get("sources", []))}</p>')
            html.append(f'<p><strong>Sentiment:</strong> {topic.get("sentiment", "neutral")}</p>')

            key_articles = topic.get('key_articles', [])
            if key_articles:
                html.append('<p><strong>Belangrijke artikelen:</strong></p>')
                html.append('<ul>')
                for article in key_articles[:3]:
                    title = article.get('title', 'N/A')
                    url = article.get('url', '#')
                    source = article.get('source', 'N/A')
                    html.append(f'<li><a href="{url}">{title}</a> - <em>{source}</em></li>')
                html.append('</ul>')

            html.append('</div>')

        html.append('</div>')
        return '\n'.join(html)

    def _generate_experts_html(self, experts: list[dict[str, Any]]) -> str:
        """Generate HTML for experts section."""
        if not experts:
            return "<div><h2>👥 Expert Aanbevelingen</h2><p>Geen experts gevonden deze periode.</p></div>"

        html = ['<div class="experts">', '<h2>👥 Expert Aanbevelingen</h2>']

        for i, expert in enumerate(experts[:5], 1):
            html.append('<div class="expert">')
            html.append(f'<h3>{i}. {expert.get("name", "N/A")}</h3>')

            org = expert.get('organization')
            if org:
                html.append(f'<p><strong>Organisatie:</strong> {org}</p>')

            expertise = expert.get('expertise', [])
            if expertise:
                html.append(f'<p><strong>Expertise:</strong> {", ".join(expertise)}</p>')

            html.append(f'<p><strong>Recente quotes:</strong> {expert.get("recent_quotes", 0)}</p>')

            contact_hints = expert.get('contact_hints', [])
            if contact_hints:
                html.append(f'<p><strong>Contact:</strong> {", ".join(contact_hints)}</p>')

            html.append('</div>')

        html.append('</div>')
        return '\n'.join(html)

    def _generate_suggestions_html(self, suggestions: list[dict[str, Any]]) -> str:
        """Generate HTML for suggestions section."""
        if not suggestions:
            return ""

        html = ['<div class="suggestions">', '<h2>💡 Podcast Topic Suggesties</h2>']

        for i, suggestion in enumerate(suggestions[:5], 1):
            html.append('<div class="topic">')
            html.append(f'<h3>{i}. {suggestion.get("topic", "N/A")}</h3>')
            html.append(f'<p><strong>Relevantie Score:</strong> {suggestion.get("relevance_score", 0):.1f}/10</p>')
            html.append(f'<p><strong>Reden:</strong> {suggestion.get("reason", "N/A")}</p>')
            html.append(f'<p><strong>Unieke Invalshoek:</strong> {suggestion.get("unique_angle", "N/A")}</p>')

            questions = suggestion.get('questions', [])
            if questions:
                html.append('<p><strong>Voorgestelde Vragen:</strong></p>')
                html.append('<ul>')
                for question in questions:
                    html.append(f'<li>{question}</li>')
                html.append('</ul>')

            html.append('</div>')

        html.append('</div>')
        return '\n'.join(html)

    async def send_report_email(
        self,
        report_data: dict[str, Any],
        markdown_file: Path | None = None,
        json_file: Path | None = None
    ) -> bool:
        """Send weekly report via email."""
        try:
            # Create message
            msg = MIMEMultipart('alternative')

            # Set headers
            week_number = datetime.now().isocalendar()[1]
            subject = self.config['email']['subject'].format(week_number=week_number)

            msg['Subject'] = subject
            msg['From'] = f"{self.config['email']['from_name']} <{self.config['email']['from_email']}>"
            msg['To'] = f"{self.config['email']['to_name']} <{self.config['email']['to_email']}>"

            # Generate HTML content
            html_content = self._generate_html_content(report_data)

            # Add HTML part
            html_part = MIMEText(html_content, 'html', 'utf-8')
            msg.attach(html_part)

            # Add attachments if requested
            attachments_config = self.config.get('attachments', {})

            if attachments_config.get('include_markdown', True) and markdown_file and markdown_file.exists():
                with open(markdown_file, 'rb') as f:
                    attachment = MIMEApplication(f.read(), _subtype='markdown')
                    attachment.add_header(
                        'Content-Disposition',
                        'attachment',
                        filename=f'ai_media_rapport_{week_number}.md'
                    )
                    msg.attach(attachment)

            if attachments_config.get('include_json', False) and json_file and json_file.exists():
                with open(json_file, 'rb') as f:
                    attachment = MIMEApplication(f.read(), _subtype='json')
                    attachment.add_header(
                        'Content-Disposition',
                        'attachment',
                        filename=f'ai_media_data_{week_number}.json'
                    )
                    msg.attach(attachment)

            # Send email
            smtp_config = self.config['smtp']

            with smtplib.SMTP(smtp_config['server'], smtp_config['port']) as server:
                if smtp_config.get('use_tls', True):
                    server.starttls()

                server.login(smtp_config['username'], smtp_config['password'])

                text = msg.as_string()
                server.sendmail(
                    smtp_config['username'],
                    [self.config['email']['to_email']],
                    text
                )

            print(f"✅ Email verzonden naar {self.config['email']['to_email']}")
            return True

        except Exception as e:
            print(f"❌ Fout bij versturen email: {e}")
            return False

    def validate_config(self) -> bool:
        """Validate email configuration."""
        try:
            required_fields = [
                ['smtp', 'server'],
                ['smtp', 'port'],
                ['smtp', 'username'],
                ['smtp', 'password'],
                ['email', 'to_email']
            ]

            for field_path in required_fields:
                current = self.config
                for field in field_path:
                    if field not in current:
                        print(f"❌ Ontbrekend veld in email config: {'.'.join(field_path)}")
                        return False
                    current = current[field]

                if not current or (isinstance(current, str) and current.startswith('${')):
                    print(f"❌ Lege waarde voor: {'.'.join(field_path)}")
                    return False

            print("✅ Email configuratie is geldig")
            return True

        except Exception as e:
            print(f"❌ Fout bij valideren email config: {e}")
            return False
