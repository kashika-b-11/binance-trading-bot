# Binance Futures Trading Bot (Testnet)

## Overview

This project is a Python-based Command Line Interface (CLI) trading bot that places orders on the **Binance Futures Testnet (USDT-M)**.

It was built as part of a Python Developer Intern assessment and demonstrates clean code structure, proper logging, input validation, and error handling.

The bot allows users to safely test trading functionality using Binance Testnet without risking real funds.

---

## Features

- Place **Market Orders**
- Place **Limit Orders**
- Place **Stop-Market Orders**
- Place **Stop-Limit Orders** *(Bonus)*
- Supports both **BUY** and **SELL**
- **Interactive CLI menu** with guided prompts and validation *(Bonus)*
- **Lightweight Web UI** via Flask — place orders from your browser *(Bonus)*
- Command Line Interface using Typer
- Structured and modular codebase
- Logging of API requests and responses to file and console
- Exception handling and input validation with descriptive error messages
- Direct REST API calls — no third-party Binance SDK required
- Uses Binance Futures Testnet environment

---

## Project Structure

```
trading_bot/
│
├── bot/
│   ├── client.py          # Binance Futures REST client (direct API calls)
│   ├── orders.py          # Order execution logic + response formatting
│   ├── validators.py      # Input validation for all order types
│   └── logging_config.py  # Logging configuration (file + console)
│
├── logs/
│   └── bot.log            # Log file (auto-created on first run)
│
├── cli.py                 # CLI entry point (flag mode + interactive mode)
├── app.py                 # Lightweight Flask Web UI
├── requirements.txt       # Dependencies
├── README.md
├── .env.example           # Example environment variables
└── .env                   # API credentials (not shared)
```

---

## Setup Instructions

### 1. Clone Repository

```bash
git clone https://github.com/kashika-b-11/binance-trading-bot.git
cd binance-trading-bot
```

### 2. Create and Activate Virtual Environment (recommended)

```bash
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Create Binance Testnet API Keys

Go to: **https://testnet.binancefuture.com**

Generate API Key and Secret Key.

Copy `.env.example` to `.env` and fill in your credentials:

```bash
cp .env.example .env
```

`.env` file:

```
API_KEY=your_api_key
API_SECRET=your_api_secret
```

> ⚠️ Never commit your `.env` file. It is listed in `.gitignore`.

---

## Usage

### Flag Mode (Direct Commands)

**Market Order:**
```bash
python cli.py --symbol BTCUSDT --side BUY --order-type MARKET --quantity 0.01
```

**Limit Order:**
```bash
python cli.py --symbol BTCUSDT --side BUY --order-type LIMIT --quantity 0.01 --price 30000
```

**Stop-Market Order:**
```bash
python cli.py --symbol BTCUSDT --side SELL --order-type STOP_MARKET --quantity 0.01 --stop-price 29000
```

**Stop-Limit Order *(Bonus)*:**
```bash
python cli.py --symbol BTCUSDT --side SELL --order-type STOP --quantity 0.01 --stop-price 29000 --price 28500
```

---

### Interactive Menu Mode *(Bonus)*

Run without flags to get a fully guided step-by-step prompt:

```bash
python cli.py --interactive
```

Example session:

```
Enter symbol (e.g. BTCUSDT): BTCUSDT
Side [BUY/SELL]: BUY

Order types:
  1) MARKET      — execute immediately at market price
  2) LIMIT       — execute at your specified price
  3) STOP_MARKET — trigger market order at stop price
  4) STOP        — Stop-Limit (trigger + limit price)

Order type: 1
Quantity: 0.01

──────────────────────────────────────────────────
  ORDER SUMMARY
──────────────────────────────────────────────────
  Symbol     : BTCUSDT
  Side       : BUY
  Type       : MARKET
  Quantity   : 0.01
──────────────────────────────────────────────────

Confirm and place order? [Y/n]:
```

---

### Web UI *(Bonus)*

```bash
python app.py
```

Then open **http://localhost:5000** in your browser.

Features:
- BUY / SELL toggle buttons
- Dropdown for all 4 order types
- Price fields that show/hide based on order type selected
- Live order result showing orderId, status, executedQty, avgPrice

---

## Example Output

```
──────────────────────────────────────────────────
  ORDER SUMMARY
──────────────────────────────────────────────────
  Symbol     : BTCUSDT
  Side       : BUY
  Type       : MARKET
  Quantity   : 0.01
──────────────────────────────────────────────────

✅ Order placed successfully!
  Order ID     : 12345678
  Symbol       : BTCUSDT
  Status       : FILLED
  Side         : BUY
  Type         : MARKET
  Quantity     : 0.01
  Executed Qty : 0.01
  Avg Price    : 96312.50000
```

---

## Logs

All API activity is logged in:

```
logs/bot.log
```

Includes:
- Order request parameters
- Raw API responses (DEBUG level)
- Order response summary (orderId, status, executedQty, avgPrice)
- Validation warnings
- API and network errors

---

## Assumptions

- Binance Futures Testnet account is used — no real funds are at risk
- USDT-M Futures trading only
- Python 3.10 or higher (uses `float | None` union syntax)
- No third-party Binance SDK — uses direct REST API calls via `requests`
- Symbol format assumed to be `<ASSET>USDT` (e.g., `BTCUSDT`, `ETHUSDT`)
- LIMIT orders use `GTC` (Good Till Cancelled) as default `timeInForce`
- Quantity precision depends on the symbol — if API returns a precision error, adjust quantity (e.g., use `0.001` instead of `0.01`)

---

## Author

**Kashika Bhardwaj**

GitHub: [https://github.com/kashika-b-11](https://github.com/kashika-b-11)

---

*This project is for educational and assessment purposes and uses Binance Testnet only.*
