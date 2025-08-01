import pytest
import pandas as pd
from datetime import datetime, timedelta
from strategies.talib_strategy import AD_Strategy
from registries.adapter_registries import (
    current_price_adapter,
    historical_data_adapter,
    tickers_adapter
)

def test_ad_strategy():
    print("\n" + "="*80)
    print("Running Chaikin A/D Line Strategy Test")
    print("="*80)
    
    # Initialize strategy
    strategy = AD_Strategy()
    
    # Get strategy requirements
    period = strategy.get_ideal_period()  # This will be used for tick_increment
    num_dataframes = strategy.get_ideal_number_dataframes()
    
    # Calculate date range based on period
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)  # Get 30 days of data
    
    print(f"\nAnalyzing data from {start_date.date()} to {end_date.date()}")
    print(f"Using period: {period}")
    print("-"*80)
    
    # Get test tickers
    tickers = tickers_adapter.fetch_tickers() # Test with all tickers for better sample
    
    results = {}
    for ticker in tickers:
        try:
            # Get current price
            current_price = current_price_adapter.get_current_price(ticker)
            
            # Get historical data
            historical_data = historical_data_adapter.get_historical_data(
                ticker=ticker,
                start_date=start_date,
                end_date=end_date,
                tick_increment=period  # Use the strategy's ideal period as tick increment
            )
            
            # Run strategy
            sentiment_score = strategy.run_strategy(historical_data, current_price)
            
            # Store results
            results[ticker] = {
                'sentiment_score': sentiment_score,
                'current_price': current_price
            }
            
            # Validate sentiment score
            assert -1 <= sentiment_score <= 1, f"Sentiment score {sentiment_score} for {ticker} outside valid range"
            
            # Print individual result with sentiment interpretation
            sentiment_text = "NEUTRAL"
            if sentiment_score > 0.5:
                sentiment_text = "STRONGLY BULLISH"
            elif sentiment_score > 0:
                sentiment_text = "MILDLY BULLISH"
            elif sentiment_score < -0.5:
                sentiment_text = "STRONGLY BEARISH"
            elif sentiment_score < 0:
                sentiment_text = "MILDLY BEARISH"
                
            print(f"\nTicker: {ticker}")
            print(f"Current Price: ${current_price:.2f}")
            print(f"Sentiment Score: {sentiment_score:.4f} ({sentiment_text})")
            
        except Exception as e:
            print(f"\nError processing {ticker}: {str(e)}")
            continue
    
    # Ensure we got results for at least one ticker
    assert len(results) > 0, "No results were generated for any tickers"
    
    # Print summary statistics
    sentiment_scores = [r['sentiment_score'] for r in results.values()]
    
    print("\n" + "="*80)
    print("Summary Statistics")
    print("="*80)
    print(f"Number of Tickers Processed: {len(results)}")
    print(f"Average Sentiment: {sum(sentiment_scores) / len(sentiment_scores):.4f}")
    
    # Sort tickers by sentiment score
    sorted_results = sorted(results.items(), key=lambda x: x[1]['sentiment_score'], reverse=True)
    
    print("\nRanked by Sentiment (Top to Bottom):")
    print("-"*80)
    for ticker, data in sorted_results:
        sentiment = data['sentiment_score']
        price = data['current_price']
        print(f"{ticker:6} | Score: {sentiment:8.4f} | Price: ${price:8.2f}")

if __name__ == "__main__":
    test_ad_strategy() 