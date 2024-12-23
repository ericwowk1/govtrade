import requests
import robinhood
from bs4 import BeautifulSoup
from datetime import datetime
import pdfplumber
import os
import shutil
import time
import main




yearnum = datetime.now().year
year = str(yearnum)
directory = "pdfs" #creates a directory to store the pdfs
url = "https://disclosures-clerk.house.gov/FinancialDisclosure/ViewMemberSearchResult"


def create_directory():
    try:
        # If directory exists, try to remove it
        if os.path.exists('pdfs'):
            try:
                shutil.rmtree('pdfs')
            except PermissionError:
                print("Warning: Could not remove existing 'pdfs' directory. It may be in use.")
                # Wait a bit and try again
                time.sleep(1)
                try:
                    shutil.rmtree('pdfs')
                except PermissionError:
                    print("Error: Still cannot access 'pdfs' directory. Please close any applications using it.")
                    return False
        
        # Create new directory
        os.makedirs('pdfs')
        return True
        
    except Exception as e:
        print(f"Error creating directory: {str(e)}")
        return False


     #finds a tags on website and download pdfs to folder
def get_trader_filings(trader):
    current_holdings = []
    payload = {
        "LastName": trader,
        "FilingYear": year,
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    
    response = requests.post(url, data=payload, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    pdf_links = soup.find_all('a')  # Get list of all <a> tags for PDFs
    for link in pdf_links:
        href = link.get('href')
        filename = href.split("/")[-1]
        current_holdings.append(filename.replace(".pdf", ""))
    return current_holdings
    #returns list with 348930890 348930891., etc.     

#parameter is a list of unique pdf numbers from the scraped website
def download_pdfs(current_holdings):
    """
    Retrieves PDF links from the website based on the current payload,
    and downloads the PDFs into the specified directory.
    """
    for link in current_holdings:
        filename = link 
        final_link = f"https://disclosures-clerk.house.gov/public_disc/ptr-pdfs/{year}/{filename}.pdf"  # Full PDF URL
        pdf_response = requests.get(final_link)
        
        file_path = os.path.join(directory, f"{filename}.pdf")
        with open(file_path, "wb") as f:
            f.write(pdf_response.content)
        

def extract_pdf_data(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            print(text)


#def blacklist_truefalse():
    val = ""
    tickers = []
    while val== "":
        val = input("do you want to blacklist stocks you currently own? This will blacklist the program from interacting with all currently owned stock tickers enter (y/n)")
        if val == "y":
            tickers = input("enter tickers you want to blacklist spaced by commas. EX: GME,TSLA,NVDA").strip().split(",")
            return tickers 
        
        elif val == "n":
            return tickers
        else:
            print("invalid input, type y/n case sensitive")
            val = ""
            
            
        
        
    


    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
   
   



