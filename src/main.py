# main.py

from api.client import ApiClient
from processing.processor import DataProcessor
from storage.database import Database
import datetime

def main():
    # Initialize API client with credentials
    api_key = "ByR2wyksBFvFj7k8wOZGXCXTVwtFLtsi"
    api_secret = "koUlAQU0yyWFsAA7"
    api_client = ApiClient(api_key, api_secret)
    api_client.authenticate()
    
    # Connect to the API
    api_client.connect()
    
    routes = [
        {"origin": "JFK", "destination": "LHR"},
        {"origin": "SFO", "destination": "CDG"},
        {"origin": "ORD", "destination": "HND"}
    ]
    start_date = datetime.date(2025, 8, 1)
    end_date = datetime.date(2025, 8, 31)
    
    # Store the processed data in the database
    db_url = "sqlite:///travel_data.db"  # Example for SQLite, adjust as needed
    database = Database(db_url)
    database.connect()

    for route in routes:
        for n in range((end_date - start_date).days + 1):
            date = start_date + datetime.timedelta(days=n)
            flight_data = api_client.get_flight_data(route["origin"], route["destination"], str(date))
            if not flight_data:
                continue
            data_processor = DataProcessor()
            processed_data = data_processor.process_flight_data(flight_data)
            # Save only relevant details
            for entry in processed_data:
                record = {
                    "origin": route["origin"],
                    "destination": route["destination"],
                    "date": str(date),
                    "price": float(entry.get("price", {}).get("total", 0)),
                    "airline": entry.get("validatingAirlineCodes", [""])[0],
                    "departure_time": entry.get("itineraries", [{}])[0].get("segments", [{}])[0].get("departure", {}).get("at", "")
                }
                database.save_data([record])

if __name__ == "__main__":
    main()