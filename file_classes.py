class Airport:
    def __init__(self, internal_id, id, ident, type, name, lat, long, elev, continent, country, region, municipality, shed_serv, icao, iata, gps_code, local_code, link, wikipedia, kwrds):
        self.internal_id = internal_id
        self.id = id
        self.ident = ident
        self.type = type
        self.name = name
        self.lat = lat
        self.long = long
        self.elev = elev
        self.continent = continent
        self.country = country
        self.region = region
        self.municipality = municipality
        self.shed_serv = shed_serv
        self.icao = icao.upper()
        self.iata = iata.upper()
        self.gps_code = gps_code.upper()
        self.local_code = local_code.upper()
        self.link = link
        self.wikipedia = wikipedia
        self.kwrds = kwrds

class Region:
    def __init__(self, region_id, code, local_code, name, continent, country, wikipedia, kwrds):
        self.country_id = region_id
        self.code = code
        self.local_code = local_code
        self.name = name
        self.continent = continent
        self.country = country
        self.wikipedia = wikipedia
        self.kwrds = kwrds

class Country:
    def __init__(self, country_id, code, name, continent, wikipedia, kwrds):
        self.country_id = country_id
        self.code = code
        self.name = name
        self.continent = continent
        self.wikipedia = wikipedia
        self.kwrds = kwrds

class Runway:
    def __init__(self, runway_id, id, airport_code, length, width, surface, lighted, closed, le_ident, le_lat, le_long, le_elev, le_heading, le_displaced_threshold, he_ident, he_lat ,he_longitude_deg, he_elev, he_heading, he_displaced_threshold):
        self.runway_id = runway_id
        self.id = id
        self.airport_code = airport_code
        self.length = length
        self.width = width
        self.surface = surface
        self.lighted = lighted
        self.closed = closed
        self.le_ident = le_ident
        self.le_lat = le_lat
        self.le_long = le_long
        self.le_elev = le_elev
        self.le_heading = le_heading
        self.le_displaced_threshold = le_displaced_threshold
        self.he_ident = he_ident
        self.he_lat = he_lat
        self.he_longitude_deg = he_longitude_deg
        self.he_elev = he_elev
        self.he_heading = he_heading
        self.he_displaced_threshold = he_displaced_threshold
