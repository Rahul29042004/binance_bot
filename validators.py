from typing import Tuple

def validate_symbol(symbol: str) -> Tuple[bool, str]:
    ok = symbol.isalnum() and symbol.endswith("USDT")
    return ok, "Symbol must look like BTCUSDT/ETHUSDT etc."

def validate_qty(qty: float) -> Tuple[bool, str]:
    return (qty > 0), "Quantity must be > 0"

def validate_price(price: float) -> Tuple[bool, str]:
    return (price > 0), "Price must be > 0"

def require_all(*checks):
    for ok, msg in checks:
        if not ok:
            raise ValueError(msg)

