import requests
import json
import time
from bs4 import BeautifulSoup
from config import (
    get_airline_programs, get_airline_program_by_code, 
    is_domestic_route, is_international_route, get_route_type,
    BASE_MILES, BASE_TAXES, DISTANCE_FACTORS, TAX_FACTORS
)

def get_award_data(origin, destination, cabin):
    """
    Get award flight data from AwardHacker
    Returns a list of award flight options
    """
    try:
        # Try to use real data integration first
        from real_data_integration import real_data
        
        # Get real award data with date parameter (current date if not specified)
        from datetime import datetime
        current_date = datetime.now().strftime('%Y-%m-%d')
        
        award_data = real_data.get_real_award_data(origin, destination, cabin, current_date)
        
        if award_data:
            print(f"✅ Using real award data for {origin}-{destination} in {cabin} class")
            return award_data
        
        # Fallback to enhanced mock data
        print(f"⚠️  Falling back to enhanced mock data for {origin}-{destination} in {cabin} class")
        return generate_mock_award_data(origin, destination, cabin)
        
    except Exception as e:
        print(f"Error fetching award data: {e}")
        return generate_mock_award_data(origin, destination, cabin)

def generate_mock_award_data(origin, destination, cabin):
    """
    Generate realistic mock award data for demonstration
    """
    cabin_mapping = {
        'economy': 'economy',
        'business': 'business',
        'first': 'first'
    }
    
    cabin_class = cabin_mapping.get(cabin, 'economy')
    
    # Get all airline programs dynamically
    all_programs = get_airline_programs()
    
    # Filter programs based on route type (domestic vs international)
    route_type = get_route_type(origin, destination)
    
    # For demonstration, we'll use a subset of programs
    # In a real implementation, you'd filter based on actual availability
    selected_programs = all_programs[:8]  # Use first 8 programs for demo
    
    programs = []
    for program in selected_programs:
        programs.append({
            "airline": program["airline"],
            "program": program["program"],
            "miles": get_miles_for_route(origin, destination, cabin_class, program["code"]),
            "taxes": get_taxes_for_route(origin, destination, cabin_class, program["code"]),
            "availability": get_availability_for_route(origin, destination, program["code"]),
            "transfer_partners": get_transfer_partners(program["code"]),
            "alliance": program["alliance"]
        })
    
    return programs

def get_miles_for_route(origin, destination, cabin_class, airline_code):
    """
    Calculate realistic miles required for a route
    """
    # Get base miles from configuration
    base_miles = BASE_MILES.get(cabin_class, BASE_MILES['economy'])
    
    # Airline-specific multipliers (could be moved to config)
    airline_multipliers = {
        "AA": 1.0, "UA": 1.1, "DL": 1.2, "BA": 0.9, "AC": 1.0,
        "WN": 0.8, "B6": 0.9, "AS": 1.0, "NK": 0.7, "F9": 0.7,
        "LH": 1.1, "AF": 1.0, "KL": 1.0, "EK": 1.3, "QR": 1.2,
        "TK": 1.0, "SQ": 1.2, "CX": 1.1, "QF": 1.1, "JL": 1.0,
        "NH": 1.1, "KE": 1.0, "CZ": 0.9, "CA": 0.9, "ET": 0.8,
        "MS": 0.8, "AT": 0.8, "LA": 1.0, "AV": 1.0, "CM": 1.0,
        "AM": 1.0, "4O": 0.7, "Y4": 0.7, "VB": 0.7
    }
    
    # Get route type and distance factor
    route_type = get_route_type(origin, destination)
    distance_factor = DISTANCE_FACTORS.get(route_type, DISTANCE_FACTORS['default'])
    
    # Get airline multiplier
    airline_multiplier = airline_multipliers.get(airline_code, 1.0)
    
    miles = base_miles * airline_multiplier * distance_factor
    
    # Round to nearest 1000
    return int(round(miles, -3))

def get_taxes_for_route(origin, destination, cabin_class, airline_code):
    """
    Calculate realistic taxes and fees for a route
    """
    # Get base taxes from configuration
    base_taxes = BASE_TAXES.get(cabin_class, BASE_TAXES['economy'])
    
    # Airline-specific tax factors (could be moved to config)
    airline_tax_factors = {
        "AA": 1.0, "UA": 1.1, "DL": 1.0, "BA": 1.5, "AC": 1.2,
        "WN": 0.8, "B6": 0.9, "AS": 1.0, "NK": 0.7, "F9": 0.7,
        "LH": 1.2, "AF": 1.1, "KL": 1.1, "EK": 1.4, "QR": 1.3,
        "TK": 1.1, "SQ": 1.2, "CX": 1.1, "QF": 1.1, "JL": 1.0,
        "NH": 1.1, "KE": 1.0, "CZ": 0.9, "CA": 0.9, "ET": 0.8,
        "MS": 0.8, "AT": 0.8, "LA": 1.0, "AV": 1.0, "CM": 1.0,
        "AM": 1.0, "4O": 0.7, "Y4": 0.7, "VB": 0.7
    }
    
    # Get route type and tax factor
    route_type = get_route_type(origin, destination)
    route_factor = TAX_FACTORS.get(route_type, TAX_FACTORS['default'])
    
    # Get airline tax factor
    airline_tax_factor = airline_tax_factors.get(airline_code, 1.0)
    
    taxes = base_taxes * airline_tax_factor * route_factor
    
    return round(taxes, 2)

def get_availability_for_route(origin, destination, airline_code):
    """
    Get availability status for a route and airline
    """
    # This would typically check real availability
    # For demo purposes, return random availability
    import random
    availability_options = ["Good", "Limited", "Excellent", "Poor"]
    return random.choice(availability_options)

def get_transfer_partners(airline_code):
    """
    Get transfer partners for an airline
    """
    # This would typically come from a database
    transfer_partners = {
        "AA": ["Chase", "Amex", "Citi"],
        "UA": ["Chase", "Amex"],
        "DL": ["Amex"],
        "BA": ["Chase", "Amex"],
        "AC": ["Chase", "Amex"],
        "WN": ["Chase"],
        "B6": ["Amex"],
        "AS": ["Chase", "Amex"],
        "NK": ["Amex"],
        "F9": ["Amex"],
        "LH": ["Amex"],
        "AF": ["Amex"],
        "KL": ["Amex"],
        "EK": ["Amex"],
        "QR": ["Amex"],
        "TK": ["Amex"],
        "SQ": ["Amex"],
        "CX": ["Amex"],
        "QF": ["Amex"],
        "JL": ["Amex"],
        "NH": ["Amex"],
        "KE": ["Amex"],
        "CZ": ["Amex"],
        "CA": ["Amex"],
        "ET": ["Amex"],
        "MS": ["Amex"],
        "AT": ["Amex"],
        "LA": ["Amex"],
        "AV": ["Amex"],
        "CM": ["Amex"],
        "AM": ["Amex"],
        "4O": ["Amex"],
        "Y4": ["Amex"],
        "VB": ["Amex"]
    }
    return transfer_partners.get(airline_code, ["Amex"])

def scrape_award_hacker_website(origin, destination, cabin):
    """
    Alternative method to scrape AwardHacker website directly
    Note: This is a placeholder for actual implementation
    """
    url = "https://www.awardhacker.com/award-charts/"
    
    params = {
        "f": origin,
        "t": destination,
        "o": str(cabin_mapping.get(cabin, 0)),
        "c": "y",
        "s": "1",
        "p": "1",
        "n": "10",
        "v": "2"
    }
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Parse the response (this would need to be implemented based on actual website structure)
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Extract award data from the parsed HTML
        # This is a placeholder - actual implementation would depend on website structure
        
        return []
        
    except Exception as e:
        print(f"Error scraping AwardHacker: {e}")
        return []

if __name__ == "__main__":
    # Test the award data function
    test_data = get_award_data("JFK", "LAX", "business")
    print(json.dumps(test_data, indent=2)) 