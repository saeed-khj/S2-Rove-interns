#!/usr/bin/env python3
"""
Configuration file for Award Travel Value Calculator
Makes the application dynamic and configurable
"""

import os
from typing import Dict, List, Tuple

# API Configuration
RAPIDAPI_KEY = os.getenv('RAPIDAPI_KEY', "3e41e7a6f1mshaf764384a6102c4p10106ejsn36368940afd9")
RAPIDAPI_HOST = os.getenv('RAPIDAPI_HOST', "sky-scrapper.p.rapidapi.com")

# Aviation Stack API (replacing Amadeus)
AVIATIONSTACK_API_KEY = os.getenv('AVIATIONSTACK_API_KEY', "f4d6249bb1d14834a014f4e248884fe2")
AVIATIONSTACK_BASE_URL = os.getenv('AVIATIONSTACK_BASE_URL', "https://api.aviationstack.com/v1")

# Legacy Amadeus (keeping for reference but not using)
AMADEUS_API_KEY = os.getenv('AMADEUS_API_KEY', "ByR2wyksBFvFj7k8wOZGXCXTVwtFLtsi")
AMADEUS_API_SECRET = os.getenv('AMADEUS_API_SECRET', "koUlAQU0yyWFsAA7")
AMADEUS_BASE_URL = os.getenv('AMADEUS_BASE_URL', "https://api.amadeus.com")

# Application Configuration
CACHE_DURATION = int(os.getenv('CACHE_DURATION', 3600))  # 1 hour default
DEBUG_MODE = os.getenv('DEBUG_MODE', 'True').lower() == 'true'
PORT = int(os.getenv('PORT', 5001))

# Dynamic Airport Database
# This would typically come from a database or API
AIRPORTS_DATABASE = [
    # Major US Airports
    {'code': 'JFK', 'name': 'John F. Kennedy International Airport', 'city': 'New York', 'country': 'US'},
    {'code': 'LAX', 'name': 'Los Angeles International Airport', 'city': 'Los Angeles', 'country': 'US'},
    {'code': 'ORD', 'name': 'O\'Hare International Airport', 'city': 'Chicago', 'country': 'US'},
    {'code': 'DFW', 'name': 'Dallas/Fort Worth International Airport', 'city': 'Dallas', 'country': 'US'},
    {'code': 'ATL', 'name': 'Hartsfield-Jackson Atlanta International Airport', 'city': 'Atlanta', 'country': 'US'},
    {'code': 'DEN', 'name': 'Denver International Airport', 'city': 'Denver', 'country': 'US'},
    {'code': 'LAS', 'name': 'McCarran International Airport', 'city': 'Las Vegas', 'country': 'US'},
    {'code': 'MCO', 'name': 'Orlando International Airport', 'city': 'Orlando', 'country': 'US'},
    {'code': 'MIA', 'name': 'Miami International Airport', 'city': 'Miami', 'country': 'US'},
    {'code': 'SEA', 'name': 'Seattle-Tacoma International Airport', 'city': 'Seattle', 'country': 'US'},
    {'code': 'BOS', 'name': 'Boston Logan International Airport', 'city': 'Boston', 'country': 'US'},
    {'code': 'SFO', 'name': 'San Francisco International Airport', 'city': 'San Francisco', 'country': 'US'},
    {'code': 'IAH', 'name': 'George Bush Intercontinental Airport', 'city': 'Houston', 'country': 'US'},
    {'code': 'PHX', 'name': 'Phoenix Sky Harbor International Airport', 'city': 'Phoenix', 'country': 'US'},
    {'code': 'CLT', 'name': 'Charlotte Douglas International Airport', 'city': 'Charlotte', 'country': 'US'},
    
    # Major International Airports
    {'code': 'LHR', 'name': 'London Heathrow Airport', 'city': 'London', 'country': 'GB'},
    {'code': 'CDG', 'name': 'Charles de Gaulle Airport', 'city': 'Paris', 'country': 'FR'},
    {'code': 'NRT', 'name': 'Narita International Airport', 'city': 'Tokyo', 'country': 'JP'},
    {'code': 'SYD', 'name': 'Sydney Airport', 'city': 'Sydney', 'country': 'AU'},
    {'code': 'YYZ', 'name': 'Toronto Pearson International Airport', 'city': 'Toronto', 'country': 'CA'},
    {'code': 'FRA', 'name': 'Frankfurt Airport', 'city': 'Frankfurt', 'country': 'DE'},
    {'code': 'AMS', 'name': 'Amsterdam Airport Schiphol', 'city': 'Amsterdam', 'country': 'NL'},
    {'code': 'MAD', 'name': 'Adolfo Suárez Madrid–Barajas Airport', 'city': 'Madrid', 'country': 'ES'},
    {'code': 'BCN', 'name': 'Barcelona–El Prat Airport', 'city': 'Barcelona', 'country': 'ES'},
    {'code': 'FCO', 'name': 'Leonardo da Vinci International Airport', 'city': 'Rome', 'country': 'IT'},
    {'code': 'MXP', 'name': 'Milan Malpensa Airport', 'city': 'Milan', 'country': 'IT'},
    {'code': 'ZRH', 'name': 'Zurich Airport', 'city': 'Zurich', 'country': 'CH'},
    {'code': 'VIE', 'name': 'Vienna International Airport', 'city': 'Vienna', 'country': 'AT'},
    {'code': 'CPH', 'name': 'Copenhagen Airport', 'city': 'Copenhagen', 'country': 'DK'},
    {'code': 'ARN', 'name': 'Stockholm Arlanda Airport', 'city': 'Stockholm', 'country': 'SE'},
    {'code': 'OSL', 'name': 'Oslo Airport', 'city': 'Oslo', 'country': 'NO'},
    {'code': 'HEL', 'name': 'Helsinki Airport', 'city': 'Helsinki', 'country': 'FI'},
    {'code': 'DUB', 'name': 'Dublin Airport', 'city': 'Dublin', 'country': 'IE'},
    {'code': 'LGW', 'name': 'London Gatwick Airport', 'city': 'London', 'country': 'GB'},
    {'code': 'MAN', 'name': 'Manchester Airport', 'city': 'Manchester', 'country': 'GB'},
    {'code': 'EDI', 'name': 'Edinburgh Airport', 'city': 'Edinburgh', 'country': 'GB'},
    {'code': 'BRU', 'name': 'Brussels Airport', 'city': 'Brussels', 'country': 'BE'},
    {'code': 'LUX', 'name': 'Luxembourg Airport', 'city': 'Luxembourg', 'country': 'LU'},
    {'code': 'WAW', 'name': 'Warsaw Chopin Airport', 'city': 'Warsaw', 'country': 'PL'},
    {'code': 'PRG', 'name': 'Václav Havel Airport Prague', 'city': 'Prague', 'country': 'CZ'},
    {'code': 'BUD', 'name': 'Budapest Ferenc Liszt International Airport', 'city': 'Budapest', 'country': 'HU'},
    {'code': 'ATH', 'name': 'Athens International Airport', 'city': 'Athens', 'country': 'GR'},
    {'code': 'IST', 'name': 'Istanbul Airport', 'city': 'Istanbul', 'country': 'TR'},
    {'code': 'DXB', 'name': 'Dubai International Airport', 'city': 'Dubai', 'country': 'AE'},
    {'code': 'DOH', 'name': 'Hamad International Airport', 'city': 'Doha', 'country': 'QA'},
    {'code': 'BKK', 'name': 'Suvarnabhumi Airport', 'city': 'Bangkok', 'country': 'TH'},
    {'code': 'SIN', 'name': 'Singapore Changi Airport', 'city': 'Singapore', 'country': 'SG'},
    {'code': 'KUL', 'name': 'Kuala Lumpur International Airport', 'city': 'Kuala Lumpur', 'country': 'MY'},
    {'code': 'HKG', 'name': 'Hong Kong International Airport', 'city': 'Hong Kong', 'country': 'HK'},
    {'code': 'ICN', 'name': 'Incheon International Airport', 'city': 'Seoul', 'country': 'KR'},
    {'code': 'PEK', 'name': 'Beijing Capital International Airport', 'city': 'Beijing', 'country': 'CN'},
    {'code': 'PVG', 'name': 'Shanghai Pudong International Airport', 'city': 'Shanghai', 'country': 'CN'},
    {'code': 'DEL', 'name': 'Indira Gandhi International Airport', 'city': 'Delhi', 'country': 'IN'},
    {'code': 'BOM', 'name': 'Chhatrapati Shivaji Maharaj International Airport', 'city': 'Mumbai', 'country': 'IN'},
    {'code': 'MEX', 'name': 'Mexico City International Airport', 'city': 'Mexico City', 'country': 'MX'},
    {'code': 'GRU', 'name': 'São Paulo/Guarulhos International Airport', 'city': 'São Paulo', 'country': 'BR'},
    {'code': 'EZE', 'name': 'Ministro Pistarini International Airport', 'city': 'Buenos Aires', 'country': 'AR'},
    {'code': 'SCL', 'name': 'Arturo Merino Benítez International Airport', 'city': 'Santiago', 'country': 'CL'},
    {'code': 'LIM', 'name': 'Jorge Chávez International Airport', 'city': 'Lima', 'country': 'PE'},
    {'code': 'BOG', 'name': 'El Dorado International Airport', 'city': 'Bogotá', 'country': 'CO'},
    {'code': 'JNB', 'name': 'O. R. Tambo International Airport', 'city': 'Johannesburg', 'country': 'ZA'},
    {'code': 'CPT', 'name': 'Cape Town International Airport', 'city': 'Cape Town', 'country': 'ZA'},
    {'code': 'CAI', 'name': 'Cairo International Airport', 'city': 'Cairo', 'country': 'EG'},
    {'code': 'NBO', 'name': 'Jomo Kenyatta International Airport', 'city': 'Nairobi', 'country': 'KE'},
    {'code': 'LOS', 'name': 'Murtala Muhammed International Airport', 'city': 'Lagos', 'country': 'NG'},
]

# Dynamic Airline Programs Database
# This would typically come from a database or API
AIRLINE_PROGRAMS = [
    # US Airlines
    {"airline": "American Airlines", "program": "American AAdvantage", "code": "AA", "alliance": "Oneworld"},
    {"airline": "United Airlines", "program": "United MileagePlus", "code": "UA", "alliance": "Star Alliance"},
    {"airline": "Delta Air Lines", "program": "Delta SkyMiles", "code": "DL", "alliance": "SkyTeam"},
    {"airline": "Southwest Airlines", "program": "Southwest Rapid Rewards", "code": "WN", "alliance": "None"},
    {"airline": "JetBlue Airways", "program": "TrueBlue", "code": "B6", "alliance": "None"},
    {"airline": "Alaska Airlines", "program": "Alaska Mileage Plan", "code": "AS", "alliance": "Oneworld"},
    {"airline": "Spirit Airlines", "program": "Free Spirit", "code": "NK", "alliance": "None"},
    {"airline": "Frontier Airlines", "program": "Frontier Miles", "code": "F9", "alliance": "None"},
    
    # International Airlines
    {"airline": "British Airways", "program": "British Airways Avios", "code": "BA", "alliance": "Oneworld"},
    {"airline": "Air Canada", "program": "Air Canada Aeroplan", "code": "AC", "alliance": "Star Alliance"},
    {"airline": "Lufthansa", "program": "Miles & More", "code": "LH", "alliance": "Star Alliance"},
    {"airline": "Air France", "program": "Flying Blue", "code": "AF", "alliance": "SkyTeam"},
    {"airline": "KLM", "program": "Flying Blue", "code": "KL", "alliance": "SkyTeam"},
    {"airline": "Emirates", "program": "Emirates Skywards", "code": "EK", "alliance": "None"},
    {"airline": "Qatar Airways", "program": "Qatar Airways Privilege Club", "code": "QR", "alliance": "Oneworld"},
    {"airline": "Turkish Airlines", "program": "Miles&Smiles", "code": "TK", "alliance": "Star Alliance"},
    {"airline": "Singapore Airlines", "program": "KrisFlyer", "code": "SQ", "alliance": "Star Alliance"},
    {"airline": "Cathay Pacific", "program": "Cathay", "code": "CX", "alliance": "Oneworld"},
    {"airline": "Qantas", "program": "Qantas Frequent Flyer", "code": "QF", "alliance": "Oneworld"},
    {"airline": "Japan Airlines", "program": "JAL Mileage Bank", "code": "JL", "alliance": "Oneworld"},
    {"airline": "ANA", "program": "ANA Mileage Club", "code": "NH", "alliance": "Star Alliance"},
    {"airline": "Korean Air", "program": "SKYPASS", "code": "KE", "alliance": "SkyTeam"},
    {"airline": "China Southern", "program": "Sky Pearl Club", "code": "CZ", "alliance": "SkyTeam"},
    {"airline": "Air China", "program": "PhoenixMiles", "code": "CA", "alliance": "Star Alliance"},
    {"airline": "Ethiopian Airlines", "program": "ShebaMiles", "code": "ET", "alliance": "Star Alliance"},
    {"airline": "EgyptAir", "program": "EgyptAir Plus", "code": "MS", "alliance": "Star Alliance"},
    {"airline": "Royal Air Maroc", "program": "Safar Flyer", "code": "AT", "alliance": "Oneworld"},
    {"airline": "LATAM", "program": "LATAM Pass", "code": "LA", "alliance": "None"},
    {"airline": "Avianca", "program": "LifeMiles", "code": "AV", "alliance": "Star Alliance"},
    {"airline": "Copa Airlines", "program": "ConnectMiles", "code": "CM", "alliance": "Star Alliance"},
    {"airline": "Aeromexico", "program": "Club Premier", "code": "AM", "alliance": "SkyTeam"},
    {"airline": "Interjet", "program": "Club Interjet", "code": "4O", "alliance": "None"},
    {"airline": "Volaris", "program": "VClub", "code": "Y4", "alliance": "None"},
    {"airline": "VivaAerobus", "program": "Viva Rewards", "code": "VB", "alliance": "None"},
]

# Dynamic Base Values (configurable)
BASE_MILES = {
    'economy': int(os.getenv('BASE_MILES_ECONOMY', 25000)),
    'business': int(os.getenv('BASE_MILES_BUSINESS', 50000)),
    'first': int(os.getenv('BASE_MILES_FIRST', 75000))
}

BASE_TAXES = {
    'economy': float(os.getenv('BASE_TAXES_ECONOMY', 50)),
    'business': float(os.getenv('BASE_TAXES_BUSINESS', 100)),
    'first': float(os.getenv('BASE_TAXES_FIRST', 150))
}

# Dynamic Distance Factors
DISTANCE_FACTORS = {
    'domestic': float(os.getenv('DISTANCE_FACTOR_DOMESTIC', 1.0)),
    'international': float(os.getenv('DISTANCE_FACTOR_INTERNATIONAL', 1.5)),
    'default': float(os.getenv('DISTANCE_FACTOR_DEFAULT', 1.2))
}

# Dynamic Tax Factors
TAX_FACTORS = {
    'domestic': float(os.getenv('TAX_FACTOR_DOMESTIC', 1.0)),
    'international': float(os.getenv('TAX_FACTOR_INTERNATIONAL', 1.5)),
    'default': float(os.getenv('TAX_FACTOR_DEFAULT', 1.0))
}

def get_airports() -> List[Dict]:
    """Get all airports from the database"""
    return AIRPORTS_DATABASE

def get_airports_by_country(country_code: str) -> List[Dict]:
    """Get airports filtered by country code"""
    return [airport for airport in AIRPORTS_DATABASE if airport['country'] == country_code]

def get_airport_by_code(code: str) -> Dict:
    """Get airport by IATA code"""
    for airport in AIRPORTS_DATABASE:
        if airport['code'] == code.upper():
            return airport
    return None

def get_airline_programs() -> List[Dict]:
    """Get all airline programs"""
    return AIRLINE_PROGRAMS

def get_airline_programs_by_alliance(alliance: str) -> List[Dict]:
    """Get airline programs filtered by alliance"""
    return [program for program in AIRLINE_PROGRAMS if program['alliance'] == alliance]

def get_airline_program_by_code(code: str) -> Dict:
    """Get airline program by airline code"""
    for program in AIRLINE_PROGRAMS:
        if program['code'] == code.upper():
            return program
    return None

def is_domestic_route(origin: str, destination: str) -> bool:
    """Check if route is domestic (same country)"""
    origin_airport = get_airport_by_code(origin)
    dest_airport = get_airport_by_code(destination)
    
    if origin_airport and dest_airport:
        return origin_airport['country'] == dest_airport['country']
    return False

def is_international_route(origin: str, destination: str) -> bool:
    """Check if route is international (different countries)"""
    return not is_domestic_route(origin, destination)

def get_route_type(origin: str, destination: str) -> str:
    """Get route type (domestic/international)"""
    if is_domestic_route(origin, destination):
        return 'domestic'
    return 'international' 