import pytest
from datetime import datetime, timedelta
from adapters.historical_data_adapters.tiingo_historical_data_adapter import TiingoHistoricalDataAdapter
from registries.standards.adapter_standards import (
    intraday_1min, intraday_5min, intraday_10min, intraday_30min, intraday_1hour,
    df_open, df_high, df_low, df_close, df_volume, df_datetime
)
import json
from pprint import pformat

@pytest.fixture
def adapter():
    return TiingoHistoricalDataAdapter()

@pytest.fixture
def date_range():
    # Use yesterday's date to ensure we have data (market hours)
    end_date = datetime.now() - timedelta(days=1)
    start_date = end_date - timedelta(days=1)
    
    # Adjust to market hours (9:30 AM - 4:00 PM ET)
    start_date = start_date.replace(hour=9, minute=30, second=0, microsecond=0)
    end_date = end_date.replace(hour=16, minute=0, second=0, microsecond=0)
    
    return start_date, end_date

def print_records(data, freq):
    """Print records in a readable format."""
    print(f"\nDetailed {freq} frequency data:")
    print(f"Total records: {len(data)}")
    print("\nAll records:")
    print("-" * 100)
    print(f"{df_datetime:<25} {df_open:>10} {df_high:>10} {df_low:>10} {df_close:>10} {df_volume:>12}")
    print("-" * 100)
    
    for record in data:
        dt = record[df_datetime].replace('T', ' ').replace('.000Z', '')
        print(f"{dt:<25} {record[df_open]:>10.2f} {record[df_high]:>10.2f} {record[df_low]:>10.2f} {record[df_close]:>10.2f} {record[df_volume]:>12,d}")
    print("-" * 100)
    
    # Save to file for reference
    filename = f"logs/tiingo_intraday_{freq}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"\nFull data saved to: {filename}")

def test_intraday_frequencies(adapter, date_range):
    """Test different intraday frequencies for AAPL."""
    start_date, end_date = date_range
    ticker = "AAPL"
    
    print(f"\nTesting intraday data from {start_date} to {end_date}")
    
    # Test all intraday frequencies
    frequencies = [intraday_1min, intraday_5min, intraday_10min, intraday_30min, intraday_1hour]
    
    for freq in frequencies:
        print(f"\n{'='*50}")
        print(f"Testing {freq} frequency:")
        print(f"{'='*50}")
        
        data = adapter.get_historical_data(ticker, start_date, end_date, freq)
        
        # Basic validation
        assert len(data) > 0, f"No data returned for {freq} frequency"
        
        # Check data structure
        first_record = data[0]
        assert df_datetime in first_record
        assert df_open in first_record
        assert df_close in first_record
        assert df_high in first_record
        assert df_low in first_record
        assert df_volume in first_record
        
        # Print all records in a readable format
        print_records(data, freq)
        
        # Validate data types
        assert isinstance(first_record[df_open], float), "Open price should be float"
        assert isinstance(first_record[df_close], float), "Close price should be float"
        assert isinstance(first_record[df_high], float), "High price should be float"
        assert isinstance(first_record[df_low], float), "Low price should be float"
        assert isinstance(first_record[df_volume], int), "Volume should be int"
        
        # Validate price rounding
        assert str(first_record[df_open]).split('.')[-1] <= '99', "Open price has more than 2 decimal places"
        assert str(first_record[df_close]).split('.')[-1] <= '99', "Close price has more than 2 decimal places"
        
        # Validate data consistency
        assert first_record[df_high] >= first_record[df_low], "High price should be >= low price"
        assert first_record[df_volume] >= 0, "Volume should be non-negative"

def test_invalid_frequency(adapter, date_range):
    """Test that invalid frequencies raise ValueError."""
    start_date, end_date = date_range
    ticker = "AAPL"
    
    with pytest.raises(ValueError) as exc_info:
        adapter.get_historical_data(ticker, start_date, end_date, "2min")
    assert "Invalid tick_increment" in str(exc_info.value)

if __name__ == "__main__":
    # Create logs directory if it doesn't exist
    import os
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    # Run tests
    adapter = TiingoHistoricalDataAdapter()
    
    # Use yesterday's date during market hours
    end_date = datetime.now() - timedelta(days=1)
    end_date = end_date.replace(hour=16, minute=0, second=0, microsecond=0)
    start_date = end_date - timedelta(days=1)
    start_date = start_date.replace(hour=9, minute=30, second=0, microsecond=0)
    
    print("\nTesting intraday data fetching for AAPL...")
    test_intraday_frequencies(adapter, (start_date, end_date))
    
    print("\nTesting invalid frequency handling...")
    try:
        test_invalid_frequency(adapter, (start_date, end_date))
        print("Invalid frequency test passed!")
    except Exception as e:
        print(f"Invalid frequency test failed: {e}") 