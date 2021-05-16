__winc_id__ = "25a8041d2d5e4e3ab61ab1be43bfb863"
__human_name__ = "dictionaries"


from helpers import get_countries


# part 1
def create_passport(name, dob, pob, height, nationality):
    return {
        "name": name,
        "date_of_birth": dob,
        "place_of_birth": pob,
        "height": height,
        "nationality": nationality,
    }


#  part 2


def add_stamp(passport, country):
    # same country do nothing
    if "stamps" not in passport:
        passport["stamps"] = []

    if country not in passport["stamps"] and country != passport["nationality"]:
        passport["stamps"].append(country)
    return passport

# part 3

def check_passport(passport, to_country, allowed_countries_for_country, not_allowed_countries_for_country):
    nationality = passport["nationality"]
    if to_country in allowed_countries_for_country[nationality]:
        
        return add_stamp(passport, to_country)
    if nationality in not_allowed_countries_for_country[to_country]:
        return False
    for stamp in passport["stamps"]:
        if stamp in not_allowed_countries_for_country:
            return False