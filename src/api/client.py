import requests

class ApiClient:
    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = "https://test.api.amadeus.com"
        self.access_token = None

    def authenticate(self):
        url = f"{self.base_url}/v1/security/oauth2/token"
        data = {
            "grant_type": "client_credentials",
            "client_id": self.api_key,
            "client_secret": self.api_secret
        }
        response = requests.post(url, data=data)
        if response.status_code == 200:
            self.access_token = response.json()["access_token"]
        else:
            print("Failed to authenticate:", response.text)
            self.access_token = None

    def connect(self):
        self.authenticate()
        if self.access_token:
            print("Connected to Amadeus API")
        else:
            print("Failed to connect to Amadeus API")

    def get_flight_data(self, origin, destination, departure_date):
        if not self.access_token:
            print("No access token. Please authenticate first.")
            return None
        url = f"{self.base_url}/v2/shopping/flight-offers"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        params = {
            "originLocationCode": origin,
            "destinationLocationCode": destination,
            "departureDate": departure_date,
            "adults": 1
        }
        response = requests.get(url, headers=headers, params=params)
        print("HTTP status:", response.status_code)
        print("API raw response:", response.text)
        if response.status_code == 200:
            return response.json().get("data")
        else:
            return None