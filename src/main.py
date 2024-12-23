import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pdfplumber
import os
import shutil
import scraper
import robinhood
import time
import utils



trader_filings = []
#blacklist_stocks = [] #blacklisted stocks are stocks you have in your portfolio before the bot starts so it ignores them
my_holdings = []


   
def main():
   #Startup logic
   
   scraper.create_directory() #creates directory folder to hold pdfs
   robinhood.robinhood_login() #logs in to robihood account
   trader = input("Who would you like to copy trade? Enter their LAST NAME ONLY ...")
   trader_filings = scraper.get_trader_filings(trader) #returns list of unique filing id's
   scraper.download_pdfs(trader_filings)
   
   #Hourly loop
   while True:
      
      while not (utils.is_trading_hours()) or  (utils.is_weekend()): #checks if market is open, if not sleeps till 9:30am
         time.sleep(utils.sleepUntilOpen())
         
 
   
if __name__ == "__main__":
    main()
   