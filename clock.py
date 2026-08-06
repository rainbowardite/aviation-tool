from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder

def find_timezone_from_input(input):
    geolocator = Nominatim(user_agent="city_tz_linker")
    timezone_finder = TimezoneFinder()
    location = geolocator.geocode(input)

    if location:
        timezone_name = timezone_finder.timezone_at(lng=location.longitude, lat=location.latitude)
        return timezone_name

    return None
