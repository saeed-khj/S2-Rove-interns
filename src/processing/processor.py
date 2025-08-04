class DataProcessor:
    def process_flight_data(self, raw_data):
        processed_data = []
        for entry in raw_data:
            processed_entry = {
                'flight_number': entry.get('flight_number'),
                'departure': entry.get('departure'),
                'arrival': entry.get('arrival'),
                'price': entry.get('price'),
                'airline': entry.get('airline'),
                'date': entry.get('date')
            }
            processed_data.append(processed_entry)
        return processed_data

    def filter_routes(self, processed_data, criteria):
        filtered = []
        for entry in processed_data:
            # Extract price as a float from nested dict
            price = float(entry.get("price", {}).get("total", float("inf")))
            price_ok = price <= criteria.get("max_price", float("inf"))
            airline_ok = entry.get("validatingAirlineCodes", [None])[0] in criteria.get("airlines", [])
            stops_ok = entry.get("itineraries", [{}])[0].get("segments", [{}])
            stops = len(stops_ok) - 1 if stops_ok else float("inf")
            stops_ok = stops <= criteria.get("max_stops", float("inf"))
            if price_ok and airline_ok and stops_ok:
                filtered.append(entry)
        return filtered