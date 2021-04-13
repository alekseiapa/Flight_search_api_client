from datetime import datetime, timedelta
from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager
from pprint import pprint

ORIGIN_CITY_IATA = "PVG"

data_manager = DataManager()
flight_search = FlightSearch()

sheet_data = data_manager.get_destination_data()
emails_data = data_manager.get_emails()

DATA_FROM = (datetime.now() + timedelta(days=1)).strftime(f"%d/%m/%Y")
DATA_TO = (datetime.now() + timedelta(days=180)).strftime(f"%d/%m/%Y")


emails = [email['email'] for email in emails_data]
names = [name['firstName'] for name in emails_data]


if data_manager.destination_data[0]['iataCode'] == "":

    city_names = [city['city'] for city in sheet_data]
    data_manager.city_codes = flight_search.get_destination_code(city_names)
    data_manager.update_destination_data(data_manager.city_codes)
    sheet_data = data_manager.get_destination_data()


destinations = {
    data['iataCode']: {
        "city": data["city"],
        "id": data["id"],
        "price": data['lowestPrice']
    } for data in sheet_data
}

for destination_code in destinations:
    flight = flight_search.check_flights(ORIGIN_CITY_IATA, destination_code, DATA_FROM, DATA_TO)

    if flight is None:
        continue

    if flight.price < destinations[destination_code]["price"]:
        emails_data = data_manager.get_emails()
        emails = [email['email'] for email in emails_data]
        names = [name['firstName'] for name in emails_data]
        notification_manager = NotificationManager()
        for email in emails:
            link = f"https://www.google.co.uk/flights?hl=en#flt={flight.origin_airport}.{flight.destination_airport}.{flight.out_date}*{flight.destination_airport}.{flight.origin_airport}.{flight.return_date}"
            message = f"Low price alert! The flight from {flight.origin_city} to {flight.destination_city} is for CNY {flight.price}\nDeparture date: {flight.out_date} to {flight.return_date}"
            notification_manager.send_email(email, message, link)
