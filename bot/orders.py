from bot.client import get_client
from bot.validators import validate_order
from bot.logging_config import setup_logger

logger = setup_logger()

client = get_client()


def place_order(
    symbol,
    side,
    order_type,
    quantity,
    price=None,
    stop_price=None
):

    try:

        validate_order(
            symbol,
            side,
            order_type,
            quantity,
            price,
            stop_price
        )

        logger.info(f"Order Request: {symbol} {side} {order_type}")

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
                "timeInForce": "GTC"

            })

        elif order_type == "STOP":

            params.update({

                "type": "STOP",
                "price": price,
                "stopPrice": stop_price,
                "timeInForce": "GTC"

            })

        response = client.futures_create_order(**params)

        logger.info(f"Response: {response}")

        return response

    except Exception as e:

        logger.error(str(e))

        raise e