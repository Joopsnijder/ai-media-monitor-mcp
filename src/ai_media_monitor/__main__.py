"""Main entry point for AI Media Monitor."""

import os
import sys

# Add the project root to Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from server import mcp

if __name__ == "__main__":
    mcp.run()
