#!/usr/bin/env python3
"""
Telegram Bot Entrypoint
Runs the Silverback bot as a separate service
"""
import subprocess
import sys

if __name__ == "__main__":
    subprocess.run([sys.executable, "silverback.py"], check=False)
