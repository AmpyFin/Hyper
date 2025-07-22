from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any

class HistoricalDataAdapter(ABC):
    @abstractmethod
    def get_historical_data(
        self,
        ticker: str,
        start_date: datetime,
        end_date: datetime,
        tick_increment: str = '1d',
    ) -> Any:
        """
        Retrieve historical data for a given ticker and date range.
        Args:
            ticker (str): The symbol or asset identifier.
            start_date (datetime): The start of the historical period.
            end_date (datetime): The end of the historical period.
            tick_increment (str, optional): The granularity of the data (e.g., '1d', '1h'). Defaults to '1d'.
        Returns:
            Any: The historical data in a standardized format (to be defined by implementation).
        """
        pass
