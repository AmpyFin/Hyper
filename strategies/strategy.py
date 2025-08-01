from abc import ABC, abstractmethod
import pandas as pd
from typing import Union, Literal
from registries.standards.adapter_standards import (
    daily, weekly, monthly, annually,
    intraday_1min, intraday_5min, intraday_10min, intraday_30min, intraday_1hour,
    df_open, df_high, df_low, df_close, df_volume, df_datetime
)

class Strategy(ABC):
    """
    Abstract base class for strategy agents.
    
    Each strategy must implement:
    1. get_strategy_name: Returns the strategy identifier in snake_case
    2. run_strategy: Takes historical data and current price, returns sentiment score
    3. get_ideal_period: Returns the ideal timeframe for the strategy
    """
    
    @abstractmethod
    def get_strategy_name(self) -> str:
        """
        Returns the strategy name in snake_case format.
        
        Returns:
            str: Strategy identifier in snake_case (e.g., 'moving_average_crossover')
        """
        pass
    
    @abstractmethod
    def run_strategy(self, historical_data: pd.DataFrame, current_price: float) -> float:
        """
        Executes the strategy logic and returns a sentiment score.
        
        Args:
            historical_data (pd.DataFrame): Historical price data with required columns:
                - DateTime: Timestamp of the data point
                - open: Opening price
                - high: Highest price
                - low: Lowest price
                - close: Closing price
                - volume: Trading volume
            current_price (float): Latest available price for the asset
            
        Returns:
            float: Sentiment score between -1 and 1
                -1.0 = Most bearish
                -0.5 = Moderately bearish
                 0.0 = Neutral
                +0.5 = Moderately bullish
                +1.0 = Most bullish
        
        Raises:
            ValueError: If the sentiment score is outside [-1, 1] range
            ValueError: If required data columns are missing
        """
        pass
    
    @abstractmethod
    def get_ideal_period(self) -> Union[Literal['1min', '5min', '10min', '30min', '1hour', 'daily', 'weekly', 'monthly']]:
        """
        Returns the ideal timeframe for the strategy.
        
        Returns:
            str: One of the following timeframes:
                - intraday_1min: One-minute data
                - intraday_5min: Five-minute data
                - intraday_10min: Ten-minute data
                - intraday_30min: Thirty-minute data
                - intraday_1hour: Hourly data
                - daily: Daily data
                - weekly: Weekly data
                - monthly: Monthly data
        """
        pass
    
    @abstractmethod
    def get_ideal_number_dataframes(self) -> int:
        """
        Returns the number of dataframes required for the strategy.
        """
        pass
    
    def validate_sentiment_score(self, score: float) -> bool:
        """
        Validates that the sentiment score is within the valid range [-1, 1].
        
        Args:
            score (float): Sentiment score to validate
            
        Raises:
            False: If score is outside [-1, 1] range
        """
        if not -1 <= score <= 1:
            return False
        return True
    
    def validate_historical_data(self, data: pd.DataFrame) -> bool:
        """
        Validates that the historical data contains all required columns.
        
        Args:
            data (pd.DataFrame): Historical data to validate
            
        Raises:
            ValueError: If required columns are missing
        """
        required_columns = {df_datetime, df_open, df_high, df_low, df_close, df_volume}
        missing_columns = required_columns - set(data.columns)
        if missing_columns:
            return False
        return True

