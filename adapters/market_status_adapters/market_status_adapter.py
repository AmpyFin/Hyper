from abc import ABC, abstractmethod

class MarketStatusAdapter(ABC):
    @abstractmethod
    def get_market_status(
    ) -> str:
        """
        Returns:
            market status (open, closed, pre-market)
        """
        pass
