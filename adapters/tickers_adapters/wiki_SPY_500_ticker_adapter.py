import pandas as pd
from typing import List
from .ticker_adapter import TickerAdapter

class WikiSPY500TickerAdapter(TickerAdapter):
    """
    Adapter for fetching S&P 500 tickers from Wikipedia.
    """
    
    def __init__(self):
        self.wiki_url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies#S&P_500_component_stocks"
        
    def fetch_tickers(self) -> List[str]:
        """
        Retrieve a list of tickers from S&P 500 index using Wikipedia data.
        Returns a list of ticker symbols as strings.
        """
        try:
            # Read the Wikipedia table
            df = pd.read_html(self.wiki_url, header=0)[0]
            
            # Extract tickers from the 'Symbol' column
            tickers = df['Symbol'].tolist()
            
            # Clean tickers (remove any whitespace and convert to strings)
            tickers = [str(ticker).strip() for ticker in tickers if pd.notna(ticker)]
            
            if not tickers:
                raise RuntimeError("No tickers returned from Wikipedia")
                
            return tickers[:500]  # Ensure we return at most 500 tickers
            
        except Exception as e:
            raise RuntimeError(f"Failed to fetch S&P 500 tickers: {str(e)}")
