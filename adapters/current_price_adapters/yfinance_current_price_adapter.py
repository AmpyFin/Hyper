import logging
from adapters.current_price_adapters.current_price_adapter import CurrentPriceAdapter
import yfinance as yf

class YFinanceCurrentPriceAdapter(CurrentPriceAdapter):
    def get_current_price(self, ticker: str) -> float:
        """
        Returns the latest available closing price for the given ticker as a float using yfinance, rounded to 2 decimal places.
        If no price is available, returns None.
        """
        try:
            data = yf.Ticker(ticker)
            hist = data.history(period="1d")
            if not hist.empty:
                price = hist['Close'].iloc[-1]
                return round(float(price), 2)
            else:
                logging.info(f"No price data returned for {ticker}")
                return None
        except Exception as e:
            logging.error(f"YFinanceCurrentPriceAdapter error: {e}")
            return None
