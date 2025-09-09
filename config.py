import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass
class Settings:
    api_key: str = os.getenv("BINANCE_API_KEY", "o6cS93zRSXNzndm2I1O7WYx82QwFZSOmGGMcF8IAVrm4x89Z3MnKRXhYY8hnYqaT")
    api_secret: str = os.getenv("BINANCE_API_SECRET", "Nuul35Tf3RWWPZK86ZNEaSGMkcheb7xlpYhLmgKScAWm1IPVaVYQvh9maAqtPFmD")
    # Use Testnet by default (SAFE). Switch to False only if you know what you're doing.
    use_testnet: bool = os.getenv("BINANCE_USE_TESTNET", "true").lower() == "true"

    @property
    def base_url(self) -> str:
        # USDT-M Futures base endpoints (prod/testnet)
        return "https://testnet.binancefuture.com" if self.use_testnet else "https://fapi.binance.com"

settings = Settings()
