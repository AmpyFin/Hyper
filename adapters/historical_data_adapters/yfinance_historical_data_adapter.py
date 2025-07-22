import logging
from adapters.historical_data_adapters.historical_data_adapter import HistoricalDataAdapter
from datetime import datetime
from typing import Any, List, Dict
import yfinance as yf
import pandas as pd

class YFinanceHistoricalDataAdapter(HistoricalDataAdapter):
    TICKER_FREQ_MAP = {
        'daily': '1d',
        'weekly': '1wk',
        'monthly': '1mo',
    }

    def get_historical_data(
        self,
        ticker: str,
        start_date: datetime,
        end_date: datetime,
        tick_increment: str = 'daily',
    ) -> List[Dict[str, Any]]:
        """
        Fetch historical price data from yfinance for a given ticker and date range.
        Returns a list of dicts with columns: DateTime, open, close, high, low (all floats rounded to 2 decimal places), volume (int).
        Only supports tick_increment: 'daily', 'weekly', 'monthly'.
        """
        if tick_increment == 'annually':
            raise ValueError("yfinance does not support 'annually' tick_increment. Use 'daily', 'weekly', or 'monthly'.")
        yf_freq = self.TICKER_FREQ_MAP.get(tick_increment)
        if yf_freq is None:
            raise ValueError(f"Invalid tick_increment '{tick_increment}'. Must be one of {list(self.TICKER_FREQ_MAP.keys())}.")
        try:
            data = yf.Ticker(ticker)
            hist = data.history(start=start_date, end=end_date, interval=yf_freq)
            if hist.empty:
                logging.info(f"No historical data returned for {ticker} with increment {tick_increment}")
                return []
            # Standardize and round data
            hist = hist.reset_index()
            standardized = []
            for _, row in hist.iterrows():
                standardized.append({
                    'DateTime': row['Date'] if 'Date' in row else row['index'],
                    'open': round(float(row['Open']), 2) if not pd.isna(row['Open']) else None,
                    'close': round(float(row['Close']), 2) if not pd.isna(row['Close']) else None,
                    'high': round(float(row['High']), 2) if not pd.isna(row['High']) else None,
                    'low': round(float(row['Low']), 2) if not pd.isna(row['Low']) else None,
                    'volume': int(round(row['Volume'])) if not pd.isna(row['Volume']) else None,
                })
            return standardized
        except Exception as e:
            logging.error(f"YFinanceHistoricalDataAdapter error: {e}")
            return []
