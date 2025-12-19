# Compatibility Layer for Ultra-Lightweight PythonAnywhere Deployment
# Place this file in quotex_predictor/predictor/compatibility_layer.py

"""
This module provides lightweight replacements for heavy packages
to make the SMC system work within PythonAnywhere's 450MB limit
"""

import math
import random
from datetime import datetime, timedelta
from typing import Dict, Any, List, Union

# Mock pandas DataFrame
class MockDataFrame:
    def __init__(self, data=None):
        if data is None:
            data = {}
        self.data = data
        self._index = 0
    
    def __getitem__(self, key):
        if key in self.data:
            return MockSeries(self.data[key])
        return MockSeries([])
    
    def __setitem__(self, key, value):
        self.data[key] = value if isinstance(value, list) else [value]
    
    def __len__(self):
        if not self.data:
            return 0
        return len(list(self.data.values())[0])
    
    @property
    def empty(self):
        return len(self) == 0
    
    @property
    def iloc(self):
        return MockIloc(self)
    
    def tail(self, n=5):
        new_data = {}
        for key, values in self.data.items():
            new_data[key] = values[-n:] if len(values) >= n else values
        return MockDataFrame(new_data)
    
    def head(self, n=5):
        new_data = {}
        for key, values in self.data.items():
            new_data[key] = values[:n] if len(values) >= n else values
        return MockDataFrame(new_data)

class MockSeries:
    def __init__(self, data):
        self.data = data if isinstance(data, list) else [data]
    
    def __getitem__(self, index):
        if isinstance(index, slice):
            return MockSeries(self.data[index])
        return self.data[index] if index < len(self.data) else 0
    
    def __len__(self):
        return len(self.data)
    
    @property
    def iloc(self):
        return MockSeriesIloc(self)
    
    def rolling(self, window, center=False):
        return MockRolling(self.data, window)
    
    def mean(self):
        return sum(self.data) / len(self.data) if self.data else 0
    
    def max(self):
        return max(self.data) if self.data else 0
    
    def min(self):
        return min(self.data) if self.data else 0
    
    def dropna(self):
        return MockSeries([x for x in self.data if x is not None])
    
    def tolist(self):
        return self.data

class MockIloc:
    def __init__(self, df):
        self.df = df
    
    def __getitem__(self, index):
        if isinstance(index, slice):
            # Return subset of DataFrame
            start, stop = index.start or 0, index.stop or len(self.df)
            new_data = {}
            for key, values in self.df.data.items():
                new_data[key] = values[start:stop]
            return MockDataFrame(new_data)
        else:
            # Return single row as dict-like object
            row_data = {}
            for key, values in self.df.data.items():
                row_data[key] = values[index] if index < len(values) else 0
            return MockRow(row_data)

class MockSeriesIloc:
    def __init__(self, series):
        self.series = series
    
    def __getitem__(self, index):
        return self.series.data[index] if index < len(self.series.data) else 0

class MockRow:
    def __init__(self, data):
        self.data = data
    
    def __getitem__(self, key):
        return self.data.get(key, 0)

class MockRolling:
    def __init__(self, data, window):
        self.data = data
        self.window = window
    
    def max(self):
        result = []
        for i in range(len(self.data)):
            start = max(0, i - self.window + 1)
            window_data = self.data[start:i+1]
            result.append(max(window_data) if window_data else 0)
        return MockSeries(result)
    
    def min(self):
        result = []
        for i in range(len(self.data)):
            start = max(0, i - self.window + 1)
            window_data = self.data[start:i+1]
            result.append(min(window_data) if window_data else 0)
        return MockSeries(result)
    
    def mean(self):
        result = []
        for i in range(len(self.data)):
            start = max(0, i - self.window + 1)
            window_data = self.data[start:i+1]
            result.append(sum(window_data) / len(window_data) if window_data else 0)
        return MockSeries(result)

# Mock numpy functions
class MockNumpy:
    @staticmethod
    def array(data):
        return data if isinstance(data, list) else [data]
    
    @staticmethod
    def var(data):
        if not data:
            return 0
        mean_val = sum(data) / len(data)
        return sum((x - mean_val) ** 2 for x in data) / len(data)
    
    @staticmethod
    def mean(data):
        return sum(data) / len(data) if data else 0
    
    @staticmethod
    def max(data):
        return max(data) if data else 0
    
    @staticmethod
    def min(data):
        return min(data) if data else 0
    
    @staticmethod
    def arctan(x):
        return math.atan(x)
    
    @staticmethod
    def pi():
        return math.pi
    
    @staticmethod
    def isnan(x):
        return x != x  # NaN check
    
    @staticmethod
    def isinf(x):
        return x == float('inf') or x == float('-inf')

# Mock pandas module
class MockPandas:
    DataFrame = MockDataFrame
    Series = MockSeries
    
    @staticmethod
    def isna(x):
        return x is None or (isinstance(x, float) and math.isnan(x))

# Generate mock price data
def generate_mock_price_data(symbol: str, timeframe: str = '1h', limit: int = 200) -> MockDataFrame:
    """Generate realistic mock price data for SMC analysis"""
    
    # Base price for different symbols
    base_prices = {
        'EURUSD': 1.1000,
        'GBPUSD': 1.2500,
        'USDJPY': 110.00,
        'AUDUSD': 0.7500,
        'USDCAD': 1.2500,
        'NZDUSD': 0.7000,
        'USDCHF': 0.9200,
    }
    
    base_price = base_prices.get(symbol.upper(), 1.0000)
    
    # Generate realistic OHLCV data
    data = {
        'open': [],
        'high': [],
        'low': [],
        'close': [],
        'volume': []
    }
    
    current_price = base_price
    
    for i in range(limit):
        # Random price movement
        change_percent = random.uniform(-0.02, 0.02)  # ±2% change
        price_change = current_price * change_percent
        
        open_price = current_price
        close_price = current_price + price_change
        
        # High and low based on volatility
        volatility = abs(price_change) * random.uniform(1.2, 2.0)
        high_price = max(open_price, close_price) + volatility
        low_price = min(open_price, close_price) - volatility
        
        data['open'].append(round(open_price, 5))
        data['high'].append(round(high_price, 5))
        data['low'].append(round(low_price, 5))
        data['close'].append(round(close_price, 5))
        data['volume'].append(random.randint(1000, 10000))
        
        current_price = close_price
    
    return MockDataFrame(data)

# Export compatibility objects
np = MockNumpy()
pd = MockPandas()

def create_mock_dataframe(data):
    return MockDataFrame(data)