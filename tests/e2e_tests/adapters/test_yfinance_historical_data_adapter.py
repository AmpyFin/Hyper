from datetime import datetime, timedelta
from adapters.historical_data_adapters.yfinance_historical_data_adapter import YFinanceHistoricalDataAdapter
from registries.standards.adapter_standards import (
    daily, weekly, monthly, annually
)
import pandas as pd

if __name__ == "__main__":
    adapter = YFinanceHistoricalDataAdapter()
    tickers = ["AAPL", "MSFT", "TSLA", "META"]
    increments = [daily, weekly, monthly]  # Removed annually since it's not supported
    
    # Use more recent dates - last month
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    
    print(f"Testing date range: {start_date} to {end_date}")

    for ticker in tickers:
        for inc in increments:
            print(f"\n{'='*50}")
            print(f"Testing {ticker} | {inc}")
            print(f"{'='*50}")
            try:
                data = adapter.get_historical_data(
                    ticker=ticker,
                    start_date=start_date,
                    end_date=end_date,
                    tick_increment=inc
                )
                print(f"Records returned: {len(data)}")
                if len(data) > 0:
                    print("\nFirst record:")
                    print(pd.DataFrame([data[0]]).to_string())
                    print("\nLast record:")
                    print(pd.DataFrame([data[-1]]).to_string())
                else:
                    print("No records returned")
            except Exception as e:
                print(f"Error: {str(e)}")
                import traceback
                print(traceback.format_exc())

    # Demonstrate invalid tick_increment
    print("\n--- Invalid tick_increment test ---")
    try:
        adapter.get_historical_data(
            ticker="AAPL",
            start_date=start_date,
            end_date=end_date,
            tick_increment="1d"
        )
    except Exception as e:
        print(f"Expected error for invalid tick_increment: {e}")

    # all documentation for standardization format must be done in docs directory and respective subdirectory
    # document a standardized format for historical data and current price - must return what format of dataframe -> open, low, high, close, volume etc.