import robin_stocks
import os
import robin_stocks.robinhood as r
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
     
        
def get_buying_power():
    with open('src/credentials.txt', 'r') as f:
        for line in f:
            clean_line = line.strip()
            key, value = clean_line.split('=')
            creds[key] = value
        accountnum = creds['accountnumber']
        buying_power = robin_stocks.robinhood.profiles.load_account_profile(account_number=accountnum, info='buying_power', dataType='indexzero')
        return buying_power





