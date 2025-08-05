# Logging in AI Media Monitor

Het AI Media Monitor systeem gebruikt gestandaardiseerde Python logging voor troubleshooting en monitoring.

## 📋 Log Systemen

### 1. Python Application Logs
- **Locatie**: `logs/daily_collection_YYYYMMDD_HHMMSS.log`
- **Format**: `YYYY-MM-DD HH:MM:SS - logger_name - LEVEL - message`
- **Inhoud**: Gedetailleerde applicatie informatie, statistics, errors

**Voorbeeld:**
```
2025-08-05 21:58:21 - daily_collection - INFO - Starting daily article collection
2025-08-05 21:58:37 - daily_collection - INFO - Found 10 potential articles to process
2025-08-05 21:58:37 - daily_collection - INFO - Storage complete: 3 new, 7 duplicates
```

### 2. Shell Script Logs  
- **Locatie**: `logs/daily_collection_YYYYMMDD_HHMMSS.log` (andere timestamp)
- **Format**: `[YYYY-MM-DD HH:MM:SS] message`
- **Inhoud**: Script-level operaties, dependency syncing, cleanup

**Voorbeeld:**
```
[2025-08-05 21:59:01] Starting daily AI article collection...
[2025-08-05 21:59:01] Syncing dependencies...
[2025-08-05 21:59:19] SUCCESS: Daily article collection completed
```

## 🔍 Log Levels

- **DEBUG**: Gedetailleerde informatie voor troubleshooting
- **INFO**: Algemene operationele informatie
- **WARNING**: Niet-kritieke problemen  
- **ERROR**: Fouten die aandacht vereisen
- **CRITICAL**: Ernstige fouten die het systeem stoppen

## 📊 Statistics Logging

Elke run genereert een gestructureerd statistics blok:

```
=== STATISTICS ===
New articles stored: 3
Duplicate articles skipped: 7
Processing errors: 0
Total articles in database: 11
Active sources (last 7 days): 5
==================
```

## 🚨 Error Handling

Bij fouten worden volledige tracebacks gelogd:

```python
# Voorbeeld error log
2025-08-05 21:58:37 - daily_collection - ERROR - Critical error during daily collection: Connection failed
Traceback (most recent call last):
  File "client.py", line 135, in daily_collect_articles
    scan_data = await self.scan_media_sources(hours_back=24)
  ...
```

## 📁 Log Beheer

### Automatische Cleanup
- **Python logs**: Automatisch aangemaakt per run
- **Shell logs**: 30 dagen retentie via script cleanup
- **Database cleanup**: 90 dagen artikel retentie

### Log Monitoring

**Bekijk laatste logs:**
```bash
# Python application log
tail -f logs/daily_collection_*.log | grep -v DEBUG

# Shell script log  
tail -f logs/daily_collection_*.log | grep "^\[2025"

# Alle errors
grep -i error logs/daily_collection_*.log
```

**Database status:**
```bash
uv run python -c "
from src.ai_media_monitor.storage.database import ArticleDatabase
db = ArticleDatabase()
info = db.get_database_info()
print(f'Database: {info[\"total_articles\"]} artikelen')
print(f'Bronnen: {list(info[\"sources\"].keys())}')
"
```

## 🛠️ Troubleshooting

### Veel Voorkomende Problemen

**1. RSS Feed Errors**
```
ERROR - Error processing Volkskrant: HTTP 403 Forbidden
```
- **Oorzaak**: Feed geblokkeerd of rate limited
- **Oplossing**: Controleer RSS URL, wacht met retry

**2. Database Locked**
```  
ERROR - Error storing article: database is locked
```
- **Oorzaak**: Concurrent database access
- **Oplossing**: Script draait mogelijk al, check processen

**3. Network Timeouts**
```
ERROR - Failed to fetch https://...: timeout
```
- **Oorzaak**: Trage internetverbinding  
- **Oplossing**: Verhoog timeout in configuratie

### Debug Mode

Voor extra debug informatie:

```python
# In code - verhoog log level
logger.setLevel(logging.DEBUG)

# Of via environment variable
export DEBUG=1
```

## 📈 Monitoring Tips

1. **Daily Checks**: Controleer logs na 6:00 AM voor succesvolle runs
2. **Weekly Reviews**: Bekijk error patterns en source coverage  
3. **Database Growth**: Monitor artikel groei per bron
4. **Performance**: Let op scan durations en timeout errors

## 🔧 Log Configuration

De logging configuratie staat in `src/ai_media_monitor/utils/logging_config.py` en kan worden aangepast voor verschillende use cases.