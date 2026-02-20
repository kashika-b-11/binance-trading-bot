import os
import requests
import time
import hmac
import hashlib
from urllib.parse import urlencode
from dotenv import load_dotenv
from bot.logging_config import setup_logger

load_dotenv()

logger = setup_logger()

BASE_URL = "https://testnet.binancefuture.com"


class BinanceFuturesClient:
    """
    Lightweight REST client for Binance Futures Testnet (USDT-M).
    Uses direct HTTP calls via `requests` — no third-party Binance SDK needed.
    """

    def __init__(self, api_key: str, api_secret: str, base_url: str = BASE_URL):
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            "X-MBX-APIKEY": self.api_key,
            "Content-Type": "application/x-www-form-urlencoded",
        })

    def _sign(self, params: dict) -> dict:
        """Append timestamp and HMAC-SHA256 signature to params."""
        params["timestamp"] = int(time.time() * 1000)
        query_string = urlencode(params)
        signature = hmac.new(
            self.api_secret.encode("utf-8"),
            query_string.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()
        params["signature"] = signature
        return params

    def new_order(self, **kwargs) -> dict:
        """
        POST /fapi/v1/order — Place a new futures order.
        All keyword arguments are forwarded as order parameters.
        """
        endpoint = f"{self.base_url}/fapi/v1/order"
        params = self._sign(kwargs)

        logger.debug(f"POST {endpoint} | Params: { {k: v for k, v in params.items() if k != 'signature'} }")

        try:
            response = self.session.post(endpoint, data=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            logger.debug(f"Raw API Response: {data}")
            return data
        except requests.exceptions.HTTPError as e:
            error_body = e.response.json() if e.response is not None else {}
            logger.error(f"HTTP Error {e.response.status_code}: {error_body}")
            raise RuntimeError(
                f"Binance API Error {error_body.get('code', '?')}: {error_body.get('msg', str(e))}"
            ) from e
        except requests.exceptions.ConnectionError:
            logger.error("Network connection failed. Check your internet connection.")
            raise RuntimeError("Network connection error. Unable to reach Binance Testnet.")
        except requests.exceptions.Timeout:
            logger.error("Request timed out.")
            raise RuntimeError("Request timed out. The Binance Testnet may be slow or unreachable.")


def get_client() -> BinanceFuturesClient:
    """
    Load API credentials from environment and return a configured client.
    Raises a clear error if credentials are missing.
    """
    api_key = os.getenv("API_KEY")
    api_secret = os.getenv("API_SECRET")

    if not api_key or not api_secret:
        raise EnvironmentError(
            "API_KEY and API_SECRET must be set in your .env file. "
            "See .env.example for reference."
        )

    return BinanceFuturesClient(api_key=api_key, api_secret=api_secret)