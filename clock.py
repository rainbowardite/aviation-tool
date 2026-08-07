from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
from typing import cast, Any

def find_timezone_from_input(input):
    geolocator = Nominatim(user_agent="city_tz_linker")
    timezone_finder = TimezoneFinder()
    location = geolocator.geocode(input)

    if location:
        safe_location = cast(Any, location)
        timezone_name = timezone_finder.timezone_at(lng=safe_location.longitude, lat=safe_location.latitude)
        return timezone_name

    return None
