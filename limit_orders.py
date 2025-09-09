import argparse
from .binance_client import BinanceClient
from .validators import validate_symbol, validate_qty, validate_price, require_all
from .logger import get_logger

logger = get_logger("limit")

def main():
    p = argparse.ArgumentParser(description="Place a LIMIT order on USDT-M Futures")
    p.add_argument("symbol")
    p.add_argument("side", choices=["BUY","SELL"])
    p.add_argument("qty", type=float)
    p.add_argument("price", type=float)
    p.add_argument("--tif", default="GTC", choices=["GTC","IOC","FOK","GTX"])
    args = p.parse_args()

    require_all(
        validate_symbol(args.symbol),
        validate_qty(args.qty),
        validate_price(args.price),
    )

    client = BinanceClient()
    resp = client.new_order(
        symbol=args.symbol,
        side=args.side,
        type="LIMIT",
        quantity=args.qty,
        price=str(args.price),
        timeInForce=args.tif
    )
    logger.info(f"ORDER RESULT: {resp}")
    print(resp)

if __name__ == "__main__":
    main()
