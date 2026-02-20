import re

VALID_SIDES = {"BUY", "SELL"}
VALID_ORDER_TYPES = {"MARKET", "LIMIT", "STOP_MARKET", "STOP"}

# Validates symbols like BTCUSDT, ETHUSDT, etc.
SYMBOL_PATTERN = re.compile(r"^[A-Z]{2,10}USDT$")


def validate_symbol(symbol: str) -> str:
    symbol = symbol.strip().upper()
    if not SYMBOL_PATTERN.match(symbol):
        raise ValueError(
            f"Invalid symbol '{symbol}'. Expected format: <ASSET>USDT (e.g., BTCUSDT, ETHUSDT)."
        )
    return symbol


def validate_side(side: str) -> str:
    side = side.strip().upper()
    if side not in VALID_SIDES:
        raise ValueError(f"Invalid side '{side}'. Must be one of: {', '.join(VALID_SIDES)}.")
    return side


def validate_order_type(order_type: str) -> str:
    order_type = order_type.strip().upper()
    if order_type not in VALID_ORDER_TYPES:
        raise ValueError(
            f"Invalid order type '{order_type}'. Must be one of: {', '.join(VALID_ORDER_TYPES)}."
        )
    return order_type


def validate_quantity(quantity: float) -> float:
    if quantity <= 0:
        raise ValueError(f"Quantity must be a positive number. Got: {quantity}.")
    return quantity


def validate_price(price: float, label: str = "price") -> float:
    if price <= 0:
        raise ValueError(f"{label.capitalize()} must be a positive number. Got: {price}.")
    return price


def validate_order(
    symbol: str,
    side: str,
    order_type: str,
    quantity: float,
    price: float | None,
    stop_price: float | None,
) -> tuple:
    """
    Full validation of all order fields.
    Returns normalized (symbol, side, order_type, quantity, price, stop_price).
    Raises ValueError with a descriptive message on any invalid input.
    """
    symbol = validate_symbol(symbol)
    side = validate_side(side)
    order_type = validate_order_type(order_type)
    quantity = validate_quantity(quantity)

    if order_type == "LIMIT":
        if price is None:
            raise ValueError("Price is required for LIMIT orders.")
        price = validate_price(price, "price")

    if order_type == "STOP_MARKET":
        if stop_price is None:
            raise ValueError("Stop price is required for STOP_MARKET orders.")
        stop_price = validate_price(stop_price, "stop_price")

    if order_type == "STOP":
        # Stop-Limit: requires both price (limit price) and stop_price (trigger price)
        if price is None:
            raise ValueError("Limit price is required for STOP (Stop-Limit) orders.")
        if stop_price is None:
            raise ValueError("Stop price (trigger) is required for STOP (Stop-Limit) orders.")
        price = validate_price(price, "price")
        stop_price = validate_price(stop_price, "stop_price")

    return symbol, side, order_type, quantity, price, stop_price