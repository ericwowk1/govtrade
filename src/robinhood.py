import robin_stocks
import os
import robin_stocks.robinhood as r
import pyotp

creds = {}

#This reads from txt file and splits into key value pairs
def robinhood_login():
    try:
        with open('src/credentials.txt', 'r') as f:
            for line in f: 
                clean_line = line.strip()
                key, value = clean_line.split('=')
                creds[key] = value
        
        #2factor login 
        totp = pyotp.TOTP(creds['my2factorapphere']).now()
        login = r.login(creds['username'], creds['password'], mfa_code=totp)
        return login
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

robinhood_login()
my_stocks = r.build_holdings()
for key,value in my_stocks.items():
    print(key,value)
