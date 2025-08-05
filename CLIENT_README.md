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

**Stap 2: Gmail App Password instellen**

⚠️ **Belangrijk**: Je hebt een speciaal Gmail App Password nodig, niet je normale wachtwoord!

1. **Ga naar je Google Account**: https://myaccount.google.com
2. **Klik op "Security"** (of "Beveiliging" in Nederlands)
3. **Schakel 2-Factor Authentication in** (als nog niet gedaan):
   - Zoek naar "2-Step Verification" / "Verificatie in 2 stappen"
   - Volg de instructies om 2FA in te schakelen
4. **Genereer App Password**:
   - Ga terug naar Security pagina
   - Klik op "2-Step Verification" / "Verificatie in 2 stappen"
   - Scroll helemaal naar beneden naar "App passwords" / "App-wachtwoorden"
   - Als je dit niet ziet, ga direct naar: https://myaccount.google.com/apppasswords
5. **Maak nieuw App Password**:
   - Select app: "Mail"
   - Select device: "Other (Custom name)" → Type: "AI Media Monitor"
   - Klik "Generate" / "Genereren"
6. **Kopieer het App Password**:
   - Je krijgt een 16-karakter code (bijv: `abcd efgh ijkl mnop`)
   - **Kopieer deze code exact inclusief spaties**

**Stap 3: Bewerk .env bestand**
```bash
# Bewerk .env en vul in met je echte gegevens:
EMAIL_USERNAME=jouw.email@gmail.com
EMAIL_PASSWORD=het_app_password_van_stap_2
EMAIL_TO_ADDRESS=ontvanger@example.com  
EMAIL_TO_NAME=Ontvanger Naam
```

**Voorbeeld van correct ingevuld .env bestand:**
```bash
EMAIL_USERNAME=john.doe@gmail.com
EMAIL_PASSWORD=abcd efgh ijkl mnop
EMAIL_TO_ADDRESS=john.doe@company.com
EMAIL_TO_NAME=John Doe
```

**Stap 4: Test de configuratie**
```bash
# Test alleen email (geen bestanden opslaan)
uv run python client.py --action weekly-report --email-only

# Test volledig (bestanden + email)
uv run python client.py --action weekly-report --email
```

**✅ Succesvol als je ziet:**
```
✅ Email configuratie is geldig
✅ Email verzonden naar [jouw-email]
```

**❌ Foutmeldingen oplossen:**
- `Username and Password not accepted` → Gebruik App Password, niet normaal wachtwoord
- `2-Step Verification required` → Schakel 2FA in op je Google account
- `App passwords not available` → Controleer of je een persoonlijk Gmail account gebruikt (geen G Suite/Workspace)

**Voordelen van .env bestand:**
- ✅ Veiliger (niet in git)
- ✅ Eenvoudiger configuratie
- ✅ Automatische defaults voor SMTP
- ✅ Geen shell exports nodig

### 4. Automatisch Uitvoeren

**Dagelijkse Artikel Verzameling (Nieuwe Functie):**

Voor betere weekly reports worden dagelijks artikelen opgeslagen in database:

```bash
# Stap 1: Maak script uitvoerbaar
chmod +x /Users/joopsnijder/Projects/ai-media-monitor-mcp/scripts/daily_collection.sh

# Stap 2: Installeer dagelijkse cron job (6:00 AM)
echo "# AI Media Monitor - Daily Collection (every day at 6:00 AM)
0 6 * * * /Users/joopsnijder/Projects/ai-media-monitor-mcp/scripts/daily_collection.sh" | crontab -
```

**Wekelijkse Cron Job Setup (Aanbevolen):**

Voor automatische wekelijkse rapporten elke maandag om 9:00:

```bash
# Stap 1: Maak script uitvoerbaar
chmod +x /Users/joopsnijder/Projects/ai-media-monitor-mcp/scripts/weekly_report.sh

# Stap 2: Installeer wekelijkse cron job met email
echo "# AI Media Monitor - Weekly Report (every Monday at 9:00 AM)
0 9 * * 1 SEND_EMAIL=true /Users/joopsnijder/Projects/ai-media-monitor-mcp/scripts/weekly_report.sh" | cron_temp
crontab cron_temp && rm cron_temp

# Stap 3: Controleer installatie
crontab -l
```

**Test de cron job handmatig:**
```bash
# Test met email verzending
SEND_EMAIL=true ./scripts/weekly_report.sh

# Test zonder email (alleen bestanden)
./scripts/weekly_report.sh
```

**Cron Job Management:**
```bash
# Bekijk huidige cron jobs
crontab -l

# Bewerk cron jobs handmatig
crontab -e

# Verwijder alle cron jobs (voorzichtig!)
crontab -r
```

**Logs controleren:**
- Logs worden opgeslagen in `logs/weekly_report_YYYYMMDD_HHMMSS.log`
- Check logs na uitvoering: `ls -la logs/`
- Bekijk laatste log: `tail -f logs/weekly_report_*.log`

**Wat gebeurt er elke maandag om 9:00:**
1. 🔄 Script start automatisch via cron
2. 📦 Dependencies worden gesynchroniseerd
3. 🔍 Nederlandse media bronnen worden gescand voor AI-gerelateerde artikelen
4. 📊 Trending topics en podcast suggesties worden geanalyseerd
5. 📧 Email wordt verzonden naar geconfigureerde ontvanger
6. 📝 Backup bestanden worden opgeslagen in `reports/` directory
7. 📋 Uitgebreide logs worden bewaard in `logs/` directory

**Verwachte resultaten:**
- ✅ Email met HTML rapport + Markdown bijlage
- ✅ JSON + Markdown bestanden in `reports/`
- ✅ Succesvolle uitvoering gelogd met timestamps

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