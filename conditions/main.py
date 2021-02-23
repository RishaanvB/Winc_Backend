# Do not modify these lines
__winc_id__ = '25596924dffe436da9034d43d0af6791'
__human_name__ = 'conditions'

# Add your code after this line

def farm_action(weather, time_of_day, 
                cow_milking_status, location_cows, 
                season, slurry_tank, grass_status):
    if (location_cows == "pasture" and time_of_day == "night") or (location_cows == "pasture" and weather == "rainy"):
        return print("take cows to cowshed")
    elif cow_milking_status is True and location_cows == "cowshed":
        return print("milk cows")
    elif slurry_tank is True and location_cows == "cowshed" and weather != "sunny" and weather != "windy":
        return print("fertilize pasture")
    elif grass_status is True and season == "spring" and weather == "sunny" and location_cows != "pasture":
        return("mow grass")
    else:
        return print("wait")









farm_action('rainy', 'night', False, 'cowshed', 'winter', False, True)


