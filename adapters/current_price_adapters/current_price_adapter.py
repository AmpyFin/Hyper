from abc import ABC, abstractmethod

class CurrentPriceAdapter(ABC):
    @abstractmethod
    def get_current_price(self, ticker: str):
        """
        Retrieve the current price for a given ticker.
        """
        pass
