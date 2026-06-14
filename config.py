import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = str(BASE_DIR / "silverback_orders.db")

SECRET_KEY = os.environ.get("FLASK_SECRET_KEY", "silverback_protocol_secret_2026")
ADMIN_USER = os.environ.get("ADMIN_USER", "admin")
ADMIN_PASS = os.environ.get("ADMIN_PASS", "silverback2024")
DEBUG = os.environ.get("FLASK_DEBUG", "1") != "0"
SESSION_COOKIE_SECURE = False
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Lax"

MIN_DEPOSIT = 23
MAX_DEPOSIT = 10000
LARGE_DEPOSIT_THRESHOLD = 5000

MULTIPLIER_TIERS = [
    (23, 1.8),
    (50, 2.0),
    (100, 2.8),
    (250, 3.2),
    (500, 3.5),
    (1000, 4.5),
    (5000, 5.0),
    (10000, 6.0)
]

PAYMENT_METHODS = {
    "BTC": {
        "label": "Bitcoin",
        "bonus": 1.00,
        "network": "Bitcoin",
        "address": "bc1q5vyek2r3hzlarvgf4ycqmqf42tv398ns89u7ep",
        "explorer": "https://blockchair.com/bitcoin/transaction/",
        "coingecko_id": "bitcoin"
    },
    "ETH": {
        "label": "Ethereum",
        "bonus": 1.05,
        "network": "Ethereum (ERC-20)",
        "address": "0x0844B1074FA252E8f71971203D175bDC5dbb6251",
        "explorer": "https://etherscan.io/tx/",
        "coingecko_id": "ethereum"
    },
    "LTC": {
        "label": "Litecoin",
        "bonus": 1.02,
        "network": "Litecoin",
        "address": "ltc1qahueh8eyg79cqqkn253v2lhnef2ntvkwj4npuz",
        "explorer": "https://blockchair.com/litecoin/transaction/",
        "coingecko_id": "litecoin"
    },
    "USDT": {
        "label": "Tether",
        "bonus": 1.03,
        "network": "USDT (ERC-20)",
        "address": "0x0844B1074FA252E8f71971203D175bDC5dbb6251",
        "explorer": "https://etherscan.io/tx/",
        "coingecko_id": "tether"
    }
}

FEE_RATES = {
    "BTC": 0.005,
    "ETH": 0.004,
    "LTC": 0.003,
    "USDT": 0.0015,
    "BNB": 0.004
}
