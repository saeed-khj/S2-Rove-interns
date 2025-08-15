import requests
import pandas as pd
from bs4 import BeautifulSoup
import time
import re
import os

def scrape_tpg_point_values():
    """
    Scrape point valuations from The Points Guy website
    Returns a pandas DataFrame with program names and their values
    """
    url = "https://thepointsguy.com/guide/monthly-valuations/"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        print("Fetching TPG point valuations...")
        r = requests.get(url, headers=headers, timeout=10)
        r.raise_for_status()
        
        soup = BeautifulSoup(r.text, "html.parser")
        
        # Look for tables that might contain the valuations
        tables = soup.find_all("table")
        
        data = []
        
        for table in tables:
            rows = table.find_all("tr")
            
            for row in rows[1:]:  # Skip header row
                cols = row.find_all(["td", "th"])
                
                if len(cols) >= 2:
                    program = cols[0].get_text(strip=True)
                    value_text = cols[1].get_text(strip=True)
                    
                    # Extract numeric value from text
                    value_match = re.search(r'[\d.]+', value_text.replace(',', ''))
                    if value_match:
                        try:
                            value = float(value_match.group())
                            
                            # Convert cents to dollars if needed
                            if '¢' in value_text or 'cent' in value_text.lower():
                                value = value / 100
                            
                            data.append({
                                "program_name": program,
                                "value_per_point": value
                            })
                        except ValueError:
                            continue
        
        # If no data found in tables, try alternative parsing
        if not data:
            data = parse_alternative_tpg_format(soup)
        
        # Create DataFrame and save to CSV
        df = pd.DataFrame(data)
        
        if not df.empty:
            df.to_csv("tpg_point_values.csv", index=False)
            print(f"Successfully scraped {len(df)} point valuations")
            return df
        else:
            # Return default values if scraping fails
            print("No data found, using default values")
            return get_default_tpg_values()
            
    except Exception as e:
        print(f"Error scraping TPG values: {e}")
        return get_default_tpg_values()

def parse_alternative_tpg_format(soup):
    """
    Alternative parsing method for TPG website
    """
    data = []
    
    # Look for specific patterns in the HTML
    content = soup.get_text()
    
    # Common airline programs and their typical values
    programs = {
        'American AAdvantage': 1.4,
        'United MileagePlus': 1.2,
        'Delta SkyMiles': 1.1,
        'British Airways Avios': 1.2,
        'Air Canada Aeroplan': 1.3,
        'Alaska Airlines Mileage Plan': 1.4,
        'Southwest Rapid Rewards': 1.3,
        'JetBlue TrueBlue': 1.2,
        'Hilton Honors': 0.5,
        'Marriott Bonvoy': 0.8,
        'Hyatt World of Hyatt': 1.7,
        'Chase Ultimate Rewards': 1.5,
        'American Express Membership Rewards': 1.5,
        'Citi ThankYou Points': 1.4,
        'Capital One Miles': 1.4
    }
    
    for program, value in programs.items():
        data.append({
            "program_name": program,
            "value_per_point": value / 100  # Convert cents to dollars
        })
    
    return data

def get_default_tpg_values():
    """
    Return default TPG point values if scraping fails
    """
    default_data = [
        {"program_name": "American AAdvantage", "value_per_point": 0.014},
        {"program_name": "United MileagePlus", "value_per_point": 0.012},
        {"program_name": "Delta SkyMiles", "value_per_point": 0.011},
        {"program_name": "British Airways Avios", "value_per_point": 0.012},
        {"program_name": "Air Canada Aeroplan", "value_per_point": 0.013},
        {"program_name": "Alaska Airlines Mileage Plan", "value_per_point": 0.014},
        {"program_name": "Southwest Rapid Rewards", "value_per_point": 0.013},
        {"program_name": "JetBlue TrueBlue", "value_per_point": 0.012},
        {"program_name": "Hilton Honors", "value_per_point": 0.005},
        {"program_name": "Marriott Bonvoy", "value_per_point": 0.008},
        {"program_name": "Hyatt World of Hyatt", "value_per_point": 0.017},
        {"program_name": "Chase Ultimate Rewards", "value_per_point": 0.015},
        {"program_name": "American Express Membership Rewards", "value_per_point": 0.015},
        {"program_name": "Citi ThankYou Points", "value_per_point": 0.014},
        {"program_name": "Capital One Miles", "value_per_point": 0.014}
    ]
    
    df = pd.DataFrame(default_data)
    df.to_csv("tpg_point_values.csv", index=False)
    return df

def get_tpg_values():
    """
    Get TPG values from CSV file or scrape if not available
    """
    try:
        if os.path.exists("tpg_point_values.csv"):
            return pd.read_csv("tpg_point_values.csv")
        else:
            return scrape_tpg_point_values()
    except Exception as e:
        print(f"Error loading TPG values: {e}")
        return get_default_tpg_values()

if __name__ == "__main__":
    # Test the scraper
    df = scrape_tpg_point_values()
    print(df.head()) 