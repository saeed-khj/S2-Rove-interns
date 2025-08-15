import requests
import json
import time
from datetime import datetime, timedelta

from config import RAPIDAPI_KEY, RAPIDAPI_HOST

def get_cash_price(origin, destination, date, return_date=None):
    """
    Get cash flight prices from Sky Scrapper API
    Returns flight options with prices
    """
    try:
        # Try to use real data integration first
        from real_data_integration import real_data
        
        cash_data = real_data.get_real_cash_prices(origin, destination, date, return_date)
        
        if cash_data:
            print(f"✅ Using real cash price data for {origin}-{destination} on {date}")
            return cash_data
        
        # Fallback to enhanced mock data
        print(f"⚠️  Falling back to enhanced mock cash price data for {origin}-{destination} on {date}")
        return generate_mock_cash_price_data(origin, destination, date, return_date)
        
    except Exception as e:
        print(f"Error fetching cash prices: {e}")
        return generate_mock_cash_price_data(origin, destination, date, return_date)

def get_real_cash_price(origin, destination, date, return_date=None):
    """
    Get real cash prices from Sky Scrapper API
    """
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": RAPIDAPI_HOST
    }
    
    # Search for flights
    search_url = "https://sky-scanner3.p.rapidapi.com/flights/search"
    
    params = {
        "origin": origin,
        "destination": destination,
        "date": date,
        "currency": "USD",
        "adults": "1"
    }
    
    if return_date:
        params["returnDate"] = return_date
    
    try:
        response = requests.get(search_url, headers=headers, params=params, timeout=15)
        response.raise_for_status()
        
        data = response.json()
        
        # Parse the response and extract flight options
        flights = parse_flight_response(data)
        
        return flights
        
    except requests.exceptions.RequestException as e:
        print(f"API request failed: {e}")
        return []
    except json.JSONDecodeError as e:
        print(f"Failed to parse API response: {e}")
        return []

def parse_flight_response(data):
    """
    Parse the Sky Scrapper API response
    """
    flights = []
    
    try:
        # Extract flight data from the response
        # The actual structure depends on the API response format
        
        if 'data' in data and 'itineraries' in data['data']:
            for itinerary in data['data']['itineraries']:
                flight = {
                    'airline': itinerary.get('legs', [{}])[0].get('carriers', {}).get('marketing', [{}])[0].get('name', 'Unknown'),
                    'departure_time': itinerary.get('legs', [{}])[0].get('departure', ''),
                    'arrival_time': itinerary.get('legs', [{}])[0].get('arrival', ''),
                    'duration': itinerary.get('legs', [{}])[0].get('duration', ''),
                    'price': itinerary.get('pricingOptions', [{}])[0].get('price', {}).get('amount', 0),
                    'currency': itinerary.get('pricingOptions', [{}])[0].get('price', {}).get('currency', 'USD'),
                    'cabin_class': 'Economy',  # Default, could be extracted from response
                    'stops': len(itinerary.get('legs', [])) - 1
                }
                flights.append(flight)
        
        return flights
        
    except Exception as e:
        print(f"Error parsing flight response: {e}")
        return []

def generate_mock_cash_price_data(origin, destination, date, return_date=None):
    """
    Generate realistic mock cash price data for demonstration
    """
    # Base prices for different routes
    base_prices = get_base_price_for_route(origin, destination)
    
    flights = []
    
    # Generate multiple flight options
    airlines = [
        "American Airlines",
        "United Airlines", 
        "Delta Air Lines",
        "Southwest Airlines",
        "JetBlue Airways"
    ]
    
    for i, airline in enumerate(airlines):
        # Add some variation to prices
        price_variation = 1.0 + (i * 0.1) + (0.1 * (i % 2))  # 10-20% variation
        base_price = base_prices['economy'] * price_variation
        
        # Generate departure times throughout the day
        departure_hour = 6 + (i * 3) % 18  # Spread flights throughout the day
        
        flight = {
            'airline': airline,
            'departure_time': f"{date}T{departure_hour:02d}:00:00",
            'arrival_time': f"{date}T{(departure_hour + get_flight_duration(origin, destination)) % 24:02d}:00:00",
            'duration': f"{get_flight_duration(origin, destination)}h",
            'price': round(base_price, 2),
            'currency': 'USD',
            'cabin_class': 'Economy',
            'stops': 0 if i < 3 else 1,  # First 3 flights are direct
            'flight_number': f"{get_airline_code(airline)}{1000 + i}",
            'aircraft': 'Boeing 737' if i < 3 else 'Airbus A320'
        }
        
        flights.append(flight)
        
        # Add business class option for some airlines
        if i < 3:
            business_flight = flight.copy()
            business_flight['cabin_class'] = 'Business'
            business_flight['price'] = round(base_price * 3.5, 2)  # Business class is ~3.5x economy
            business_flight['flight_number'] = f"{get_airline_code(airline)}{2000 + i}"
            flights.append(business_flight)
    
    # Sort by price
    flights.sort(key=lambda x: x['price'])
    
    return flights

def get_base_price_for_route(origin, destination):
    """
    Get base prices for different cabin classes on a route
    """
    # Domestic routes
    domestic_routes = [
        ("JFK", "LAX"), ("ORD", "LAX"), ("DFW", "LAX"),
        ("ATL", "LAX"), ("JFK", "ORD"), ("DFW", "ORD")
    ]
    
    # International routes
    international_routes = [
        ("JFK", "LHR"), ("JFK", "CDG"), ("JFK", "NRT"),
        ("LAX", "LHR"), ("LAX", "NRT"), ("ORD", "LHR")
    ]
    
    route = (origin, destination)
    reverse_route = (destination, origin)
    
    if route in domestic_routes or reverse_route in domestic_routes:
        return {
            'economy': 350,
            'business': 1200,
            'first': 2000
        }
    elif route in international_routes or reverse_route in international_routes:
        return {
            'economy': 800,
            'business': 2500,
            'first': 4000
        }
    else:
        # Default prices
        return {
            'economy': 500,
            'business': 1500,
            'first': 2500
        }

def get_flight_duration(origin, destination):
    """
    Get estimated flight duration in hours
    """
    # Domestic routes
    domestic_routes = [
        ("JFK", "LAX"), ("ORD", "LAX"), ("DFW", "LAX"),
        ("ATL", "LAX"), ("JFK", "ORD"), ("DFW", "ORD")
    ]
    
    # International routes
    international_routes = [
        ("JFK", "LHR"), ("JFK", "CDG"), ("JFK", "NRT"),
        ("LAX", "LHR"), ("LAX", "NRT"), ("ORD", "LHR")
    ]
    
    route = (origin, destination)
    reverse_route = (destination, origin)
    
    if route in domestic_routes or reverse_route in domestic_routes:
        return 5  # 5 hours for domestic
    elif route in international_routes or reverse_route in international_routes:
        return 8  # 8 hours for international
    else:
        return 6  # Default duration

def get_airline_code(airline_name):
    """
    Get airline code from airline name
    """
    airline_codes = {
        "American Airlines": "AA",
        "United Airlines": "UA", 
        "Delta Air Lines": "DL",
        "Southwest Airlines": "WN",
        "JetBlue Airways": "B6"
    }
    
    return airline_codes.get(airline_name, "XX")

def search_flights_with_filters(origin, destination, date, cabin_class=None, max_price=None, direct_only=False):
    """
    Search flights with additional filters
    """
    flights = get_cash_price(origin, destination, date)
    
    # Apply filters
    if cabin_class:
        flights = [f for f in flights if f['cabin_class'].lower() == cabin_class.lower()]
    
    if max_price:
        flights = [f for f in flights if f['price'] <= max_price]
    
    if direct_only:
        flights = [f for f in flights if f['stops'] == 0]
    
    return flights

if __name__ == "__main__":
    # Test the cash price function
    test_flights = get_cash_price("JFK", "LAX", "2024-01-15")
    print(json.dumps(test_flights, indent=2)) 