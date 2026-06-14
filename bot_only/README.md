# Standalone Silverback Bot (bot_only)

Minimal, self-contained Telegram bot for quick deployment. Files included:

- `bot.py` — the minimal bot application
- `requirements.txt` — Python dependencies
- `Procfile` — worker entry for Heroku-like platforms
- `.env.example` — example environment variables

Quick start:

1. Copy `.env.example` to `.env` and set `SILVERBACK_BOT_TOKEN` and `SILVERBACK_ADMIN_CHAT_ID`.
2. Install dependencies: `pip install -r requirements.txt`.
3. Run locally: `python bot.py`.
4. To deploy to Heroku, push this folder and set config vars accordingly; the `Procfile` runs the bot.

Docker (recommended):

Build the image and run (from the `bot_only/` folder):

```bash
docker build -t silverback-bot:latest .
docker run -e SILVERBACK_BOT_TOKEN=your_token -e SILVERBACK_ADMIN_CHAT_ID=123456789 silverback-bot:latest
```

Using Docker Compose (loads `.env`):

```bash
docker-compose up --build
```

Notes:
- The Dockerfile is multi-stage and runs the process as a non-root user.
- Use the `.env` file or environment variables in your platform to provide the bot token and admin chat id.
