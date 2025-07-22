from abc import ABC, abstractmethod
from typing import List

class TickerAdapter(ABC):
    @abstractmethod
    def fetch_tickers(self) -> List[str]:
        """
        Retrieve a list of tickers as strings.
        """
        pass
