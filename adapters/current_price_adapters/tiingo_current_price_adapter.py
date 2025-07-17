import logging
from config import Tiingo_API_KEY
from adapters.current_price_adapters.current_price_adapter import CurrentPriceAdapter
import requests

class TiingoCurrentPriceAdapter(CurrentPriceAdapter):
    BASE_URL = "https://api.tiingo.com/tiingo/daily/{ticker}/prices"

    def get_current_price(self, ticker: str) -> float:
        """
        Returns the latest available closing price for the given ticker as a float.
        If no price is available, returns None.
        """
        url = self.BASE_URL.format(ticker=ticker)
        params = {
            "token": Tiingo_API_KEY,
        }
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            if data and isinstance(data, list):
                latest = data[-1]
                # Tiingo returns 'close' as the closing price
                price = latest.get('close')
                if price is not None:
                    return float(price)
                else:
                    logging.info(f"No 'close' price found for {ticker}")
                    return None
            else:
                logging.info(f"No price data returned for {ticker}")
                return None
        except requests.RequestException as e:
            logging.error(f"TiingoCurrentPriceAdapter error: {e}")
            if hasattr(e, 'response') and e.response is not None:
                try:
                    logging.warning(f"Response content: {e.response.text}")
                except Exception:
                    pass
            return None
