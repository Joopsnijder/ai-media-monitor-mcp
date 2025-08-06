#!/usr/bin/env python3
"""
Simple API endpoint for weekly report that only outputs JSON to stdout.
"""

import asyncio
import json
import sys
import os

# Suppress all print statements by redirecting stderr to devnull
sys.stderr = open(os.devnull, 'w')

async def main():
    try:
        # Import the server function directly
        from server import get_weekly_report
        
        # Generate the report
        report_data = await get_weekly_report()
        
        # Output only JSON to stdout
        print(json.dumps(report_data, default=str, ensure_ascii=False))
        
    except Exception as e:
        # Output error as JSON
        error_response = {
            "error": "Failed to generate weekly report",
            "details": str(e)
        }
        print(json.dumps(error_response))
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())