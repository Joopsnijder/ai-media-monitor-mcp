#!/usr/bin/env python3
"""
Simple API endpoint for weekly report that only outputs JSON to stdout.
"""

import asyncio
import json
import sys
import os
import warnings
from io import StringIO

# Completely redirect stdout to capture all print statements
original_stdout = sys.stdout
captured_output = StringIO()

try:
    # Redirect all output
    sys.stdout = captured_output
    sys.stderr = open(os.devnull, 'w')
    warnings.filterwarnings('ignore')
    
    # Set environment variables to suppress any debug output
    os.environ['PYTHONHASHSEED'] = '0'
    os.environ['PYTHONUNBUFFERED'] = '0'
    
    async def main():
        try:
            # Import the server function directly
            from server import get_weekly_report
            
            # Generate the report
            report_data = await get_weekly_report()
            
            # Restore stdout only for final JSON output
            sys.stdout = original_stdout
            
            # Output only clean JSON
            print(json.dumps(report_data, default=str, ensure_ascii=False))
            
        except Exception as e:
            # Restore stdout for error output
            sys.stdout = original_stdout
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

except Exception as e:
    # Final fallback - restore stdout and output error
    sys.stdout = original_stdout
    sys.stderr = sys.__stderr__
    
    error_response = {
        "error": "Script execution failed",
        "details": str(e),
        "type": str(type(e).__name__)
    }
    print(json.dumps(error_response))
    sys.exit(1)