import logging
from adapters.current_price_adapters.current_price_adapter import CurrentPriceAdapter
import yfinance as yf

class YFinanceCurrentPriceAdapter(CurrentPriceAdapter):
    def get_current_price(self, ticker: str) -> float:
        """
        Returns the latest available current price for the given ticker as a float using yfinance, rounded to 2 decimal places.
        If no price is available, returns None.
        """
        try:
            data = yf.Ticker(ticker)
            # Try to get the real-time price from fast_info or info
            price = None
            if hasattr(data, 'fast_info') and data.fast_info is not None:
                price = data.fast_info.get('last_price')
            if price is None:
                # Fallback to info dict
                info = getattr(data, 'info', None)
                if info and 'regularMarketPrice' in info:
                    price = info['regularMarketPrice']
            if price is None:
                # Fallback to latest close
                hist = data.history(period="1d")
                if not hist.empty:
                    price = hist['Close'].iloc[-1]
            if price is not None:
                return round(float(price), 2)
            else:
                logging.info(f"No current price data returned for {ticker}")
                return None
        except Exception as e:
            logging.error(f"YFinanceCurrentPriceAdapter error: {e}")
            return None
