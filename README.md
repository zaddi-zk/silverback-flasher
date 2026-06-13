# Silverback Flasher (local run)

This repository contains a demo Telegram bot (`silverback.py`) and a React/Vite landing page.

## Requirements
- Python 3.10+ (for python-telegram-bot v20+)
- Node.js (for the frontend) - install LTS from https://nodejs.org

## Backend (Telegram bot)
1. Install Python deps:

```bash
python -m pip install -r requirements.txt
```

2. Set environment variables (recommended) or edit `silverback.py` directly:

```powershell
$env:SILVERBACK_BOT_TOKEN="YOUR_BOT_TOKEN"
$env:SILVERBACK_ADMIN_CHAT_ID="8711230373"
python silverback.py
```

The bot will start polling and the verification loop will run in the background.

## Frontend (landing page)
1. Install Node & npm, then in the project root:

```bash
npm install
npm run dev
```

2. Open http://localhost:5173 to view the landing page.

## Notes
- Replace blockchain API keys in `silverback.py` for real verification.
- Keep your bot token secret. If you commit it accidentally, rotate it immediately.
