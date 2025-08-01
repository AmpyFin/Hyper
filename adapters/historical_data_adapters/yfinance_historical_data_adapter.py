import logging
from adapters.historical_data_adapters.historical_data_adapter import HistoricalDataAdapter
from datetime import datetime
from typing import Any, List, Dict
import yfinance as yf
import pandas as pd
from registries.standards.adapter_standards import daily, weekly, monthly, annually
from registries.standards.adapter_standards import df_open, df_high, df_low, df_close, df_volume, df_datetime

class YFinanceHistoricalDataAdapter(HistoricalDataAdapter):
    TICKER_FREQ_MAP = {
        daily: '1d',
        weekly: '1wk',
        monthly: '1mo',
    }

    def get_historical_data(
        self,
        ticker: str,
        start_date: datetime,
        end_date: datetime,
        tick_increment: str = daily,
    ) -> List[Dict[str, Any]]:
        """
        Fetch historical price data from yfinance for a given ticker and date range.
        Returns a list of dicts with columns: DateTime, open, close, high, low (all floats rounded to 2 decimal places), volume (int).
        Only supports tick_increment: 'daily', 'weekly', 'monthly'.
        """
        if tick_increment == annually:
            raise ValueError(f"yfinance does not support '{annually}' tick_increment. Use '{daily}', '{weekly}', or '{monthly}'.")
        
        yf_freq = self.TICKER_FREQ_MAP.get(tick_increment)
        if yf_freq is None:
            raise ValueError(f"Invalid tick_increment '{tick_increment}'. Must be one of {list(self.TICKER_FREQ_MAP.keys())}.")
        
        try:
            data = yf.Ticker(ticker)
            hist = data.history(start=start_date, end=end_date, interval=yf_freq)
            
            if hist.empty:
                logging.info(f"No historical data returned for {ticker} with increment {tick_increment}")
                return []
            
            # Debug info
            logging.info(f"Retrieved data for {ticker}:")
            logging.info(f"Shape: {hist.shape}")
            logging.info(f"Columns: {hist.columns.tolist()}")
            logging.info(f"First row:\n{hist.iloc[0]}")
            
            # Reset index to get Date as a column and standardize column names
            hist = hist.reset_index()
            hist.columns = hist.columns.str.lower()
            
            standardized = []
            for _, row in hist.iterrows():
                try:
                    # Convert timestamp to string in ISO format
                    date_str = row['date'].isoformat() if isinstance(row['date'], pd.Timestamp) else str(row['date'])
                    
                    record = {
                        df_datetime: date_str,
                        df_open: round(float(row['open']), 2) if not pd.isna(row['open']) else None,
                        df_close: round(float(row['close']), 2) if not pd.isna(row['close']) else None,
                        df_high: round(float(row['high']), 2) if not pd.isna(row['high']) else None,
                        df_low: round(float(row['low']), 2) if not pd.isna(row['low']) else None,
                        df_volume: int(round(float(row['volume']))) if not pd.isna(row['volume']) else None,
                    }
                    standardized.append(record)
                except Exception as row_error:
                    logging.error(f"Error processing row {row.to_dict()}: {row_error}")
                    continue
                    
            return standardized
            
        except Exception as e:
            logging.error(f"YFinanceHistoricalDataAdapter error for {ticker}: {str(e)}")
            logging.error(f"Full traceback:", exc_info=True)
            return []
