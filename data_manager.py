from pprint import pprint
from datetime import datetime, timedelta
import requests

SHEETY_PRICES_ENDPOINT = "https://api.sheety.co/ba96b93311a5671c7fe70fcac57906fa/flightDeals/prices"
SHEETY_USERS_ENDPOINT = "https://api.sheety.co/ba96b93311a5671c7fe70fcac57906fa/flightDeals/users"


class DataManager:

    def __init__(self):
        self.destination_data = {}
        self.city_codes = []

    def get_destination_data(self):

        response = requests.get(SHEETY_PRICES_ENDPOINT)
        data = response.json()['prices']
        self.destination_data = data
        return self.destination_data

    def update_destination_data(self, codes):
        city_id = 2
        while city_id <= len(codes) + 1:
            for code in codes:
                query = {
                    "price": {
                        'iataCode': code
                    }
                }
                response = requests.put(url=f"{SHEETY_PRICES_ENDPOINT}/{city_id}", json=query)
                city_id += 1

    def get_emails(self):
        response = requests.get(SHEETY_USERS_ENDPOINT)
        data = response.json()['users']
        return data





















