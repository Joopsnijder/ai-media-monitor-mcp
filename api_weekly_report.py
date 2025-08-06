#!/usr/bin/env python3
"""
Simple API endpoint for weekly report that only outputs JSON to stdout.
"""

import asyncio
import json
import sys
import os
import warnings

# Suppress all warnings and stderr output
warnings.filterwarnings('ignore')
sys.stderr = open(os.devnull, 'w')

# Set environment variable to suppress database debug output
os.environ['PYTHONHASHSEED'] = '0'

async def main():
    try:
        # Import the server function directly
        from server import get_weekly_report
        
        # Generate the report
        report_data = await get_weekly_report()
        
        # Output only JSON to stdout
        print(json.dumps(report_data, default=str, ensure_ascii=False))
        
    except Exception as e:
        # Restore stderr for error output
        sys.stderr = sys.__stderr__
        error_response = {
            "error": "Failed to generate weekly report",
            "details": str(e),
            "type": str(type(e).__name__)
        }
        print(json.dumps(error_response))
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())