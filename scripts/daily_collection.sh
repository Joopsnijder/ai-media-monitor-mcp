#!/bin/bash

# Daily Article Collection Script
# This script collects AI articles daily and stores them in SQLite database.
# 
# Add to crontab for daily execution:
# 0 6 * * * /path/to/ai-media-monitor-mcp/scripts/daily_collection.sh

set -euo pipefail

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

# Create logs directory
LOG_DIR="$PROJECT_DIR/logs"
mkdir -p "$LOG_DIR"

# Log file with timestamp
LOG_FILE="$LOG_DIR/daily_collection_$(date +%Y%m%d_%H%M%S).log"

# Logging function
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# Error handling
handle_error() {
    local exit_code=$?
    log "ERROR: Daily collection failed with exit code $exit_code"
    exit $exit_code
}

trap 'handle_error' ERR

log "Starting daily AI article collection..."

# Change to project directory
cd "$PROJECT_DIR"

# Check if virtual environment exists and uv is available
if ! command -v uv &> /dev/null; then
    log "ERROR: uv is not installed. Please install uv first."
    exit 1
fi

# Sync dependencies
log "Syncing dependencies..."
uv sync >> "$LOG_FILE" 2>&1

# Run the daily collection
log "Collecting articles from media sources..."

# Use client.py with new daily-collect action
# Note: Python logging will create its own detailed log file
# This bash log captures script-level operations
if uv run python client.py --action daily-collect; then
    log "SUCCESS: Daily article collection completed"
else
    log "ERROR: Failed to collect articles"
    exit 1
fi

# Cleanup old log files (keep last 30 days)
log "Cleaning up old log files..."
find "$LOG_DIR" -name "daily_collection_*.log" -mtime +30 -delete 2>/dev/null || true

# Database cleanup (keep last 90 days of articles)
log "Cleaning up old articles from database..."
uv run python -c "
from src.ai_media_monitor.storage.database import ArticleDatabase
db = ArticleDatabase()
deleted = db.cleanup_old_articles(days_to_keep=90)
print(f'Cleaned up {deleted} old articles')
" >> "$LOG_FILE" 2>&1

log "Daily collection process completed successfully"

# Show final stats
uv run python -c "
from src.ai_media_monitor.storage.database import ArticleDatabase
db = ArticleDatabase()
info = db.get_database_info()
print(f'Database now contains {info[\"total_articles\"]} articles from {len(info[\"sources\"])} sources')
" >> "$LOG_FILE" 2>&1