__winc_id__ = "25a8041d2d5e4e3ab61ab1be43bfb863"
__human_name__ = "dictionaries"


def create_passport(name, dob, pob, height, nationality):
    dct = {
        "name": name,
        "date of birth": dob,
        "place of birth": pob,
        "height": height,
        "nationality": nationality,
    }
    return dct


# deel 2 add stamp

def add_stamp(passport, country):
    if "stamps" not in passport:
        passport["stamps"] = []
    if "stamps" in passport and country != passport["nationality"]:
        passport["stamps"].append(country)
    return passport




def check_passport(passport,
                   destination_country,
                   allowed_destinations_per_country,
                   forbidden_origins_per_country):
    nationality = passport['nationality']
    if destination_country in allowed_destinations_per_country[nationality]:
        if destination_country in forbidden_origins_per_country:
            if nationality in forbidden_origins_per_country[destination_country]:
                return False
            if 'stamps' in passport:
                for stamp in passport['stamps']:
                    if stamp in forbidden_origins_per_country[destination_country]:
                        return False
        return add_stamp(passport, destination_country)
    return False