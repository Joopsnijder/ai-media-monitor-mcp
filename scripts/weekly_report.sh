#!/bin/bash
#
# Weekly AI Media Monitor Report Generator
# 
# This script generates a weekly report using the MCP client.
# Can be run manually or scheduled via cron.
#
# Example cron entry (runs every Monday at 9 AM):
# 0 9 * * 1 /path/to/ai-media-monitor-mcp/scripts/weekly_report.sh
#

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

# Change to project directory
cd "$PROJECT_DIR"

# Set up logging
LOG_DIR="$PROJECT_DIR/logs"
mkdir -p "$LOG_DIR"
LOG_FILE="$LOG_DIR/weekly_report_$(date +%Y%m%d_%H%M%S).log"

# Function to log with timestamp
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# Email configuration (set to true to enable email reports)
SEND_EMAIL=${SEND_EMAIL:-false}

log "Starting weekly AI media report generation..."

# Check if uv is available
if ! command -v uv &> /dev/null; then
    log "ERROR: uv not found. Please install uv first."
    exit 1
fi

# Sync dependencies
log "Syncing dependencies..."
if [ "$SEND_EMAIL" = "true" ]; then
    log "Installing email dependencies..."
    uv sync --extra email >> "$LOG_FILE" 2>&1
else
    uv sync >> "$LOG_FILE" 2>&1
fi

if [ $? -ne 0 ]; then
    log "ERROR: Failed to sync dependencies"
    exit 1
fi

# Generate the weekly report
log "Generating weekly report..."

if [ "$SEND_EMAIL" = "true" ]; then
    # Generate and send via email
    log "Generating report with email sending enabled..."
    uv run python client.py --action weekly-report --email >> "$LOG_FILE" 2>&1
else
    # Just generate and save
    log "Generating report (saving to file only)..."
    uv run weekly-report >> "$LOG_FILE" 2>&1
fi

if [ $? -eq 0 ]; then
    log "SUCCESS: Weekly report generated successfully"
    
    if [ "$SEND_EMAIL" = "true" ]; then
        log "Email report sent (if email configuration is correct)"
    else
        # Find the most recent report file
        LATEST_REPORT=$(find "$PROJECT_DIR/reports" -name "ai_media_report_*.md" -type f -printf '%T+ %p\n' 2>/dev/null | sort -r | head -n1 | cut -d' ' -f2-)
        
        if [ -n "$LATEST_REPORT" ]; then
            log "Report saved: $LATEST_REPORT"
        fi
    fi
else
    log "ERROR: Failed to generate weekly report"
    exit 1
fi

log "Weekly report generation completed"