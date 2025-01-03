import requests
from bs4 import BeautifulSoup
from datetime import datetime
import os
import shutil
import scraper
import robinhood
import time
import utils
import queue

trader_filings = []
my_holdings = []
myqueue = queue.Queue()
start_up_trades = {}
hourly_trades = {}
start_up_filings = []

def hourly_check(trader, start_up_filings): 
    print("Running hourly_check() function...")
    try:
        scraper.create_directory()  # creates fresh directory folder
        print("Created new directory folder.")
    except Exception as e:
        print(f"Failed to create directory. Error: {e}")
        scraper.create_directory()

    hourly_filings = scraper.get_trader_filings(trader)
    print(f"Hourly filings: {hourly_filings}")
    if len(hourly_filings) > len(start_up_filings):
        for x in hourly_filings:
            if x in start_up_filings:
                continue
            else:
                scraper.download_pdfs(x)
                start_up_filings.append(x)
                stock_dict = scraper.extract_pdf_data(x)  # stock_dict contains "GME, S"
                print(f"Stock dict extracted: {stock_dict}")
                for x in stock_dict:
                    robinhood.trade_stock(x)

def main():
    # Startup logic
    global start_up_filings
    scraper.create_directory()  # creates directory folder to hold pdfs
    robinhood.robinhood_login()  # logs in to robinhood account
    trader = input("Who would you like to copy trade? Enter their LAST NAME ONLY ...")
    start_up_filings = scraper.get_trader_filings(trader)  # gets list of past filings in 2024. program will ignore these and monitor for new ones

    scraper.download_pdfs(start_up_filings)

    while True:
       
      if (robinhood.market_open()):
            print("Market is open! Running trading logic.")
            hourly_check(trader, start_up_filings)
            print("Trading logic completed. Sleeping for 2 hours.")
            time.sleep(7200)
   
      else:
         sleep_duration = utils.sleepUntilOpen()
         print(f"Market closed. Sleeping until open in {sleep_duration} seconds.")
         time.sleep(sleep_duration)

if __name__ == "__main__":
    main()
