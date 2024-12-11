from dagster import asset, job, op, graph, Output
import subprocess
import os

# Define an asset that runs the Scrapy spider and processes the data
@asset
def run_scrapy_spider():
    """
    This asset runs the Scrapy spider and handles data fetching and saving.
    """
    spider_path = 'scrapy_project/spider/spider'
    command = f"cd {spider_path} && scrapy crawl stock_price -a stock_symbols="AAPL,MSFT,GOOGL,TSLA,AMZN""
    
    try:
        # Run the Scrapy command
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print("Scrapy spider ran successfully")
        return Output(result.stdout, "scrapy_output")
    except subprocess.CalledProcessError as e:
        print(f"Error running Scrapy spider: {e.stderr}")
        raise


