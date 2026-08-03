import csv
from file_classes import Airport, Country, Runway

def initialize_airports() -> dict:
    airports_by_id = {}

    with open("./files/airports.csv", mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for index, row in enumerate(reader):
            airport_obj = Airport(
                internal_id=index,
                id=row["id"] or "0",
                ident=row["ident"] or "0",
                type=row["type"] or "0",
                name=row["name"] or "0",
                lat=row["latitude_deg"] or "0",
                long=row["longitude_deg"] or "0",
                elev=row["elevation_ft"] or "0",
                continent=row["continent"] or "0",
                country=row["iso_country"] or "0",
                region=row["iso_region"] or "0",
                municipality=row["municipality"] or "0",
                shed_serv=row["scheduled_service"] or "0",
                icao=row["icao_code"] or "0",
                iata=row["iata_code"] or "0",
                gps_code=row["gps_code"] or "0",
                local_code=row["local_code"] or "0",
                link=row["home_link"] or "0",
                wikipedia=row["wikipedia_link"] or "0",
                kwrds=row["keywords"] or "0"
            )

            airports_by_id[airport_obj.id] = airport_obj

    return airports_by_id

#Accessing a specific airport object by its id
#target_airport = airports_by_code.get("3632") # LAX
#target_airport.____

def initialize_country() -> dict:
    countries_by_code = {}

    with open("./files/countries.csv", mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            countries_obj = Country(
                country_id=row["id"] or "0",
                code=row["code"] or "0",
                name=row["name"] or "0",
                continent=row["continent"] or "0",
                wikipedia=row["wikipedia_link"] or "0",
                kwrds=row["keywords"] or "0"
            )

            countries_by_code[countries_obj.code] = countries_obj

    return countries_by_code

def initialize_runway() -> dict:
    runways_by_id = {}

    with open("./files/runways.csv", mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            runways_obj = Runway(
                runway_id=row["id"] or "0",
                id=row["airport_ref"] or "0",
                airport_code=row["airport_ident"] or "0",
                length=row["length_ft"] or "0",
                width=row["width_ft"] or "0",
                surface=row["surface"] or "0",
                lighted=row["lighted"] or "0",
                closed=row["closed"] or "0",
                le_ident=row["le_ident"] or "0",
                le_lat=row["le_latitude_deg"] or "0",
                le_long=row["le_longitude_deg"] or "0",
                le_elev=row["le_elevation_ft"] or "0",
                le_heading=row["le_heading_degT"] or "0",
                le_displaced_threshold=row["le_displaced_threshold_ft"] or "0",
                he_ident=row["he_ident"] or "0",
                he_lat=row["he_latitude_deg"] or "0",
                he_longitude_deg=row["he_longitude_deg"] or "0",
                he_elev=row["he_elevation_ft"] or "0",
                he_heading=row["he_heading_degT"] or "0",
                he_displaced_threshold=row["he_displaced_threshold_ft"] or "0"
            )

            runways_by_id[runways_obj.runway_id] = runways_obj

    return runways_by_id
