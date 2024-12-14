import requests
import robinhood
from bs4 import BeautifulSoup
from datetime import datetime
import pdfplumber
import os
import shutil

#Global variables
current_holdings = [] #This stores pdf #'s for nancy trades. we check the pdf_links with this list hourly for new pdf #s
yearnum = datetime.now().year
year = str(yearnum)
directory = "pdfs" #creates a directory to store the pdfs
url = "https://disclosures-clerk.house.gov/FinancialDisclosure/ViewMemberSearchResult"


def create_directory():
   '''creates a directory folder to store the pdfs
   '''
   try:
    os.mkdir(directory)
    print("Directory created successfully")
   except FileExistsError:
    print("folder exists, deleting and creating new one")
    print("Deleting it will remove all files inside. Type 'yes' to confirm:")
    user_input = input("> ").strip().lower()
    if user_input == "yes":
        shutil.rmtree(directory)   
        os.mkdir(directory)
        print("Directory created successfully")
    else:
        print("Operation cancelled")
   except Exception as e:
      print(e)
      exit()

def start_fill_list(pdf_links):
    """
    Fills the `start_results` list with PDF numbers for gov person trades.
    """
    for link in pdf_links:
        href = link.get('href')
        filename = href.split("/")[-1]
        current_holdings.append(filename)
        
def download_pdf(response, filename):
    """
    Downloads a PDF and saves it to the specified directory.
    """
    file_path = os.path.join(directory, filename)
    with open(file_path, "wb") as f:
        f.write(response.content)
        
        
        
def main():
    # Step 1: Create directory for storing PDFs
    create_directory()

    # Step 2: Fetch disclosures data
    payload = {
        "LastName": "pelosi",
        "FilingYear": year
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    
    response = requests.post(url, data=payload, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    pdf_links = soup.find_all('a')  # Get list of all <a> tags for PDFs

    # Step 3: Fill start_results with filenames
    start_fill_list(pdf_links)

    # Step 4: Download all PDFs
    for link in pdf_links:
        href = link.get('href')
        filename = href.split("/")[-1]  # Get the unique number to save the PDF
        final_link = f"https://disclosures-clerk.house.gov/public_disc/ptr-pdfs/{year}/{filename}"  # Full PDF URL
        pdf_response = requests.get(final_link)
        download_pdf(pdf_response, filename)

'''def extract_pdf_data(pdf_path):
  with pdfplumber.open(pdf_path) as pdf:
     
   
      # COME BACK TO THIS TO GET THE PDF DATA FROM THE FOLDERS AND STORE IN LIST.
'''


if __name__ == "__main__":
    main()
   


    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
   
   



