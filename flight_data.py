

class FlightData:
    def __init__(self, price, departure_city, departure_code, arrival_city,
                 arrival_code, outbound_date, return_date, stopovers=0, via_city=""):
        self.price = price
        self.departure_city = departure_city
        self.departure_code = departure_code
        self.arrival_city = arrival_city
        self.arrival_code = arrival_code
        self.outbound_date = outbound_date
        self.return_date = return_date
        self.stopovers = stopovers
        self.via_city = via_city
