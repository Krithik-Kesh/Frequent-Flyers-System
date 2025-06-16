"""Applications for creating customers, flight segments, airports and trips"""
import csv
import datetime
from typing import Dict, List, Tuple

from airport import Airport
from customer import Customer
from flight import Trip, FlightSegment
from visualizer import Visualizer

# AIRPORT_LOCATIONS: global mapping of an airport's IATA with their respective
#                    longitude and latitude positions.
# NOTE: This is used for our testing purposes, so it has to be populated in
# create_airports(), but you are welcome to use it as you see fit.
AIRPORT_LOCATIONS = {}

# DEFAULT_BASE_COST: Default rate per km for the base cost of a flight segment.
DEFAULT_BASE_COST = 0.1225


def import_data(file_airports: str, file_customers: str, file_segments: str,
                file_trips: str) -> Tuple[
        List[List[str]], List[List[str]], List[List[str]], List[List[str]]]:
    """ Opens all the data files <data/filename.csv> which stores the CSV data,
        and returns a tuple of lists of lists of strings. This contains the 
        read in data, line-by-line, (airports, customers, flights, trips).

        Precondition: the dataset file must be in CSV format.
    """

    airport_log, customer_log, flight_log, trip_log = [], [], [], []

    airport_data = csv.reader(open(file_airports))
    customer_data = csv.reader(open(file_customers))
    flight_data = csv.reader(open(file_segments))
    trip_data = csv.reader(open(file_trips))

    for row in airport_data:
        airport_log.append(row)

    for row in flight_data:
        flight_log.append(row)

    for row in customer_data:
        customer_log.append(row)

    for row in trip_data:
        trip_log.append(row)

    return airport_log, flight_log, customer_log, trip_log


def create_customers(log: List[List[str]]) -> Dict[int, Customer]:
    """ Returns a dictionary of Customer IDs and their Customer instances, 
    based on the customers from the input dataset from the <log>.

    Precondition:
        - The <log> list contains the input data in the correct format.
    """
    customers_dic = {}
    for i in log:
        customer = Customer(int(i[0]), i[1], int(i[2]), i[3])
        customers_dic[customer.get_id()] = customer
    return customers_dic


def create_flight_segments(log: List[List[str]]) \
        -> Dict[datetime.date, List[FlightSegment]]:
    """ Returns a dictionary storing all FlightSegments, indexed by their
    departure date, based on the input dataset stored in the <log>.

    Precondition:
    - The <log> list contains the input data in the correct format.
    """
    d = {}
    for row in log:
        fid = row[0]
        dep_code = row[1]
        arr_code = row[2]
        date_parts = list(map(int, row[3].split(":")))
        dep_time_parts = list(map(int, row[4].split(":")))
        arr_time_parts = list(map(int, row[5].split(":")))
        year, month, day = date_parts
        dep_dt = datetime.datetime(year, month, day,
                                   dep_time_parts[0], dep_time_parts[1])
        arr_dt = datetime.datetime(year, month, day,
                                   arr_time_parts[0], arr_time_parts[1])
        dist = float(row[6])
        coords = ((0.0, 0.0), (0.0, 0.0))
        seg = FlightSegment(fid, dep_dt, arr_dt,
                            DEFAULT_BASE_COST, dist, dep_code, arr_code, coords)
        dep_date = dep_dt.date()
        if dep_date not in d:
            d[dep_date] = []
        d[dep_date].append(seg)
    return d


def create_airports(log: List[List[str]]) -> List[Airport]:
    """ Return a list of Airports with all applicable data, based
    on the input dataset stored in the <log>.

    Precondition:
    - The <log> list contains the input data in the correct format.
    """
    airs = []
    for i in log:
        iata = i[0]
        name = i[1]
        loc = (float(i[2]), float(i[3]))
        air = Airport(iata, name, loc)
        AIRPORT_LOCATIONS[iata] = air
        airs.append(air)
    return airs


def load_trips(log: List[List[str]], customer_dict: Dict[int, Customer],
               flight_segments: Dict[datetime.date, List[FlightSegment]]) \
        -> List[Trip]:
    """ Creates the Trip objects and makes the bookings.

    Preconditions:
    - The <log> list contains the input data in the correct format.
    - the customers are already correctly stored in the <customer_dict>,
    indexed by their customer ID.
    - the flight segments are already correctly stored in the 
    <flight_segments>, indexed by their departure date
    """
    d = []
    for j in log:
        res_id = j[0]
        cus_id = int(j[1])
        year, month, day = map(int, j[2].split("-"))
        trip_date = datetime.date(year, month, day)
        raw_segment_str = j[3]
        cleaned = raw_segment_str.strip("[]")
        entries = cleaned.split("),(")
        segments = []
        for i in entries:
            i = i.strip("()").replace("'", "").replace('"', '')
            parts = i.split(",")
            if len(parts) < 2:
                continue
            dep_air = parts[0].strip()
            seat_type = parts[1].strip()
            for seg in flight_segments.get(trip_date, []):
                if seg.get_dep() == dep_air:
                    segments.append((seg, seat_type))
                    break
        if segments:
            trip = customer_dict[cus_id].book_trip(res_id, segments, trip_date)
            d.append(trip)
    return d


if __name__ == '__main__':
    print("\n---------------------------------------------")
    print("Reading in all data! Processing...")
    print("---------------------------------------------\n")

    # input_data = import_data('data/airports.csv', 'data/customers.csv',
    #     'data/segments.csv', 'data/trips.csv')
    input_data = import_data('../data/airports.csv', 'data/customers.csv',
                             'data/segments_small.csv', 'data/trips_small.csv')

    airports = create_airports(input_data[0])
    print("Airports Created! Still Processing...")
    flights = create_flight_segments(input_data[1])
    print("Flight Segments Created! Still Processing...")
    customers = create_customers(input_data[2])
    print("Customers Created! Still Processing...")
    print("Loading trips can take a while...")
    trips = load_trips(input_data[3], customers, flights)
    print("Trips Created! Opening Visualizer...\n")

    flights_len = 0
    for ky in flights:
        flights_len += len(flights[ky])

    print("---------------------------------------------")
    print("Some Statistics:")
    print("---------------------------------------------")
    print("Total airports in the dataset:", len(airports))
    print("Total flight segments in the dataset:", flights_len)
    print("Total customers in the dataset:", len(customers))
    print("Total trips in the dataset:", len(trips))
    print("---------------------------------------------\n")

    all_flights = [seg for tp in trips for seg in tp.get_flight_segments()]
    all_customers = [customers[cid] for cid in customers]

    V = Visualizer()
    V.draw(all_flights)

    while not V.has_quit():

        flights = V.handle_window_events(all_customers, all_flights)

        all_flights = []

        for flt in flights:
            all_flights.append(flt)

        V.draw(all_flights)

    import python_ta

    python_ta.check_all(config={
        'allowed-import-modules': [
            'python_ta', 'typing', 'csv', 'datetime', 'doctest',
            'visualizer', 'customer', 'flight', 'airport'
        ],
        'max-nested-blocks': 6,
        'allowed-io': [
            'create_customers', 'create_airports', 'import_data',
            'create_flight_segments', 'load_trips'
        ],
        'generated-members': 'pygame.*'
    })
