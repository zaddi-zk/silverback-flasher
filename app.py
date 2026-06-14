import os
import random
import string
import requests
import time
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from database import Database
import config

app = Flask(__name__, static_folder='static', static_url_path='/static')

is_development = config.DEBUG
app.secret_key = config.SECRET_KEY
app.config['SESSION_COOKIE_SECURE'] = not is_development
app.config['SESSION_COOKIE_HTTPONLY'] = config.SESSION_COOKIE_HTTPONLY
app.config['SESSION_COOKIE_SAMESITE'] = config.SESSION_COOKIE_SAMESITE
app.config['TEMPLATES_AUTO_RELOAD'] = is_development

ADMIN_USER = config.ADMIN_USER
ADMIN_PASS = config.ADMIN_PASS

db = Database(config.DATABASE_PATH)

PAYMENT_METHODS = config.PAYMENT_METHODS
MIN_DEPOSIT = config.MIN_DEPOSIT
MAX_DEPOSIT = config.MAX_DEPOSIT
LARGE_DEPOSIT_THRESHOLD = config.LARGE_DEPOSIT_THRESHOLD
MULTIPLIER_TIERS = config.MULTIPLIER_TIERS

FALLBACK_RATES = {
    "BTC": 43000.0,
    "ETH": 2550.0,
    "LTC": 70.0,
    "USDT": 1.0,
    "BNB": 650.0
}

RATE_CACHE = {
    "rates": FALLBACK_RATES.copy(),
    "timestamp": 0,
    "cache_ttl": 300  # 5 minutes
}

FEE_RATES = {
    "BTC": 0.005,
    "ETH": 0.004,
    "LTC": 0.003,
    "USDT": 0.0015,
    "BNB": 0.004
}


def fetch_real_rates() -> dict:
    """
    Fetch real cryptocurrency rates from CoinGecko API.
    Returns dict with currency as key and USD price as value.
    Falls back to cached/default rates on failure.
    """
    try:
        # Build CoinGecko API request
        coin_ids = [PAYMENT_METHODS[curr]["coingecko_id"] for curr in PAYMENT_METHODS]
        url = "https://api.coingecko.com/api/v3/simple/price"
        params = {
            "ids": ",".join(coin_ids),
            "vs_currencies": "usd",
            "include_market_cap": "false",
            "include_24hr_vol": "false"
        }
        
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
        
        # Map CoinGecko response back to our currency codes
        rates = {}
        for currency, wallet_info in PAYMENT_METHODS.items():
            coingecko_id = wallet_info["coingecko_id"]
            if coingecko_id in data and "usd" in data[coingecko_id]:
                rates[currency] = float(data[coingecko_id]["usd"])
        
        if rates:
            print(f"✓ Fetched real-time rates: {rates}")
            RATE_CACHE["rates"] = rates
            RATE_CACHE["timestamp"] = time.time()
            return rates
        
    except requests.exceptions.Timeout:
        print("⚠ Rate fetch timeout - using cached rates")
    except requests.exceptions.RequestException as e:
        print(f"⚠ Failed to fetch real rates: {e} - using cached rates")
    except Exception as e:
        print(f"⚠ Error processing rates: {e} - using cached rates")
    
    return RATE_CACHE["rates"]


def get_current_rates() -> dict:
    """
    Get current rates with intelligent caching.
    Refreshes from API if cache is stale, otherwise returns cached rates.
    """
    current_time = time.time()
    if current_time - RATE_CACHE["timestamp"] > RATE_CACHE["cache_ttl"]:
        return fetch_real_rates()
    return RATE_CACHE["rates"]


def get_base_multiplier(deposit_amount: float) -> float:
    """
    Calculate base multiplier based on deposit tier.
    Uses linear interpolation between tiers.
    """
    if deposit_amount < MIN_DEPOSIT:
        return 0  # Invalid
    
    if deposit_amount >= MULTIPLIER_TIERS[-1][0]:
        return MULTIPLIER_TIERS[-1][1]  # Max multiplier
    
    # Find the two tiers to interpolate between
    for i in range(len(MULTIPLIER_TIERS) - 1):
        lower_amount, lower_mult = MULTIPLIER_TIERS[i]
        upper_amount, upper_mult = MULTIPLIER_TIERS[i + 1]
        
        if lower_amount <= deposit_amount <= upper_amount:
            # Linear interpolation
            ratio = (deposit_amount - lower_amount) / (upper_amount - lower_amount)
            multiplier = lower_mult + ratio * (upper_mult - lower_mult)
            return round(multiplier, 4)
    
    return MULTIPLIER_TIERS[0][1]


def get_payment_bonus(currency: str) -> float:
    """Get the bonus multiplier for a payment method."""
    return PAYMENT_METHODS.get(currency, {}).get("bonus", 1.0)


def calculate_flash_amount(deposit_usd: float, currency: str) -> dict:
    """
    Calculate the complete flash transaction with all multipliers.
    Returns dict with deposit, base_multiplier, bonus, final_multiplier, and flash_amount.
    """
    # Validation
    if deposit_usd < MIN_DEPOSIT:
        return {
            "success": False,
            "error": f"Minimum deposit is ${MIN_DEPOSIT}",
            "min_deposit": MIN_DEPOSIT
        }
    
    if deposit_usd > MAX_DEPOSIT:
        return {
            "success": False,
            "error": f"Maximum deposit is ${MAX_DEPOSIT}",
            "max_deposit": MAX_DEPOSIT
        }
    
    # Calculate multipliers
    base_multiplier = get_base_multiplier(deposit_usd)
    payment_bonus = get_payment_bonus(currency)
    final_multiplier = base_multiplier * payment_bonus
    
    # Calculate flash amount
    flash_amount = deposit_usd * final_multiplier
    
    # Determine if large deposit warning needed
    warning = None
    if deposit_usd > LARGE_DEPOSIT_THRESHOLD:
        warning = f"Large deposit (${deposit_usd}) may require additional verification"
    
    return {
        "success": True,
        "deposit": round(deposit_usd, 2),
        "base_multiplier": round(base_multiplier, 4),
        "payment_method": currency,
        "payment_bonus": payment_bonus,
        "final_multiplier": round(final_multiplier, 4),
        "flash_amount": round(flash_amount, 2),
        "warning": warning
    }


def get_multiplier_table() -> list:
    """Return the multiplier table for UI display."""
    return [
        {
            "min_deposit": tier[0],
            "multiplier": tier[1],
            "label": f"${tier[0]}"
        }
        for tier in MULTIPLIER_TIERS
    ]


def generate_payment_id(length: int = 12) -> str:
    return "PAY-" + "".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(length))


def calculate_receive_amount(amount_usd: float, currency: str) -> tuple[float, float]:
    """
    Calculate receive amount in crypto based on real-time rates.
    Returns (receive_amount_crypto, fee_usd)
    """
    fee_rate = FEE_RATES.get(currency, 0.003)
    fee_usd = max(0.5, amount_usd * fee_rate)
    
    # Use real-time rates
    current_rates = get_current_rates()
    crypto_rate = current_rates.get(currency, FALLBACK_RATES.get(currency, 1.0))
    
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
    total_value = sum([row["amount"] for row in db.fetchall("SELECT amount FROM orders")]) if total_orders else 0
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
    return render_template("bridge.html", stats=stats, wallets=PAYMENT_METHODS, multiplier_table=get_multiplier_table())

@app.route("/api/calculate", methods=["POST"])
def api_calculate():
    """
    Backend order validation endpoint.
    Accepts deposit amount and payment currency, returns a validated flash amount and optional warning.
    """
    try:
        data = request.json or {}
        deposit = float(data.get("deposit", 0))
        currency = data.get("currency", "BTC")
        
        if currency not in PAYMENT_METHODS:
            return jsonify({"success": False, "error": "Invalid currency"}), 400
        
        result = calculate_flash_amount(deposit, currency)
        if not result.get("success"):
            return jsonify(result), 400
        
        return jsonify({
            "success": True,
            "deposit": result["deposit"],
            "payment_method": result["payment_method"],
            "flash_amount": result["flash_amount"],
            "warning": result.get("warning")
        })
    
    except ValueError:
        return jsonify({"success": False, "error": "Invalid deposit amount"}), 400
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/api/multiplier-table", methods=["GET"])
def api_multiplier_table():
    """
    Get the multiplier tier table for UI display.
    """
    try:
        table_data = {
            "success": True,
            "base_tiers": get_multiplier_table(),
            "payment_bonuses": {
                currency: {
                    "name": PAYMENT_METHODS[currency]["network"],
                    "bonus": PAYMENT_METHODS[currency]["bonus"]
                }
                for currency in PAYMENT_METHODS
            },
            "limits": {
                "minimum": MIN_DEPOSIT,
                "maximum": MAX_DEPOSIT,
                "large_deposit_threshold": LARGE_DEPOSIT_THRESHOLD
            }
        }
        return jsonify(table_data)
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/api/rates", methods=["GET"])
def api_rates():
    """
    Public API endpoint to fetch real-time cryptocurrency rates.
    Returns current rates for all supported currencies with timestamp.
    """
    try:
        current_rates = get_current_rates()
        return jsonify({
            "success": True,
            "rates": current_rates,
            "timestamp": RATE_CACHE["timestamp"],
            "cache_ttl": RATE_CACHE["cache_ttl"],
            "currencies": list(current_rates.keys())
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error fetching rates: {str(e)}",
            "rates": RATE_CACHE["rates"]
        }), 500

@app.route("/initiate-payment", methods=["POST"])
def initiate_payment():
    data = request.json or {}
    try:
        amount = float(data.get("amount", 0))
        currency = data.get("currency")
    except (ValueError, TypeError):
        return jsonify({"success": False, "message": "Invalid amount or currency"}), 400
    
    if currency not in PAYMENT_METHODS:
        return jsonify({"success": False, "message": "Invalid currency"}), 400
    
    calc_result = calculate_flash_amount(amount, currency)
    if not calc_result.get("success"):
        return jsonify(calc_result), 400
    
    wallet = PAYMENT_METHODS.get(currency)
    user_session = session.get("user_id") or str(datetime.utcnow().timestamp())
    session["user_id"] = user_session
    payment_id = generate_payment_id()
    
    db.create_order(
        payment_id,
        user_session,
        amount,
        currency,
        wallet["address"]
    )

    order = db.get_order(payment_id)
    order_id = order["id"] if order else None

    return jsonify({
        "success": True,
        "order_id": order_id,
        "payment_id": payment_id,
        "wallet_address": wallet["address"],
        "network": wallet["network"],
        "explorer": wallet["explorer"],
        "deposit_amount": amount,
        "currency": currency,
        "flash_amount": calc_result["flash_amount"],
        "warning": calc_result.get("warning")
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

    if order["status"] == "success":
        return jsonify({"success": False, "message": "Order is already completed."}), 400

    db.update_order(payment_id, tx_hash, "processing")

    return jsonify({"success": True, "order_id": order["id"], "payment_id": payment_id})

@app.route("/api/my-orders")
def api_my_orders():
    user_session = session.get("user_id")
    if not user_session:
        return jsonify({"success": True, "orders": []})

    rows = db.fetchall(
        "SELECT payment_id, amount, currency, status, tx_hash, created_at FROM orders WHERE user_session = ? ORDER BY created_at DESC",
        (user_session,)
    )
    orders = [dict(row) for row in rows]
    return jsonify({"success": True, "orders": orders})

@app.route("/flash-status/<payment_id>")
def flash_status(payment_id):
    order = db.fetchone("SELECT * FROM orders WHERE payment_id = ?", (payment_id,))
    if not order:
        return jsonify({"success": False, "message": "Order not found."}), 404

    status = order["status"]
    if status == "processing":
        status = "success"
        db.update_order(payment_id, order["tx_hash"], "success")

    return jsonify({
        "success": True,
        "status": status,
        "tx_hash": order["tx_hash"] or generate_fake_tx_hash(),
        "explorer": PAYMENT_METHODS.get(order["currency"], {}).get("explorer")
    })

@app.route("/mock-explorer/<tx_hash>")
def mock_explorer(tx_hash):
    return render_template("mock_explorer.html", tx_hash=tx_hash)


@app.route("/healthz")
def healthz():
    """Basic health check for Render and load balancers."""
    return jsonify({"status": "ok"}), 200

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
    total_income = sum(order["amount"] for order in orders)

    return render_template("admin_orders.html", orders=orders, total_income=total_income)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("admin"))

# Initialize real rates on app startup
@app.before_request
def initialize_rates():
    """Fetch real rates on first request if cache is empty."""
    if RATE_CACHE["timestamp"] == 0:
        fetch_real_rates()

if __name__ == "__main__":
    print("\n" + "="*60)
    print("Silverback Protocol - Flask Backend")
    print("="*60)
    print("Fetching initial cryptocurrency rates...")
    fetch_real_rates()
    print("\nApplication starting...\n")
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=is_development)
