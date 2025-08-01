import logging
from config import Tiingo_API_KEY
from adapters.historical_data_adapters.historical_data_adapter import HistoricalDataAdapter
from datetime import datetime, timedelta
import requests
from typing import Any, List, Dict
from registries.standards.adapter_standards import daily, weekly, monthly, annually, intraday_1min, intraday_5min, intraday_10min, intraday_30min, intraday_1hour
from registries.standards.adapter_standards import df_open, df_high, df_low, df_close, df_volume, df_datetime

class TiingoHistoricalDataAdapter(HistoricalDataAdapter):
    DAILY_URL = "https://api.tiingo.com/tiingo/daily/{ticker}/prices"
    INTRADAY_URL = "https://api.tiingo.com/iex/{ticker}/prices"

    # Valid frequencies for each endpoint
    DAILY_FREQS = {daily, weekly, monthly, annually}
    INTRADAY_FREQS = {intraday_1min, intraday_5min, intraday_10min, intraday_30min, intraday_1hour}

    def get_historical_data(
        self,
        ticker: str,
        start_date: datetime,
        end_date: datetime,
        tick_increment: str = daily,
    ) -> List[Dict[str, Any]]:
        """
        Fetch historical price data from Tiingo for a given ticker and date range.
        Returns a list of dicts with columns: DateTime, open, close, high, low (all floats rounded to 2 decimal places), volume (int).
        
        Supported tick_increments:
        - Daily data: 'daily', 'weekly', 'monthly', 'annually'
        - Intraday data: '1min', '5min', '10min', '30min', '1hour'
        
        Note: Intraday data is only available during market hours and for a limited time range.
        For intraday data, the date range should typically be within the last 5 trading days.
        """
        # Determine which endpoint to use based on tick_increment
        if tick_increment in self.DAILY_FREQS:
            return self._get_daily_data(ticker, start_date, end_date, tick_increment)
        elif tick_increment in self.INTRADAY_FREQS:
            # For intraday data, limit the date range to last 5 days to ensure data availability
            adjusted_start = max(start_date, end_date - timedelta(days=5))
            return self._get_intraday_data(ticker, adjusted_start, end_date, tick_increment)
        else:
            valid_freqs = self.DAILY_FREQS.union(self.INTRADAY_FREQS)
            raise ValueError(f"Invalid tick_increment '{tick_increment}'. Must be one of {valid_freqs}.")

    def _get_daily_data(
        self,
        ticker: str,
        start_date: datetime,
        end_date: datetime,
        tick_increment: str
    ) -> List[Dict[str, Any]]:
        """Fetch daily, weekly, monthly, or annual data."""
        url = self.DAILY_URL.format(ticker=ticker)
        params = {
            "startDate": start_date.strftime("%Y-%m-%d"),
            "endDate": end_date.strftime("%Y-%m-%d"),
            "resampleFreq": tick_increment,
            "token": Tiingo_API_KEY,
        }
        return self._make_request(url, params)

    def _get_intraday_data(
        self,
        ticker: str,
        start_date: datetime,
        end_date: datetime,
        tick_increment: str
    ) -> List[Dict[str, Any]]:
        """Fetch intraday data with specified frequency."""
        url = self.INTRADAY_URL.format(ticker=ticker)
        params = {
            "startDate": start_date.strftime("%Y-%m-%d"),
            "endDate": end_date.strftime("%Y-%m-%d"),
            "resampleFreq": tick_increment,
            "columns": f"{df_open},{df_high},{df_low},{df_close},{df_volume}",
            "token": Tiingo_API_KEY,
            "forceFill": "true"  # Fill missing data points
        }
        return self._make_request(url, params)

    def _make_request(self, url: str, params: Dict[str, str]) -> List[Dict[str, Any]]:
        """Make request to Tiingo API and standardize response."""
        headers = {
            'Content-Type': 'application/json'
        }
        try:
            response = requests.get(url, params=params, headers=headers)
            response.raise_for_status()
            data = response.json()
            
            # Handle empty response
            if not data:
                logging.warning(f"No data returned from Tiingo API for URL: {url} with params: {params}")
                return []
            
            # Standardize and round data
            standardized = []
            for row in data:
                # Skip rows with missing required data
                if not all(key in row for key in ['date', 'open', 'close', 'high', 'low', 'volume']):
                    continue
                    
                try:
                    standardized.append({
                        df_datetime: row['date'],
                        df_open: round(float(row['open']), 2),
                        df_close: round(float(row['close']), 2),
                        df_high: round(float(row['high']), 2),
                        df_low: round(float(row['low']), 2),
                        df_volume: int(round(float(row['volume'])))
                    })
                except (ValueError, TypeError) as e:
                    logging.warning(f"Error processing row {row}: {e}")
                    continue
                    
            return standardized
        except requests.RequestException as e:
            self.handle_error(e, getattr(e, 'response', None))
            return []

    def handle_error(self, error: Exception, response=None):
        logging.error(f"TiingoHistoricalDataAdapter error: {error}")
        if response is not None:
            try:
                logging.warning(f"Response content: {response.text}")
            except Exception:
                pass