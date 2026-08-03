#!/usr/bin/env python3
import sys
import random
from files import initialize_airports, initialize_country, initialize_runway
from distance import get_distance, calculate_distance_from_timecode
from runway import get_longest_runway_id, get_runway_id
from airport import get_airport_id, get_airport_id_from_internal
from metar import get_awc_metar, print_metar

def get_airport_info(airports, countries, runways, code, distance=0, time="0"):
    airport = airports.get(code)
    if airport:
        country = countries.get(airport.country)
        runway_id = get_runway_id(runways, airport.id)
        runway = runways.get(runway_id)

        if country and runway:
            if distance == 0:
                print(f"{airport.ident}, {airport.name}, {airport.municipality}, {country.name}, {runway.length}ft")
            else:
                if time == "0":
                    print(f"{airport.ident}, {airport.name}, {airport.municipality}, {country.name}, {runway.length}ft, {int(distance)}nm")
                else:
                    print(f"{airport.ident}, {airport.name}, {airport.municipality}, {country.name}, {runway.length}ft, {int(distance)}nm, {time}")

            return [airport, country, runway_id, runway]
    return []

def get_airports_within_limits(departure_airport: list, airports: dict, runways: dict, min_distance: float, max_distance: float, min_runway_length: int):
    departure_airport_lat = departure_airport[0].lat
    departure_airport_long = departure_airport[0].long
    elegible_airport_ids = []
    distances = []
    for airport_id, airport in airports.items():
        distance = get_distance(float(departure_airport_lat), float(departure_airport_long), float(airport.lat), float(airport.long))
        if runways:
            arrival_airport_longest_runway_id = get_runway_id(runways, airport_id)
            arrival_airport_longest_runway = runways.get(arrival_airport_longest_runway_id)
            if arrival_airport_longest_runway:
                arrival_airport_longest_runway_length = arrival_airport_longest_runway.length
                if float(distance) <= max_distance and float(distance) >= min_distance and int(arrival_airport_longest_runway_length) >= min_runway_length and airport.shed_serv == "yes":
                    elegible_airport_ids.append(airport_id)
                    distances.append(distance)
    return elegible_airport_ids, distances

def random_airport(airports):
    random_number = random.randint(0, len(airports))
    airport_id = get_airport_id_from_internal(airports, random_number)
    airport = airports.get(airport_id)
    return airport.ident

def sort_by_distance(ids, distances):
    paired_data = zip(distances, ids)
    sorted_pairs = sorted(paired_data)
    sorted_distances = [d for d, i in sorted_pairs]
    sorted_ids = [i for d, i in sorted_pairs]
    return sorted_ids, sorted_distances

def distance_to_time(distance, speed):
    def check_single_digit(data):
        if -10 < data < 10:
            return f"0{data}"
        else:
            return data

    time_hours = distance / speed
    hours = int(time_hours)
    minutes = int((time_hours - hours) * 60)
    return check_single_digit(hours), check_single_digit(minutes)

def program_loop(airports, countries, runways, _departure_airport_ident="0"):
    def arrival_input():
        arrival_airport_code = input("\nEnter arrival airport code: ")
        if arrival_airport_code == "":
            random_number = random.randint(0, (len(potential_airport_list) - 1))
            airport_id = potential_airport_list[random_number]
            arrival_airport = get_airport_info(airports, countries, runways, airport_id)
        else:
            arrival_airport = get_airport_info(airports, countries, runways, get_airport_id(airports, arrival_airport_code))
        print_metar(arrival_airport)
        dep_arr_distance = get_distance(float(departure_airport[0].lat), float(departure_airport[0].long), float(arrival_airport[0].lat), float(arrival_airport[0].long))
        hours, minutes = distance_to_time(dep_arr_distance, speed)
        print(f"{int(dep_arr_distance)}nm, {hours}:{minutes}")
        return arrival_airport


    if _departure_airport_ident == "0":
        input_airport = input("Enter departure airport: ").upper()
        if input_airport == "":
            input_airport = random_airport(airports)
            print(input_airport)
    else:
        input_airport = _departure_airport_ident.upper()
    min_time = input("Enter minimum time (HH:MM): ")
    if min_time == "":
        min_time = "00:45"
        print(min_time)
    max_time = input("Enter max time (HH:MM): ")
    if max_time == "":
        max_time = "02:30"
        print(max_time)

    min_runway_length = 4460 # a319/a320: 4460, a321: 5600, b737-600: 4265, b737-700: 4650, 777: 6600
    speed = 420 # a319/320/321/b737: 420, 777: 450

    departure_airport = get_airport_info(airports, countries, runways, get_airport_id(airports, input_airport))
    if(departure_airport[0].icao != 0):
        print_metar(departure_airport)

    print(f"\nFinding Elegible Airports {min_time} to {max_time} away from {departure_airport[0].ident}")
    min_distance = calculate_distance_from_timecode(speed, min_time)
    max_distance = calculate_distance_from_timecode(speed, max_time)

    #elegible_airport_ids = ["1234"]
    #distances = ["10"]

    elegible_airport_ids, distances = get_airports_within_limits(departure_airport, airports, runways, min_distance, max_distance, min_runway_length)
    elegible_airport_ids, distances = sort_by_distance(elegible_airport_ids, distances)

    if len(elegible_airport_ids) > 0:
        print("Arrival Airport Options:")
        potential_airport_list = []
        for index, id in enumerate(elegible_airport_ids):
            distance = distances[index]
            hours, minutes = distance_to_time(distance, speed)
            potential_arrival_airport = get_airport_info(airports, countries, runways, id, distances[index], f"{hours}:{minutes}")
            potential_airport_list.append(potential_arrival_airport[0].id)

        arrival_airport = arrival_input()

        end_loop = True

        while end_loop:
            next_option = input("\nre-list | re-select | find-next | restart | quit: ")

            if next_option == "re-list":
                for index, id in enumerate(potential_airport_list):
                    distance = distances[index]
                    hours, minutes = distance_to_time(distance, speed)
                    potential_airport = get_airport_info(airports, countries, runways, id, distances[index], f"{hours}:{minutes}")

            if next_option == "re-list" or next_option == "re-select":
                re_listed_arrival_airport = arrival_input()

            if next_option == "find-next":
                program_loop(airports, countries, runways, arrival_airport[0].ident)
                end_loop = False


            if next_option == "restart":
                end_loop = False

            if next_option == "quit":
                end_loop = False
                sys.exit(0)
    else:
        print("No available airports for selection.")

def main() -> None:
    airports = initialize_airports()
    countries = initialize_country()
    runways = initialize_runway()

    while True:
        program_loop(airports, countries, runways)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Process interrupted by user.")
        sys.exit(130)
        #except Exception as e:
        #print(f"An unexpected error occurred: {e}")
        #sys.exit(1)
