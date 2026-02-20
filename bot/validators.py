def validate_order(symbol, side, order_type, quantity, price, stop_price):

    if side not in ["BUY", "SELL"]:
        raise ValueError("Side must be BUY or SELL")

    if order_type not in ["MARKET", "LIMIT", "STOP"]:
        raise ValueError("Invalid order type")

    if quantity <= 0:
        raise ValueError("Quantity must be positive")

    if order_type == "LIMIT" and price is None:
        raise ValueError("Price required for LIMIT")

    if order_type == "STOP" and (price is None or stop_price is None):
        raise ValueError("STOP order requires price and stop_price")