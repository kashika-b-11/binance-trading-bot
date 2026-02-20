import typer
from bot.orders import place_order

app = typer.Typer()


@app.command()
def trade(
    symbol: str = typer.Option(..., help="Trading symbol"),
    side: str = typer.Option(..., help="BUY or SELL"),
    order_type: str = typer.Option(..., help="MARKET, LIMIT, STOP"),
    quantity: float = typer.Option(..., help="Order quantity"),
    price: float = typer.Option(None, help="Price for LIMIT/STOP"),
    stop_price: float = typer.Option(None, help="Stop price for STOP"),
):

    print("\nOrder Summary:")
    print("Symbol:", symbol)
    print("Side:", side)
    print("Type:", order_type)
    print("Quantity:", quantity)

    try:

        response = place_order(
            symbol,
            side,
            order_type,
            quantity,
            price,
            stop_price
        )

        print("\nSUCCESS")
        print("Order ID:", response["orderId"])
        print("Status:", response["status"])

    except Exception as e:

        print("\nFAILED")
        print(str(e))


if __name__ == "__main__":
    app()