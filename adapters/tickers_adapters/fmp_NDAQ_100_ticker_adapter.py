import requests
from typing import List
from .ticker_adapter import TickerAdapter
from config import FMP_API_KEY

class FMPNDAQ100TickerAdapter(TickerAdapter):
    """
    Adapter for fetching NASDAQ-100 tickers from Financial Modeling Prep API.
    """
    
    def __init__(self):
        self.api_url = "https://financialmodelingprep.com/api/v3/nasdaq_constituent"
        self.api_key = FMP_API_KEY
        
    def fetch_tickers(self) -> List[str]:
        """
        Retrieve a list of tickers from NASDAQ-100 index.
        Returns a list of ticker symbols as strings.
        """
        try:
            # Make request to FMP API
            params = {
                "apikey": self.api_key
            }
            
            response = requests.get(self.api_url, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            # Extract tickers from the response
            tickers = [company["symbol"] for company in data if company.get("symbol")]
            
            if not tickers:
                raise RuntimeError("No tickers returned from FMP API")
                
            return tickers[:100]  # Ensure we return exactly 100 tickers
            
        except requests.RequestException as e:
            raise RuntimeError(f"Failed to fetch NASDAQ-100 tickers: {str(e)}")
        except (KeyError, ValueError) as e:
            raise RuntimeError(f"Failed to parse NASDAQ-100 tickers data: {str(e)}")
