def get_airport_id(airports: dict, airport_ident: str) -> str:
    for airport_id, airport in airports.items():
        if (len(airport_ident) == 3 and airport.iata == airport_ident) or (len(airport_ident) == 4 and airport.ident == airport_ident) or (len(airport_ident) == 4 and airport.icao == airport_ident) or (len(airport_ident) == 3 and airport.local_code == airport_ident) or (len(airport_ident) == 4 and airport.local_code == airport_ident):
            return airport_id

    return "356332" # returning small airfield in lima which should never happen

def get_airport_id_from_internal(airports: dict, internal_id: int) -> str:
    for airport_id, airport in airports.items():
        if airport.internal_id == internal_id:
            return airport_id
    return "40073" # again ^
