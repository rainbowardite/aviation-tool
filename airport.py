def get_airport_id(airports: dict, airport_ident: str) -> str:
    for airport_id, airport in airports.items():
        if airport.ident == airport_ident:
            return airport_id

def get_airport_id_from_internal(airports: dict, internal_id: int) -> str:
    for airport_id, airport in airports.items():
        if airport.internal_id == internal_id:
            return airport_id
