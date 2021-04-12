import requests
from pprint import pprint
from flight_data import FlightData

TEQUILA_ENDPOINT = "https://tequila-api.kiwi.com"
TEQUILA_API_KEY = "TEQUILA_API_KEY"


class FlightSearch:
    def __init__(self):
        self.city_codes = []

    def get_destination_code(self, city_names):
        for city in city_names:
            headers = {
                "apikey": TEQUILA_API_KEY
            }

            query = {
                "term": city,
                "location_types": "city"
            }

            response = requests.get(url=f"{TEQUILA_ENDPOINT}/locations/query", headers=headers, params=query)
            data = response.json()
            code = data['locations'][0]['code']
            self.city_codes.append(code)
        return self.city_codes


    def check_flights(self, origin_city, dest_city, date_from, date_to):

        headers = {
            "apikey": TEQUILA_API_KEY
        }
        query = {
            "fly_from": origin_city,
            "fly_to": dest_city,
            "date_from": date_from,
            "date_to": date_to,
            "flight_type": "round",
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            "one_for_city": 1,
            "curr": "CNY",
            "max_stopovers": 0,
        }
        response = requests.get(url=f"{TEQUILA_ENDPOINT}/v2/search", headers=headers, params=query)
        try:
            data = response.json()['data'][0]
        except IndexError:
            print(f"Sorry! No data found for the flight from {origin_city} to {dest_city}")
            return None
        else:
            price = data['price']
            origin_city = data['cityFrom']
            origin_airport = data['cityCodeFrom']
            destination_city = data['cityTo']
            destination_airport = data['cityCodeTo']
            out_date = data['route'][0]['utc_departure']
            return_date = data['route'][1]["utc_arrival"]

            flight_data = FlightData(price, origin_city, origin_airport, destination_city, destination_airport, out_date, return_date)
            print(f"From: {flight_data.origin_city}\nTo:{flight_data.destination_city}\nPrice: CNY {flight_data.price}\n")
            return flight_data



