from bot.validators import validate_order
from bot.logging_config import setup_logger

logger = setup_logger()


def place_order(
    symbol: str,
    side: str,
    order_type: str,
    quantity: float,
    price: float | None = None,
    stop_price: float | None = None,
) -> dict:
    """
    Validate inputs and place an order on Binance Futures Testnet.

    Supported order types:
      - MARKET     : Executed immediately at current market price.
      - LIMIT      : Executed at specified price or better (requires `price`).
      - STOP_MARKET: Triggered when market hits `stop_price`, executes as market order.
      - STOP       : Stop-Limit — triggered at `stop_price`, places limit order at `price`.

    Returns the full API response dict on success.
    Raises ValueError for bad input, RuntimeError for API/network failures.
    """
    from bot.client import get_client

    symbol, side, order_type, quantity, price, stop_price = validate_order(
        symbol, side, order_type, quantity, price, stop_price
    )

    # --- Log request summary ---
    logger.info("=" * 60)
    logger.info("ORDER REQUEST")
    logger.info(f"  Symbol    : {symbol}")
    logger.info(f"  Side      : {side}")
    logger.info(f"  Type      : {order_type}")
    logger.info(f"  Quantity  : {quantity}")
    if price is not None:
        logger.info(f"  Price     : {price}")
    if stop_price is not None:
        logger.info(f"  Stop Price: {stop_price}")

    # --- Build params ---
    params = {
        "symbol": symbol,
        "side": side,
        "quantity": quantity,
    }

    if order_type == "MARKET":
        params["type"] = "MARKET"

    elif order_type == "LIMIT":
        params.update({
            "type": "LIMIT",
            "price": price,
            "timeInForce": "GTC",
        })

    elif order_type == "STOP_MARKET":
        params.update({
            "type": "STOP_MARKET",
            "stopPrice": stop_price,
        })

    elif order_type == "STOP":
        # Stop-Limit: triggers at stopPrice, then places a limit order at price
        params.update({
            "type": "STOP",
            "price": price,
            "stopPrice": stop_price,
            "timeInForce": "GTC",
        })

    # --- Place order ---
    client = get_client()
    response = client.new_order(**params)

    # --- Log response ---
    logger.info("ORDER RESPONSE")
    logger.info(f"  Order ID    : {response.get('orderId', 'N/A')}")
    logger.info(f"  Status      : {response.get('status', 'N/A')}")
    logger.info(f"  Executed Qty: {response.get('executedQty', '0')}")
    avg_price = response.get('avgPrice') or response.get('price', 'N/A')
    logger.info(f"  Avg Price   : {avg_price}")
    logger.info("=" * 60)

    return response


def format_order_result(response: dict) -> str:
    """Return a clean, human-readable summary of an order response."""
    lines = [
        "\n✅ Order placed successfully!",
        f"  Order ID     : {response.get('orderId', 'N/A')}",
        f"  Symbol       : {response.get('symbol', 'N/A')}",
        f"  Status       : {response.get('status', 'N/A')}",
        f"  Side         : {response.get('side', 'N/A')}",
        f"  Type         : {response.get('type', 'N/A')}",
        f"  Quantity     : {response.get('origQty', 'N/A')}",
        f"  Executed Qty : {response.get('executedQty', '0')}",
    ]
    avg_price = response.get("avgPrice") or response.get("price")
    if avg_price and float(avg_price) > 0:
        lines.append(f"  Avg Price    : {avg_price}")
    return "\n".join(lines)