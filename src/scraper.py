import requests
from bs4 import BeautifulSoup
import json
import time

def scrape_loan_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            print(f"Failed to fetch {url}: Status {response.status_code}")
            return None
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Target the main content area (common for BoM site structure)
        # We look for the article or main container
        main_content = soup.find('div', {'id': 'content'}) or soup.find('main') or soup.body
        
        data = {
            "source_url": url,
            "title": soup.title.string.strip() if soup.title else "No Title",
            "content": []
        }

        # Extracting meaningful text blocks (Headers and Paragraphs)
        for element in main_content.find_all(['h1', 'h2', 'h3', 'p', 'li']):
            text = element.get_text(strip=True)
            if text and len(text) > 20:  
                data["content"].append(text)
        
        return data

    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None

# Target URLs from Bank of Maharashtra
urls = [
    # --- Retail Loans ---
    "https://bankofmaharashtra.bank.in/personal-banking/loans/home-loan",
    "https://bankofmaharashtra.bank.in/personal-banking/loans/personal-loan",
    "https://bankofmaharashtra.bank.in/personal-banking/loans/car-loan",
    "https://bankofmaharashtra.bank.in/maha-super-flexi-housing-loan-scheme",
    "https://bankofmaharashtra.bank.in/maha-adhaar-loan", # Pensioner Loan
    
    # --- MSME & Business Loans ---
    "https://bankofmaharashtra.bank.in/msme-large-credit",
    "https://bankofmaharashtra.bank.in/maha-msme-project-loan-scheme",
    
    # --- Education Loans ---
    "https://bankofmaharashtra.bank.in/model-education-loan-scheme",
    
    # --- Agriculture Loans ---
    "https://bankofmaharashtra.bank.in/agricultures",
    "https://bankofmaharashtra.bank.in/kisan-credit-card",
    "https://bankofmaharashtra.bank.in/kisan-all-purpose-term-loan"
]

def run_scraper():
    all_data = []
    for url in urls:
        print(f"Scraping: {url}...")
        page_data = scrape_loan_page(url)
        if page_data:
            all_data.append(page_data)
        time.sleep(1) # Be polite to the server
    
    with open('data/raw_data.json', 'w', encoding='utf-8') as f:
        json.dump(all_data, f, indent=4)
    print("Scraping complete! Data saved to data/raw_data.json")

if __name__ == "__main__":
    run_scraper()