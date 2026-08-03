def appropriate_surface(runway: dict):
    options = ["Tarmac", "tar old", "Tar", "Surface paved", "PEM", "paving", "Pavement", "paved", "N", "MET", "L", "S", "Hard", "H", "grass/asphalt", "CONC-TURF", "Concrete/Turf", "concrete", "CONC-G", "CONC", "CON/PAD", "CON/ASP", "CON", "COM", "C", "Bituminous", "Bitumen", "BITUM", "BIT", "BIT", "B", "ASPH-TURF-P", "ASPH-TURF", "ASPH-TRTD-G", "ASPH-TRTD-P", "ASPH-P", "ASPH-GRVL", "ASPH-GRVL-F", "ASPH-GRVL-G", "ASPH-GRVL-P", "ASPH-G", "ASPH-F", "ASPH-CONC-G", "ASPH-CONC-F", "ASPH-CONC", "Asphault", "Asphalt/Turf", "Asphalt/Gravel", "Asphalt/Concrete", "Asphalt", "ASPH/GRVL", "ASPH/ CONC", "ASPH 71/F/C/X/T", "ASPH", "ASP/TURF", "ASP/GVL", "ASP/GRS", "ASP/CONC", "ASP/CON", "ASP", "Ashphalt", "Asfalto", "Asfalt", "ASB", "APSH"]

    can_land = False

    for option in options:
        if runway and runway.surface.upper() == option.upper(): # type: ignore
            can_land = True

    return can_land
