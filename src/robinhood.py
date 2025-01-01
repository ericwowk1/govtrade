import robin_stocks
import os
import robin_stocks.robinhood as r
from datetime import datetime,timezone
import pyotp



creds = {}

def robinhood_login():
    '''
    This reads from txt file and splits into key value pairs
    '''
    global accountnum
    with open('src/credentials.txt', 'r') as f:
        for line in f:
            clean_line = line.strip()
            key, value = clean_line.split('=')
            creds[key] = value
        #2factor login 
        totp = pyotp.TOTP(creds['my2factorapphere']).now()
        login = r.login(creds['username'], creds['password'], mfa_code=totp)
        accountnum = creds['accountnumber']
        
def get_current_holdings():
    '''
    This function gets your current stock holdings to ignore
    so the bot doesnt sell your investments / also compares to gov portfolio
    '''
    my_stocks = r.build_holdings()
    for key,value in my_stocks.items():
        print(key,value)
        
def robinhood_logout():
    r.logout()
  
def get_account_number():
    with open('src/credentials.txt', 'r') as f:
        for line in f:
            clean_line = line.strip()
            key, value = clean_line.split('=')
            creds[key] = value
        accountnum = creds['accountnumber']   
        
def get_buying_power():
    accnum = get_account_number()
    buying_power = robin_stocks.robinhood.profiles.load_account_profile(account_number=accountnum, info='buying_power', dataType='indexzero')
    return buying_power

def owns_stock(ticker):
    positions = r.account.get_all_positions()
    for position in positions:
        instrument_url = position.get("instrument")
        # Fetch the instrument details to get the ticker symbol
        instrument_data = r.helper.request_get(instrument_url)
        if instrument_data.get("symbol") == ticker:
            return True
    return False

def get_stock_quantity(ticker):
    positions = r.account.get_all_positions()
    for position in positions:
        instrument_url = position.get("instrument")
        # Fetch the instrument details to get the ticker symbol
        instrument_data = r.helper.request_get(instrument_url)
        if instrument_data.get("symbol") == ticker:
            return float(position.get("quantity", 0))
    return 0

def market_open():
    market_hours = r.get_market_today_hours('XNYS')  # Retrieve market hours once

    if not market_hours or not market_hours.get("is_open", False):
        return False 
    else:
        open_time = datetime.fromisoformat(market_hours["opens_at"].replace("Z", "+00:00"))
        close_time = datetime.fromisoformat(market_hours["closes_at"].replace("Z", "+00:00"))
        current_time = datetime.now(timezone.utc)
        return open_time <= current_time <= close_time
 
def trade_stock(stock):
    robinhood_login()
    accountnum = get_account_number()
    for ticker, action in stock.items():
        if action == "P":  # Check if the action is a purchase
            purchase_amount = get_buying_power() * 0.10  # Spend 10% of buying power
            r.orders.order_buy_fractional_by_price(
                ticker,
                purchase_amount,
                timeInForce='gfd',
                extendedHours=False,
                jsonify=True,
                market_hours='regular_hours'
            )
            robinhood_logout()
        if action == "S" and owns_stock(ticker):
            robinhood_login()
            quantity = get_stock_quantity(ticker)
            if quantity == 0:
                 return
            else:
                 r.orders.order_sell_fractional_by_quantity(ticker, quantity)
            robinhood_logout()

         
         
    
    
    
        
        
