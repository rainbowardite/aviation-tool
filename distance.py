import math

def get_distance(lat1, lon1, lat2, lon2):
    EARTH_RADIUS_NM = 3440.065

    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = (math.sin(dlat / 2) ** 2 +
         math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2)
    c = 2 * math.asin(math.sqrt(a))

    return EARTH_RADIUS_NM * c


def timecode_to_hours(timecode_str):
    parts = timecode_str.split(":")

    if len(parts) != 2:
        raise ValueError("Timecode must be in 'HH:MM' format")

    hours = int(parts[0])
    minutes = int(parts[1])

    # Convert minutes to hours and add to total
    total_hours = hours + (minutes / 60)
    return total_hours


def calculate_distance_from_timecode(speed_knots, timecode_str):
    hours = timecode_to_hours(timecode_str)

    return speed_knots * hours
