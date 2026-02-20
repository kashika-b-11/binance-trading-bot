"""
Lightweight Web UI for Binance Futures Testnet Trading Bot
Run with: python app.py
Then open: http://localhost:5000
"""

from flask import Flask, render_template_string, request, jsonify
from bot.orders import place_order
from bot.logging_config import setup_logger

app = Flask(__name__)
logger = setup_logger()

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Binance Futures Bot</title>
  <link href="https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500;600&display=swap" rel="stylesheet"/>
  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

    :root {
      --bg: #0b0e17;
      --surface: #111827;
      --surface2: #1a2235;
      --border: #1f2d45;
      --accent: #f0b90b;
      --accent2: #e8a200;
      --green: #0ecb81;
      --red: #f6465d;
      --text: #e2e8f0;
      --muted: #64748b;
      --mono: 'Space Mono', monospace;
      --sans: 'DM Sans', sans-serif;
    }

    body {
      background: var(--bg);
      color: var(--text);
      font-family: var(--sans);
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      align-items: center;
      padding: 40px 20px;
    }

    /* Grid background */
    body::before {
      content: '';
      position: fixed;
      inset: 0;
      background-image:
        linear-gradient(rgba(240,185,11,0.03) 1px, transparent 1px),
        linear-gradient(90deg, rgba(240,185,11,0.03) 1px, transparent 1px);
      background-size: 40px 40px;
      pointer-events: none;
      z-index: 0;
    }

    .wrapper {
      position: relative;
      z-index: 1;
      width: 100%;
      max-width: 560px;
    }

    header {
      text-align: center;
      margin-bottom: 36px;
    }

    .logo {
      display: inline-flex;
      align-items: center;
      gap: 10px;
      margin-bottom: 8px;
    }

    .logo-icon {
      width: 36px;
      height: 36px;
      background: var(--accent);
      border-radius: 8px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 18px;
    }

    h1 {
      font-family: var(--mono);
      font-size: 22px;
      font-weight: 700;
      color: var(--accent);
      letter-spacing: -0.5px;
    }

    .subtitle {
      font-size: 13px;
      color: var(--muted);
      font-family: var(--mono);
      margin-top: 4px;
    }

    .testnet-badge {
      display: inline-block;
      background: rgba(240,185,11,0.1);
      border: 1px solid rgba(240,185,11,0.3);
      color: var(--accent);
      font-family: var(--mono);
      font-size: 11px;
      padding: 3px 10px;
      border-radius: 20px;
      margin-top: 10px;
      letter-spacing: 1px;
    }

    .card {
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 16px;
      padding: 28px;
      margin-bottom: 16px;
    }

    .form-group {
      margin-bottom: 20px;
    }

    label {
      display: block;
      font-size: 12px;
      font-family: var(--mono);
      color: var(--muted);
      text-transform: uppercase;
      letter-spacing: 1px;
      margin-bottom: 8px;
    }

    input, select {
      width: 100%;
      background: var(--surface2);
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 12px 16px;
      color: var(--text);
      font-family: var(--mono);
      font-size: 14px;
      outline: none;
      transition: border-color 0.2s, box-shadow 0.2s;
      appearance: none;
    }

    input:focus, select:focus {
      border-color: var(--accent);
      box-shadow: 0 0 0 3px rgba(240,185,11,0.1);
    }

    input::placeholder { color: var(--muted); }

    .side-toggle {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 8px;
    }

    .side-btn {
      padding: 12px;
      border-radius: 10px;
      border: 2px solid var(--border);
      background: var(--surface2);
      color: var(--muted);
      font-family: var(--mono);
      font-size: 13px;
      font-weight: 700;
      cursor: pointer;
      transition: all 0.2s;
      letter-spacing: 1px;
    }

    .side-btn:hover { border-color: var(--accent); }

    .side-btn.buy.active {
      background: rgba(14,203,129,0.1);
      border-color: var(--green);
      color: var(--green);
    }

    .side-btn.sell.active {
      background: rgba(246,70,93,0.1);
      border-color: var(--red);
      color: var(--red);
    }

    .price-fields {
      display: none;
      gap: 12px;
    }

    .price-fields.show {
      display: grid;
    }

    .price-fields.two-col {
      grid-template-columns: 1fr 1fr;
    }

    .price-fields.one-col {
      grid-template-columns: 1fr;
    }

    .submit-btn {
      width: 100%;
      padding: 14px;
      background: var(--accent);
      color: #0b0e17;
      border: none;
      border-radius: 10px;
      font-family: var(--mono);
      font-size: 14px;
      font-weight: 700;
      letter-spacing: 1px;
      cursor: pointer;
      transition: background 0.2s, transform 0.1s;
      margin-top: 4px;
    }

    .submit-btn:hover { background: var(--accent2); }
    .submit-btn:active { transform: scale(0.99); }
    .submit-btn:disabled { opacity: 0.5; cursor: not-allowed; }

    .result-card {
      display: none;
      border-radius: 16px;
      padding: 20px 24px;
      margin-bottom: 16px;
      border: 1px solid;
    }

    .result-card.success {
      background: rgba(14,203,129,0.05);
      border-color: rgba(14,203,129,0.3);
    }

    .result-card.error {
      background: rgba(246,70,93,0.05);
      border-color: rgba(246,70,93,0.3);
    }

    .result-title {
      font-family: var(--mono);
      font-size: 13px;
      font-weight: 700;
      margin-bottom: 14px;
      letter-spacing: 0.5px;
    }

    .result-card.success .result-title { color: var(--green); }
    .result-card.error .result-title { color: var(--red); }

    .result-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 10px;
    }

    .result-item {
      background: var(--surface2);
      border-radius: 8px;
      padding: 10px 12px;
    }

    .result-item .key {
      font-family: var(--mono);
      font-size: 10px;
      color: var(--muted);
      text-transform: uppercase;
      letter-spacing: 1px;
      margin-bottom: 4px;
    }

    .result-item .val {
      font-family: var(--mono);
      font-size: 14px;
      font-weight: 700;
      color: var(--text);
    }

    .result-item .val.green { color: var(--green); }
    .result-item .val.yellow { color: var(--accent); }

    .error-msg {
      font-family: var(--mono);
      font-size: 13px;
      color: var(--red);
    }

    .spinner {
      display: none;
      width: 18px;
      height: 18px;
      border: 2px solid rgba(0,0,0,0.3);
      border-top-color: #0b0e17;
      border-radius: 50%;
      animation: spin 0.7s linear infinite;
      margin: 0 auto;
    }

    @keyframes spin { to { transform: rotate(360deg); } }

    footer {
      text-align: center;
      font-family: var(--mono);
      font-size: 11px;
      color: var(--muted);
      margin-top: 8px;
    }

    select option { background: var(--surface2); }
  </style>
</head>
<body>
  <div class="wrapper">
    <header>
      <div class="logo">
        <div class="logo-icon">₿</div>
        <h1>FUTURES BOT</h1>
      </div>
      <div class="subtitle">Binance Futures Testnet (USDT-M)</div>
      <div class="testnet-badge">TESTNET MODE</div>
    </header>

    <!-- Result -->
    <div class="result-card" id="resultCard">
      <div class="result-title" id="resultTitle"></div>
      <div id="resultBody"></div>
    </div>

    <!-- Form -->
    <div class="card">
      <form id="orderForm">

        <div class="form-group">
          <label>Symbol</label>
          <input type="text" id="symbol" placeholder="BTCUSDT" value="BTCUSDT" required/>
        </div>

        <div class="form-group">
          <label>Side</label>
          <div class="side-toggle">
            <button type="button" class="side-btn buy active" onclick="setSide('BUY')">BUY</button>
            <button type="button" class="side-btn sell" onclick="setSide('SELL')">SELL</button>
          </div>
          <input type="hidden" id="side" value="BUY"/>
        </div>

        <div class="form-group">
          <label>Order Type</label>
          <select id="orderType" onchange="updatePriceFields()">
            <option value="MARKET">MARKET — execute at market price</option>
            <option value="LIMIT">LIMIT — execute at your price</option>
            <option value="STOP_MARKET">STOP_MARKET — trigger → market order</option>
            <option value="STOP">STOP (Stop-Limit) — trigger → limit order</option>
          </select>
        </div>

        <div class="form-group">
          <label>Quantity</label>
          <input type="number" id="quantity" placeholder="0.01" step="0.001" min="0.001" required/>
        </div>

        <!-- Limit price only -->
        <div class="price-fields one-col" id="limitFields">
          <div class="form-group" style="margin-bottom:0">
            <label>Limit Price (USDT)</label>
            <input type="number" id="price" placeholder="e.g. 30000" step="0.01"/>
          </div>
        </div>

        <!-- Stop Market: stop price only -->
        <div class="price-fields one-col" id="stopMarketFields">
          <div class="form-group" style="margin-bottom:0">
            <label>Stop Price / Trigger (USDT)</label>
            <input type="number" id="stopPriceSM" placeholder="e.g. 29000" step="0.01"/>
          </div>
        </div>

        <!-- Stop-Limit: both -->
        <div class="price-fields two-col" id="stopLimitFields">
          <div class="form-group" style="margin-bottom:0">
            <label>Stop Price / Trigger</label>
            <input type="number" id="stopPriceSL" placeholder="e.g. 29000" step="0.01"/>
          </div>
          <div class="form-group" style="margin-bottom:0">
            <label>Limit Price</label>
            <input type="number" id="limitPriceSL" placeholder="e.g. 28500" step="0.01"/>
          </div>
        </div>

        <button type="submit" class="submit-btn" id="submitBtn">
          <span id="btnText">PLACE ORDER</span>
          <div class="spinner" id="spinner"></div>
        </button>
      </form>
    </div>

    <footer>logs/bot.log &nbsp;·&nbsp; testnet.binancefuture.com</footer>
  </div>

  <script>
    function setSide(s) {
      document.getElementById('side').value = s;
      document.querySelectorAll('.side-btn').forEach(b => b.classList.remove('active'));
      document.querySelector(`.side-btn.${s.toLowerCase()}`).classList.add('active');
    }

    function updatePriceFields() {
      const type = document.getElementById('orderType').value;
      document.getElementById('limitFields').classList.remove('show');
      document.getElementById('stopMarketFields').classList.remove('show');
      document.getElementById('stopLimitFields').classList.remove('show');
      if (type === 'LIMIT') document.getElementById('limitFields').classList.add('show');
      if (type === 'STOP_MARKET') document.getElementById('stopMarketFields').classList.add('show');
      if (type === 'STOP') document.getElementById('stopLimitFields').classList.add('show');
    }

    document.getElementById('orderForm').addEventListener('submit', async (e) => {
      e.preventDefault();

      const btn = document.getElementById('submitBtn');
      const spinner = document.getElementById('spinner');
      const btnText = document.getElementById('btnText');
      btn.disabled = true;
      btnText.style.display = 'none';
      spinner.style.display = 'block';

      const type = document.getElementById('orderType').value;
      const payload = {
        symbol: document.getElementById('symbol').value.trim().toUpperCase(),
        side: document.getElementById('side').value,
        order_type: type,
        quantity: parseFloat(document.getElementById('quantity').value),
        price: null,
        stop_price: null,
      };

      if (type === 'LIMIT') {
        payload.price = parseFloat(document.getElementById('price').value) || null;
      } else if (type === 'STOP_MARKET') {
        payload.stop_price = parseFloat(document.getElementById('stopPriceSM').value) || null;
      } else if (type === 'STOP') {
        payload.stop_price = parseFloat(document.getElementById('stopPriceSL').value) || null;
        payload.price = parseFloat(document.getElementById('limitPriceSL').value) || null;
      }

      try {
        const res = await fetch('/place_order', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });
        const data = await res.json();
        showResult(data);
      } catch (err) {
        showResult({ success: false, error: 'Network error: ' + err.message });
      } finally {
        btn.disabled = false;
        btnText.style.display = 'inline';
        spinner.style.display = 'none';
      }
    });

    function showResult(data) {
      const card = document.getElementById('resultCard');
      const title = document.getElementById('resultTitle');
      const body = document.getElementById('resultBody');

      card.className = 'result-card ' + (data.success ? 'success' : 'error');
      card.style.display = 'block';

      if (data.success) {
        const r = data.response;
        title.textContent = '✅  ORDER PLACED SUCCESSFULLY';
        const avgPrice = (parseFloat(r.avgPrice) > 0 ? r.avgPrice : r.price) || '—';
        body.innerHTML = `
          <div class="result-grid">
            <div class="result-item"><div class="key">Order ID</div><div class="val yellow">${r.orderId}</div></div>
            <div class="result-item"><div class="key">Status</div><div class="val green">${r.status}</div></div>
            <div class="result-item"><div class="key">Symbol</div><div class="val">${r.symbol}</div></div>
            <div class="result-item"><div class="key">Side</div><div class="val">${r.side}</div></div>
            <div class="result-item"><div class="key">Type</div><div class="val">${r.type}</div></div>
            <div class="result-item"><div class="key">Quantity</div><div class="val">${r.origQty}</div></div>
            <div class="result-item"><div class="key">Executed Qty</div><div class="val">${r.executedQty}</div></div>
            <div class="result-item"><div class="key">Avg Price</div><div class="val">${avgPrice}</div></div>
          </div>`;
      } else {
        title.textContent = '❌  ORDER FAILED';
        body.innerHTML = `<div class="error-msg">${data.error}</div>`;
      }

      card.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }

    updatePriceFields();
  </script>
</body>
</html>
"""


@app.route("/")
def index():
    return render_template_string(HTML)


@app.route("/place_order", methods=["POST"])
def api_place_order():
    data = request.get_json()
    try:
        response = place_order(
            symbol=data.get("symbol"),
            side=data.get("side"),
            order_type=data.get("order_type"),
            quantity=float(data.get("quantity")),
            price=data.get("price"),
            stop_price=data.get("stop_price"),
        )
        return jsonify({"success": True, "response": response})
    except (ValueError, RuntimeError, EnvironmentError) as e:
        logger.warning(f"UI order failed: {e}")
        return jsonify({"success": False, "error": str(e)})
    except Exception as e:
        logger.exception(f"Unexpected UI error: {e}")
        return jsonify({"success": False, "error": f"Unexpected error: {e}"})


if __name__ == "__main__":
    print("\n🤖  Binance Futures Testnet Trading Bot — Web UI")
    print("📡  Open your browser at: http://localhost:5000\n")
    app.run(debug=False, port=5000)