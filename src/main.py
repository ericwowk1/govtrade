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
   
   try:
      scraper.create_directory() #creates fresh directory folder
      print("Created new directory folder")
   except Exception as e:
      print("failed to create directory.. trying again")
      scraper.create_directory()
   hourly_filings = scraper.get_trader_filings(trader)
   if len(hourly_filings) > len(start_up_filings):
      for x in hourly_filings:
         if x in start_up_filings:
            continue
         else:
            scraper.download_pdfs(x)
            start_up_filings.append(x)  #adds the new filing stock to start_up_filings so next iteration is compared to updated list
            stock_dict = scraper.extract_pdf_data(x) #stock_dict contains "GME, S"
            for x in stock_dict:
               robinhood.trade_stock(x)
            
 
   
def main():
   #Startup logic
   global start_up_filings
   scraper.create_directory() #creates directory folder to hold pdfs
   robinhood.robinhood_login() #logs in to robinhood account
   trader = input("Who would you like to copy trade? Enter their LAST NAME ONLY ...")
   start_up_filings = scraper.get_trader_filings(trader) #gets list of past filings in 2024. program will ignore these and monitor for new ones
   print(f"startup filings {start_up_filings}")
   scraper.download_pdfs(start_up_filings)
   
      
   
   while True:

      if not (robinhood.market_open()):
         print(f"Market closed sleeping until open in {utils.sleepUntilOpen()} seconds")
         time.sleep(utils.sleepUntilOpen())
      else:
         print("market is open! running trading logic")
         hourly_check(trader)
         time.sleep(7200)

   
if __name__ == "__main__":
    main()
   