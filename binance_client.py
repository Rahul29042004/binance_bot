import time, hmac, hashlib, requests
from urllib.parse import urlencode
from config import settings
from logger import get_logger

logger = get_logger("binance")

class BinanceClient:
    def __init__(self, api_key: str = settings.api_key, api_secret: str = settings.api_secret):
        self.api_key = api_key
        self.api_secret = api_secret.encode()
        self.base = settings.base_url

    def _headers(self):
        return {"X-MBX-APIKEY": self.api_key}

    def _sign(self, params: dict):
        qs = urlencode(params, doseq=True)
        sig = hmac.new(self.api_secret, qs.encode(), hashlib.sha256).hexdigest()
        return qs + f"&signature={sig}"

    def _get(self, path: str, params: dict = None, signed: bool = False):
        params = params or {}
        if signed:
            params["timestamp"] = int(time.time() * 1000)
            url = f"{self.base}{path}?{self._sign(params)}"
            r = requests.get(url, headers=self._headers(), timeout=10)
        else:
            url = f"{self.base}{path}"
            r = requests.get(url, params=params, timeout=10)
        r.raise_for_status()
        return r.json()

    def _post(self, path: str, params: dict = None, signed: bool = True):
        params = params or {}
        if signed:
            params["timestamp"] = int(time.time() * 1000)
            payload = self._sign(params)
            url = f"{self.base}{path}"
            r = requests.post(url, headers=self._headers(), data=payload, timeout=10)
        else:
            url = f"{self.base}{path}"
            r = requests.post(url, data=params, timeout=10)
        r.raise_for_status()
        return r.json()

    # --- Market data (simple) ---
    def mark_price(self, symbol: str):
        return self._get("/fapi/v1/premiumIndex", {"symbol": symbol})

    # --- Trading endpoints ---
    def new_order(self, **params):
        """
        Minimal wrapper for POST /fapi/v1/order
        Send fields like symbol, side, type, quantity, price, timeInForce, reduceOnly, stopPrice etc.
        """
        logger.info(f"Placing order: {params}")
        return self._post("/fapi/v1/order", params, signed=True)

    def batch_orders(self, orders: list):
        """
        POST /fapi/v1/batchOrders  (Max 5 orders)
        orders: list of dicts (each is a /order payload)
        """
        return self._post("/fapi/v1/batchOrders", {"batchOrders": orders})
