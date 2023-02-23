import requests
from flight_data import FlightData
from pprint import pprint
from dotenv import load_dotenv
import os

flight_api_endpoint = "https://api.tequila.kiwi.com/v2/search"


def configure():
    load_dotenv()


configure()


class FlightSearch:
    #This class is responsible for talking to the Flight Search API.
    def get_destination_code(self, city_name):
        tequila_api = "https://api.tequila.kiwi.com/locations/query"
        headers = {
            "apikey": os.getenv('flight_API_KEY')
        }
        tequila_params = {
            "term": city_name,
            "location_types": "city"
        }
        response = requests.get(url=tequila_api, params=tequila_params, headers=headers)
        code = response.json()["locations"][0]["code"]
        return code

    def search_for_flight(self, departure_city_code, arrival_city_code, from_time, to_time):
        headers = {
            "apikey": os.getenv('flight_API_KEY')
        }

        flight_params = {
            "fly_from": departure_city_code,
            "fly_to": arrival_city_code,
            "date_from": from_time.strftime("%d/%m/%Y"),
            "date_to": to_time.strftime("%d/%m/%Y"),
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            "one_for_city": 1,
            "max_stopovers": 0,
            "flight_type": "round",
            "curr": "GBP",
        }

        response = requests.get(url=flight_api_endpoint, params=flight_params, headers=headers)
        try:
            result = response.json()["data"][0]
        except IndexError:
            print(f"No direct flights found for {departure_city_code}.")
            flight_params["max_stopovers"] = 2
            response = requests.get(url=flight_api_endpoint, params=flight_params, headers=headers)
            result = response.json()["data"][0]
            flight_data = FlightData(
                price=result["price"],
                departure_city=result["route"][0]["cityFrom"],
                departure_code=result["route"][0]["flyFrom"],
                arrival_city=result["route"][1]["cityTo"],
                arrival_code=result["route"][1]["flyTo"],
                outbound_date=result["route"][0]["local_departure"].split("T")[0],
                return_date=result["route"][2]["local_departure"].split("T")[0],
                stopovers=2,
                via_city=result["route"][0]["cityTo"]
            )
            pprint(f"{flight_data.arrival_city}: GBP:{flight_data.price}. There will be 1 stopover"
                   f"in {result['route'][0]['cityTo']}")
            return flight_data
        else:
            flight_data = FlightData(
                price=result["price"],
                departure_city=result["route"][0]["cityFrom"],
                departure_code=result["route"][0]["flyFrom"],
                arrival_city=result["route"][0]["cityTo"],
                arrival_code=result["route"][0]["flyTo"],
                outbound_date=result["route"][0]["local_departure"].split("T")[0],
                return_date=result["route"][1]["local_departure"].split("T")[0]
            )

            print(f"{flight_data.arrival_city}: £:{flight_data.price}")
            return flight_data
