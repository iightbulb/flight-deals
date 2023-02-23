from data_manager import DataManager
from notification_manager import NotificationManager
from flight_search import FlightSearch
from datetime import datetime, timedelta


data_manager = DataManager()
sheet_data = data_manager.get_destination_data()
flight_search = FlightSearch()
notification_manager = NotificationManager()

ORIGINAL_CITY_IATA = "LON"

if sheet_data[0]["iataCode"] == '':
    for row in sheet_data:
        row["iataCode"] = flight_search.get_destination_code(row["city"])
    data_manager.destination_data = sheet_data
    data_manager.update_destination_codes()

tomorrow = datetime.now() + timedelta(days=1)
six_months_time = datetime.now() + timedelta(days=(6*30))

for destination in sheet_data:
    flight = flight_search.search_for_flight(
        ORIGINAL_CITY_IATA,
        destination["iataCode"],
        from_time=tomorrow,
        to_time=six_months_time,
    )

    if flight.price < destination["lowestPrice"]:

        users = data_manager.get_customer_emails()
        names = [row["firstName"] for row in users]
        emails = [row["email"] for row in users]

        the_message = f"Good Flight Deal! Only {flight.price} to fly from " \
                  f"{flight.departure_city}-{flight.departure_code} to " \
                  f"{flight.arrival_city}-{flight.arrival_code} from " \
                  f"{flight.outbound_date} to {flight.return_date}. \n" \
                  f"https://www.google.co.uk/flights?hl=en#flt={flight.departure_code}.{flight.arrival_code}" \
                  f".{flight.outbound_date}*{flight.arrival_code}.{flight.departure_code}" \
                  f".{flight.return_date} "

        if flight.stopovers > 0:
            the_message += f"\nThere will be {flight.stopovers} stopover in {flight.via_city}"

        #notification_manager.send_sms(the_message)
        notification_manager.send_email(the_message, emails, names)
