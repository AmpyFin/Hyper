import logging
from config import Tiingo_API_KEY
from adapters.historical_data_adapters.historical_data_adapter import HistoricalDataAdapter
from datetime import datetime
import requests
from typing import Any, List, Dict

class TiingoHistoricalDataAdapter(HistoricalDataAdapter):
    BASE_URL = "https://api.tiingo.com/tiingo/daily/{ticker}/prices"

    def get_historical_data(
        self,
        ticker: str,
        start_date: datetime,
        end_date: datetime,
        tick_increment: str = 'daily',
    ) -> List[Dict[str, Any]]:
        """
        Fetch historical price data from Tiingo for a given ticker and date range.
        Note: Tiingo only supports resampleFreq values: 'daily', 'weekly', 'monthly', 'annually'.
        """
        valid_freqs = {'daily', 'weekly', 'monthly', 'annually'}
        if tick_increment not in valid_freqs:
            raise ValueError(f"Invalid tick_increment '{tick_increment}'. Must be one of {valid_freqs}.")
        url = self.BASE_URL.format(ticker=ticker)
        params = {
            "startDate": start_date.strftime("%Y-%m-%d"),
            "endDate": end_date.strftime("%Y-%m-%d"),
            "resampleFreq": tick_increment,
            "token": Tiingo_API_KEY,
        }
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            return data
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