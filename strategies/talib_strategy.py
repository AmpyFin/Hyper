import talib
import pandas as pd
import numpy as np
from registries.strategy_registries import strategy_ideal_periods, strategy_ideal_number_dataframes
from strategies.strategy import Strategy
from registries.standards.adapter_standards import df_open, df_high, df_low, df_close, df_volume, df_datetime

class AD_Strategy(Strategy):
    def get_strategy_name(self):
        return "chaikin_ad_line"
    
    def get_ideal_period(self):
        return strategy_ideal_periods[self.get_strategy_name()]

    def get_ideal_number_dataframes(self):
        return strategy_ideal_number_dataframes[self.get_strategy_name()]
    
    def run_strategy(self, historical_data, current_price):
        # Convert list of dicts to DataFrame if necessary
        if isinstance(historical_data, list):
            historical_data = pd.DataFrame(historical_data)
        
        # Validate input data
        if not self.validate_historical_data(historical_data):
            logging.error(f"Historical data is invalid for strategy {self.get_strategy_name()}")
            return 0
        
        # Convert data types to float64 for TA-Lib
        for col in [df_high, df_low, df_close, df_volume]:
            historical_data[col] = historical_data[col].astype(np.float64)
        
        # Calculate Chaikin A/D Line
        ad_line = talib.AD(historical_data[df_high].values, historical_data[df_low].values, 
                          historical_data[df_close].values, historical_data[df_volume].values)
        
        # Get the last two values to determine trend
        if len(ad_line) < 2:
            raise ValueError("Not enough data points to calculate trend (need at least 2)")
            
        last_ad = ad_line[-1]
        prev_ad = ad_line[-2]
        
        # Calculate percentage change in A/D line
        ad_change = (last_ad - prev_ad) / abs(prev_ad) if prev_ad != 0 else 0
        
        # Convert change to sentiment score between -1 and 1
        sentiment_score = np.clip(ad_change, -1, 1)
        
        # Validate sentiment score
        if not self.validate_sentiment_score(sentiment_score):
            logging.error(f"Sentiment score {sentiment_score} is outside valid range [-1, 1]")
            return 0
        
        return float(sentiment_score)