from surface import appropriate_surface

def get_longest_runway_id(runways: dict, runway_list: list) -> int:
    if len(runway_list) == 1:
        runway = runways.get(str(runway_list[0]))
        if runway:
            if appropriate_surface(runway):
                return runway_list[0]
            else:
                return 0
    else:
        runway_length_list = []
        for runway_id in runway_list:
            if runways:
                runway = runways.get(str(runway_id))
                if runway:
                    runway_length = runway.length
                    if appropriate_surface(runway):
                        runway_length_list.append(runway_length)

        if len(runway_length_list) > 0:
            longest_runway_index = runway_length_list.index(max(runway_length_list, key=int))
            return runway_list[longest_runway_index]
        else:
            return 0

def get_runway_id(runways: dict, airport_id: str) -> int:
    runway_list = []
    for runway_id, runway in runways.items():
        if runway.id == airport_id:
            runway_list.append(runway_id)

    if len(runway_list) == 0:
        return 0
    elif len(runway_list) == 1:
        return runway_list[0]
    else:
        longest_runway_id = get_longest_runway_id(runways, runway_list)
        return longest_runway_id
