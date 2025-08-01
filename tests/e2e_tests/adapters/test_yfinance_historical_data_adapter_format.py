from datetime import datetime
from adapters.historical_data_adapters.yfinance_historical_data_adapter import YFinanceHistoricalDataAdapter
from registries.standards.adapter_standards import (
    daily, weekly, monthly,
    df_datetime, df_open, df_high, df_low, df_close, df_volume
)

EXPECTED_COLUMNS = [df_datetime, df_open, df_close, df_high, df_low, df_volume]
EXPECTED_TYPES = {
    df_datetime: None,  # Accepts datetime or string, just check presence
    df_open: float,
    df_close: float,
    df_high: float,
    df_low: float,
    df_volume: int,
}

if __name__ == "__main__":
    adapter = YFinanceHistoricalDataAdapter()
    ticker = "AAPL"
    increments = [daily, weekly, monthly]  # Removed annually since it's not supported
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2023, 1, 10)

    for inc in increments:
        print(f"\n--- {ticker} | {inc} ---")
        data = adapter.get_historical_data(
            ticker=ticker,
            start_date=start_date,
            end_date=end_date,
            tick_increment=inc
        )
        if not data:
            print("No data returned.")
            continue
        
        # Check columns
        for i, record in enumerate(data):
            missing = [col for col in EXPECTED_COLUMNS if col not in record]
            if missing:
                print(f"Record {i}: Missing columns: {missing}")
            
            # Check types and rounding
            for col, typ in EXPECTED_TYPES.items():
                val = record.get(col)
                if col == df_datetime:
                    if val is None:
                        print(f"Record {i}: {df_datetime} is missing or None")
                elif val is not None:
                    if typ and not isinstance(val, typ):
                        print(f"Record {i}: {col} is not {typ.__name__} (got {type(val).__name__})")
                    if typ is float and val is not None:
                        # Check rounding to 2 decimals
                        if round(val, 2) != val:
                            print(f"Record {i}: {col} is not rounded to 2 decimals: {val}")
            
            # Only check the first 5 records for brevity
            if i >= 4:
                break
        print("Format check complete for this increment.") 