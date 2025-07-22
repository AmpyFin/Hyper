import requests
from typing import List
from .ticker_adapter import TickerAdapter

class ARKKHoldingsTickersAdapter(TickerAdapter):
    """
    Adapter for fetching ARKK ETF holdings tickers from ARK Funds API.
    """
    
    def __init__(self):
        self.api_url = "https://arkfunds.io/api/v2/etf/holdings"
        
    def fetch_tickers(self) -> List[str]:
        """
        Retrieve a list of tickers from ARKK holdings.
        Returns a list of ticker symbols as strings, excluding any null values.
        """
        try:
            # Make request to ARK Funds API
            params = {
                "symbol": "ARKK",
                "limit": 1000  # Get maximum available holdings
            }
            response = requests.get(self.api_url, params=params)
            response.raise_for_status()  # Raise exception for bad status codes
            
            # Parse response JSON
            data = response.json()
            
            # Extract tickers, filter out None/null values
            tickers = [
                holding["ticker"] 
                for holding in data.get("holdings", [])
                if holding.get("ticker") is not None
            ]
            
            return tickers
            
        except requests.RequestException as e:
            raise RuntimeError(f"Failed to fetch ARKK holdings: {str(e)}")
        except (KeyError, ValueError) as e:
            raise RuntimeError(f"Failed to parse ARKK holdings data: {str(e)}")
