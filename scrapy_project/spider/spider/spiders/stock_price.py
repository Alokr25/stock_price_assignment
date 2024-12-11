import scrapy
import pandas as pd
from datetime import datetime
import os

class StockSpider(scrapy.Spider):
    name = 'stock_price'
    allowed_domains = ['alphavantage.co']
    start_urls = ['https://www.alphavantage.co/query']  # Required by Scrapy but not directly used.

    API_KEY = os.getenv('ALPHA_VANTAGE_API_KEY', 'ABNBIVQXYDYTSHBO')  # Use environment variable if available
    BASE_URL = 'https://www.alphavantage.co/query'

    def __init__(self, stock_symbols=None, *args, **kwargs):
        super(StockSpider, self).__init__(*args, **kwargs)
        # Parse the command-line argument or default to a single stock symbol
        if stock_symbols:
            print(stock_symbols)
            self.stock_symbols = stock_symbols.split(',')
        else:
            self.stock_symbols = ['AAPL']  # Default if no argument is provided

    def start_requests(self):
        for symbol in self.stock_symbols:
            params = {
                'function': 'TIME_SERIES_INTRADAY',
                'symbol': symbol,
                'interval': '5min',
                'apikey': self.API_KEY
            }
            url = f"{self.BASE_URL}?function={params['function']}&symbol={params['symbol']}&interval={params['interval']}&apikey={params['apikey']}"
            yield scrapy.Request(url, callback=self.parse, cb_kwargs={'symbol': symbol})

    def parse(self, response, symbol):
        data = response.json()
        
        if 'Time Series (1min)' not in data:
            self.log(f"Error fetching data for {symbol}.")
            return

        time_series = data['Time Series (1min)']
        records = []

        for timestamp, metrics in time_series.items():
            records.append({
                'timestamp': timestamp,
                'open_price': float(metrics['1. open']),
                'high': float(metrics['2. high']),
                'low': float(metrics['3. low']),
                'stock_price': float(metrics['4. close']),
                'trading_volume': int(metrics['5. volume']),
            })

        stock_df = pd.DataFrame(records)

        # Save data as CSV
        stock_csv_path = f'{symbol}_stock_data.csv'
        stock_df.to_csv(stock_csv_path, index=False)
        self.log(f"Data saved to {stock_csv_path}")

