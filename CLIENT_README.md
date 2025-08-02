# AI Media Monitor MCP Client

De MCP client stelt je in staat om automatisch rapporten te genereren door de AI Media Monitor MCP server aan te roepen.

## Functionaliteit

De client kan verschillende acties uitvoeren:
- **Weekly Report**: Comprehensive wekelijks rapport met alle data
- **Scan**: Scan recente artikelen
- **Trends**: Analyseer trending topics
- **Experts**: Identificeer potentiële podcast gasten

## Installatie

Zorg ervoor dat alle dependencies geïnstalleerd zijn:

```bash
# Basis installatie
uv sync

# Met email functionaliteit
uv sync --extra email
```

## Gebruik

### 1. Handmatig Uitvoeren

**Wekelijks rapport genereren:**
```bash
uv run weekly-report
# Of expliciet:
uv run client --action weekly-report --format both
```

**Recente artikelen scannen:**
```bash
uv run client --action scan --hours 48 --format markdown
```

**Trending topics analyseren:**
```bash
uv run client --action trends --period week --format json
```

**Experts identificeren:**
```bash
uv run client --action experts --period month --format both
```

**Met email verzending:**
```bash
# Genereer rapport en verstuur via email
uv run client --action weekly-report --email

# Alleen email versturen (geen bestanden opslaan)
uv run client --action weekly-report --email-only
```

### 2. Opties

- `--action`: Actie om uit te voeren (`weekly-report`, `scan`, `trends`, `experts`)
- `--format`: Output formaat (`json`, `markdown`, `both`)
- `--hours`: Aantal uren terug te scannen (voor scan actie)
- `--period`: Periode voor trends/experts (`day`, `week`, `month`)
- `--output`: Specifiek output bestand (optioneel)
- `--email`: Verstuur rapport ook via email
- `--email-only`: Alleen email versturen, geen bestanden opslaan

### 3. Email Configuratie

Voor automatische email rapporten:

**Stap 1: Maak .env bestand**
```bash
# Kopieer het voorbeeld bestand
cp .env.example .env
```

**Stap 2: Gmail App Password**
1. Ga naar [Google Account](https://myaccount.google.com)
2. Schakel 2-Factor Authentication in
3. Ga naar "App passwords" 
4. Genereer een app password voor "Mail"
5. Kopieer het gegenereerde wachtwoord

**Stap 3: Bewerk .env bestand**
```bash
# Bewerk .env en vul in:
EMAIL_USERNAME=jouw.email@gmail.com
EMAIL_PASSWORD=jouw_app_password_hier
EMAIL_TO_ADDRESS=jouw.email@gmail.com
EMAIL_TO_NAME=Jouw Naam
```

**Stap 4: Testen**
```bash
uv run python client.py --action weekly-report --email
```

**Voordelen van .env bestand:**
- ✅ Veiliger (niet in git)
- ✅ Eenvoudiger configuratie
- ✅ Automatische defaults voor SMTP
- ✅ Geen shell exports nodig

### 4. Automatisch Uitvoeren

**Met cron (wekelijks op maandag om 9:00):**

```bash
# Bewerk crontab
crontab -e

# Voor alleen bestanden opslaan:
0 9 * * 1 /path/to/ai-media-monitor-mcp/scripts/weekly_report.sh

# Voor email verzending:
0 9 * * 1 SEND_EMAIL=true /path/to/ai-media-monitor-mcp/scripts/weekly_report.sh
```

**Met systemd timer (Ubuntu/Linux):**

1. Maak een service bestand:
```bash
sudo nano /etc/systemd/system/ai-media-report.service
```

```ini
[Unit]
Description=AI Media Monitor Weekly Report
After=network.target

[Service]
Type=oneshot
User=your_username
WorkingDirectory=/path/to/ai-media-monitor-mcp
ExecStart=/path/to/ai-media-monitor-mcp/scripts/weekly_report.sh
```

2. Maak een timer bestand:
```bash
sudo nano /etc/systemd/system/ai-media-report.timer
```

```ini
[Unit]
Description=Run AI Media Report weekly
Requires=ai-media-report.service

[Timer]
OnCalendar=Mon *-*-* 09:00:00
Persistent=true

[Install]
WantedBy=timers.target
```

3. Activeer de timer:
```bash
sudo systemctl enable ai-media-report.timer
sudo systemctl start ai-media-report.timer
```

## Output

### Bestandslocaties

Rapporten worden opgeslagen in de `reports/` directory:
- JSON: `ai_media_report_YYYYMMDD_HHMMSS.json`
- Markdown: `ai_media_report_YYYYMMDD_HHMMSS.md`

Logs worden opgeslagen in de `logs/` directory (bij gebruik van shell script).

### Rapport Inhoud

Een wekelijks rapport bevat:

1. **Summary Statistics**
   - Aantal trending topics
   - Aantal geïdentificeerde experts
   - Aantal topic suggesties

2. **Highlights**
   - Top trending topic met details
   - Meest geciteerde expert

3. **Trending Topics** (top 5)
   - Topic naam en aantal vermeldingen
   - Sentiment analyse
   - Key artikelen met bronnen

4. **Expert Recommendations** (top 5)
   - Naam en organisatie
   - Expertise gebieden
   - Contact informatie

5. **Podcast Topic Suggestions** (top 5)
   - Relevantie score
   - Unieke invalshoek
   - Voorgestelde vragen

## Troubleshooting

**Client kan geen verbinding maken:**
- Zorg ervoor dat de MCP server werkt: `uv run server`
- Check of alle dependencies geïnstalleerd zijn: `uv sync`

**Lege rapporten:**
- Verhoog de scan periode: `--hours 72` of `--period month`
- Check de RSS feeds in de configuratie

**Permission errors:**
- Zorg ervoor dat scripts uitvoerbaar zijn: `chmod +x scripts/*.sh`
- Check directory permissions voor `reports/` en `logs/`

## Voorbeelden

**Dagelijkse scan voor podcast voorbereiding:**
```bash
# Scan laatste 24 uur, markdown output
uv run client --action scan --hours 24 --format markdown

# Check trending topics van afgelopen week
uv run client --action trends --period week --format both
```

**Maandelijkse expert review:**
```bash
# Identificeer experts van afgelopen maand
uv run client --action experts --period month --format json
```

**Volledige wekelijkse analyse:**
```bash
# Genereer compleet rapport
uv run weekly-report
```

## Integratie

De client kan geïntegreerd worden met:
- **Email**: Stuur rapporten automatisch via mail
- **Slack/Teams**: Post rapporten in kanalen
- **Cloud Storage**: Upload naar Google Drive/Dropbox
- **CMS**: Automatisch publiceren op websites
- **Analytics**: Integratie met tracking tools

Zie `scripts/weekly_report.sh` voor voorbeelden van uitbreidingen.