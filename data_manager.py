import requests


SHEETY_ENDPOINT = "https://api.sheety.co/a011f77a1602e7d844a100b6f668e8d2/myFlightDeals/prices"
USERS_SHEETY_ENDPOINT = "https://api.sheety.co/a011f77a1602e7d844a100b6f668e8d2/myFlightDeals/users"

class DataManager:
    #This class is responsible for talking to the Google Sheet.
    def __init__(self):
        self.destination_data = {}
        self.customer_data = {}

    def get_destination_data(self):
        response = requests.get(url=SHEETY_ENDPOINT)
        data = response.json()
        self.destination_data = data["prices"]
        return self.destination_data

    def update_destination_codes(self):
        for city in self.destination_data:
            new_data = {
                "price": {
                    "iataCode": city["iataCode"]
                }
            }
            response = requests.put(url=f"{SHEETY_ENDPOINT}/{city['id']}", json=new_data)

    def get_customer_emails(self):
        response = requests.get(url=USERS_SHEETY_ENDPOINT)
        result = response.json()
        self.customer_data = result["users"]
        return self.customer_data






