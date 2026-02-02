"""Entry point for running Orisha as a module.

Usage:
    python -m orisha [command] [options]

Example:
    python -m orisha write --output docs/SYSTEM.md
    python -m orisha check
"""

from orisha.cli import app

if __name__ == "__main__":
    app()
