# Binance Futures Trading Bot (Testnet)

## Overview

This project is a Python-based Command Line Interface (CLI) trading bot that places orders on the **Binance Futures Testnet (USDT-M)**.

It was built as part of a Python Developer Intern assessment and demonstrates clean code structure, proper logging, input validation, and error handling.

The bot allows users to safely test trading functionality using Binance Testnet without risking real funds.

---

## Features

* Place **Market Orders**
* Place **Limit Orders**
* Place **Stop Orders** (Bonus Feature)
* Supports both **BUY** and **SELL**
* Command Line Interface using Typer
* Structured and modular codebase
* Logging of API requests and responses
* Exception handling and input validation
* Uses Binance Futures Testnet environment

---

## Project Structure

```
trading_bot/
│
├── bot/
│   ├── client.py          # Binance client setup
│   ├── orders.py          # Order execution logic
│   ├── validators.py      # Input validation
│   ├── logging_config.py  # Logging configuration
│
├── logs/
│   └── bot.log            # Log file
│
├── cli.py                 # CLI entry point
├── requirements.txt      # Dependencies
├── README.md
└── .env                  # API credentials (not shared)
```

---

## Setup Instructions

### 1. Clone Repository

```
git clone https://github.com/kashika-b-11/binance-trading-bot.git

cd binance-trading-bot
```

---

### 2. Install Dependencies

```
pip install -r requirements.txt
```

---

### 3. Create Binance Testnet API Keys

Go to:

https://testnet.binancefuture.com

Generate API Key and Secret Key.

Create a `.env` file in project root:

```
API_KEY=your_api_key
API_SECRET=your_api_secret
```

---

## Usage

### Market Order

```
python cli.py --symbol BTCUSDT --side BUY --order-type MARKET --quantity 0.01
```

---

### Limit Order

```
python cli.py --symbol BTCUSDT --side BUY --order-type LIMIT --quantity 0.01 --price 30000
```

---

### Stop Order

```
python cli.py --symbol BTCUSDT --side SELL --order-type STOP --quantity 0.01 --price 29000 --stop-price 29500
```

---

## Example Output

```
Order Summary:
Symbol: BTCUSDT
Side: BUY
Type: MARKET
Quantity: 0.01

SUCCESS
Order ID: 12345678
Status: FILLED
```

---

## Logs

All API activity is logged in:

```
logs/bot.log
```

Includes:

* Order requests
* Order responses
* Errors (if any)

---

## Assumptions

* Binance Futures Testnet account is used
* USDT-M Futures trading
* Python 3.10 or higher

---

## Author

**Kashika Bhardwaj**

GitHub: https://github.com/kashika-b-11

---

## Notes

This project is for educational and assessment purposes and uses Binance Testnet only.
