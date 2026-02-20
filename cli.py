"""
Binance Futures Testnet Trading Bot — CLI Entry Point
Supports both direct flag mode and interactive menu mode.
"""

import typer
from typing import Optional
from bot.orders import place_order, format_order_result
from bot.logging_config import setup_logger

app = typer.Typer(
    name="trading-bot",
    help="Place orders on Binance Futures Testnet (USDT-M)",
    add_completion=False,
)

logger = setup_logger()


def _abort(message: str) -> None:
    typer.echo(f"\n❌  Error: {message}", err=True)
    raise typer.Exit(code=1)


def _prompt_with_validation(prompt: str, valid_options: list[str] | None = None, cast=str):
    """Prompt user for input, validate against options if given, re-prompt on error."""
    while True:
        if valid_options:
            options_str = " / ".join(valid_options)
            value = typer.prompt(f"{prompt} [{options_str}]")
        else:
            value = typer.prompt(prompt)

        try:
            value = cast(value.strip())
            if valid_options and str(value).upper() not in valid_options:
                typer.echo(f"  ⚠️  Invalid choice. Please enter one of: {', '.join(valid_options)}")
                continue
            return value if not isinstance(value, str) else value.upper()
        except (ValueError, TypeError):
            typer.echo(f"  ⚠️  Invalid input. Please try again.")


def _run_interactive_mode():
    """Interactive guided menu for placing an order."""
    typer.echo("\n" + "═" * 52)
    typer.echo("   🤖  BINANCE FUTURES TESTNET — TRADING BOT")
    typer.echo("═" * 52)
    typer.echo("   Interactive Order Placement\n")

    # Symbol
    symbol = typer.prompt("  Enter symbol (e.g. BTCUSDT, ETHUSDT)").strip().upper()

    # Side
    side = _prompt_with_validation("  Side", ["BUY", "SELL"])

    # Order type
    typer.echo("\n  Order types:")
    typer.echo("    1) MARKET      — execute immediately at market price")
    typer.echo("    2) LIMIT       — execute at your specified price")
    typer.echo("    3) STOP_MARKET — trigger market order at stop price")
    typer.echo("    4) STOP        — Stop-Limit (trigger + limit price)")
    order_type = _prompt_with_validation(
        "\n  Order type", ["MARKET", "LIMIT", "STOP_MARKET", "STOP"]
    )

    # Quantity
    quantity = _prompt_with_validation("  Quantity", cast=float)

    # Price / Stop Price based on type
    price = None
    stop_price = None

    if order_type == "LIMIT":
        price = _prompt_with_validation("  Limit price", cast=float)

    elif order_type == "STOP_MARKET":
        stop_price = _prompt_with_validation("  Stop price (trigger)", cast=float)

    elif order_type == "STOP":
        stop_price = _prompt_with_validation("  Stop price (trigger)", cast=float)
        price = _prompt_with_validation("  Limit price (placed after trigger)", cast=float)

    # Confirm
    typer.echo("\n" + "─" * 52)
    typer.echo("  ORDER SUMMARY")
    typer.echo("─" * 52)
    typer.echo(f"  Symbol     : {symbol}")
    typer.echo(f"  Side       : {side}")
    typer.echo(f"  Type       : {order_type}")
    typer.echo(f"  Quantity   : {quantity}")
    if price:
        typer.echo(f"  Price      : {price}")
    if stop_price:
        typer.echo(f"  Stop Price : {stop_price}")
    typer.echo("─" * 52)

    confirm = typer.confirm("\n  Confirm and place order?", default=True)
    if not confirm:
        typer.echo("\n  ❌  Order cancelled.")
        raise typer.Exit(code=0)

    return symbol, side, order_type, quantity, price, stop_price


@app.command()
def trade(
    symbol: Optional[str] = typer.Option(
        None, "--symbol", "-s", help="Trading pair symbol, e.g. BTCUSDT"
    ),
    side: Optional[str] = typer.Option(
        None, "--side", help="Order side: BUY or SELL"
    ),
    order_type: Optional[str] = typer.Option(
        None, "--order-type", "-t", help="MARKET | LIMIT | STOP_MARKET | STOP"
    ),
    quantity: Optional[float] = typer.Option(
        None, "--quantity", "-q", help="Order quantity (e.g. 0.01 for BTC)"
    ),
    price: Optional[float] = typer.Option(
        None, "--price", "-p", help="Limit price (required for LIMIT / STOP orders)"
    ),
    stop_price: Optional[float] = typer.Option(
        None, "--stop-price", help="Trigger price (required for STOP_MARKET / STOP orders)"
    ),
    interactive: bool = typer.Option(
        False, "--interactive", "-i", help="Launch interactive guided menu"
    ),
) -> None:
    """
    Place a futures order on Binance Testnet.

    \b
    Run with no flags for interactive mode:
      python cli.py --interactive

    \b
    Or pass flags directly:
      python cli.py --symbol BTCUSDT --side BUY --order-type MARKET --quantity 0.01
      python cli.py --symbol BTCUSDT --side BUY --order-type LIMIT --quantity 0.01 --price 30000
      python cli.py --symbol BTCUSDT --side SELL --order-type STOP_MARKET --quantity 0.01 --stop-price 29000
      python cli.py --symbol BTCUSDT --side SELL --order-type STOP --quantity 0.01 --stop-price 29000 --price 28500
    """

    # --- Interactive mode ---
    if interactive or symbol is None:
        try:
            symbol, side, order_type, quantity, price, stop_price = _run_interactive_mode()
        except typer.Exit:
            raise

    else:
        # --- Flag mode: validate required flags ---
        missing = []
        if not side:
            missing.append("--side")
        if not order_type:
            missing.append("--order-type")
        if quantity is None:
            missing.append("--quantity")
        if missing:
            _abort(f"Missing required options: {', '.join(missing)}")

        typer.echo("\n" + "─" * 50)
        typer.echo("  ORDER SUMMARY")
        typer.echo("─" * 50)
        typer.echo(f"  Symbol     : {symbol.upper()}")
        typer.echo(f"  Side       : {side.upper()}")
        typer.echo(f"  Type       : {order_type.upper()}")
        typer.echo(f"  Quantity   : {quantity}")
        if price is not None:
            typer.echo(f"  Price      : {price}")
        if stop_price is not None:
            typer.echo(f"  Stop Price : {stop_price}")
        typer.echo("─" * 50)

    # --- Place order ---
    try:
        response = place_order(
            symbol=symbol,
            side=side,
            order_type=order_type,
            quantity=quantity,
            price=price,
            stop_price=stop_price,
        )
        typer.echo(format_order_result(response))

    except ValueError as e:
        logger.warning(f"Validation failed: {e}")
        _abort(str(e))
    except EnvironmentError as e:
        logger.error(f"Configuration error: {e}")
        _abort(str(e))
    except RuntimeError as e:
        logger.error(f"Order failed: {e}")
        _abort(str(e))
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        _abort(f"Unexpected error: {e}")


if __name__ == "__main__":
    app()