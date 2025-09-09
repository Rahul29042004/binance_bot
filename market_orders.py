import argparse
from .binance_client import BinanceClient
from .validators import validate_symbol, validate_qty, require_all
from .logger import get_logger

logger = get_logger("market")

def main():
    p = argparse.ArgumentParser(description="Place a MARKET order on USDT-M Futures (Testnet by default)")
    p.add_argument("symbol", help="e.g., BTCUSDT")
    p.add_argument("side", choices=["BUY","SELL"])
    p.add_argument("qty", type=float, help="contract quantity (e.g., 0.001)")
    args = p.parse_args()

    require_all(
        validate_symbol(args.symbol),
        validate_qty(args.qty),
    )

    client = BinanceClient()
    resp = client.new_order(
        symbol=args.symbol,
        side=args.side,
        type="MARKET",
        quantity=args.qty
    )
    logger.info(f"ORDER RESULT: {resp}")
    print(resp)

if __name__ == "__main__":
    main()
