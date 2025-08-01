from adapters.market_status_adapters.finnhub_market_status_adapter import FinnhubMarketStatusAdapter
from registries.standards.adapter_standards import market_open, market_closed, market_pre_market

finnhub_market_status_adapter = FinnhubMarketStatusAdapter()

def test_get_market_status():
    market_status = finnhub_market_status_adapter.get_market_status()
    assert market_status in [market_open, market_closed, market_pre_market]
    print(f"Market status: {market_status}")

test_get_market_status()