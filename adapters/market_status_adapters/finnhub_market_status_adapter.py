from registries.standards.adapter_standards import market_open, market_closed, market_pre_market
from adapters.market_status_adapters.market_status_adapter import MarketStatusAdapter
from config import FINNHUB_API_KEY
import finnhub

class FinnhubMarketStatusAdapter(MarketStatusAdapter):
    def get_market_status(self) -> str:
        finnhub_client = finnhub.Client(api_key=FINNHUB_API_KEY)
        market_status =finnhub_client.market_status(exchange='US')

        if market_status['session'] == 'regular':
            return market_open
        elif market_status['session'] == 'post-market' or market_status['session'] is None:
            return market_closed
        elif market_status['session'] == 'pre-market':
            return market_pre_market
        else:
            raise ValueError(f"Unknown market status in Finnhub Market Status Adapter: {market_status['session']}")

