from runway import get_runway_id
from files import initialize_airports, initialize_country, initialize_runway

def distance_to_time(distance, speed):
    def check_single_digit(data):
        if -10 < data < 10:
            return f"0{data}"
        else:
            return data

    time_hours = distance / (speed - 140)
    hours = int(time_hours)
    minutes = int((time_hours - hours) * 60)
    return check_single_digit(hours), check_single_digit(minutes)

def get_airport_info(id):
    airports = initialize_airports()
    countries = initialize_country()
    runways = initialize_runway()

    airport = airports.get(id)
    if airport:
        country = countries.get(airport.country)
        runway_id = get_runway_id(runways, airport.id)
        runway = runways.get(runway_id)
        return [airport, country, runway_id, runway]
    return []
