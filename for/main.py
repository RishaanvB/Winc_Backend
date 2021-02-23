from helpers import get_countries


""" Leave this untouched. Wincpy uses it to match this assignment with the
tests it runs. """
__winc_id__ = 'c545bc87620d4ced81cbddb8a90b4a51'
__human_name__ = 'for'


""" Your code here. """

# This block is only run if this file is the entrypoint; python main.py
# It is not run if it is imported as a module: `from main import *`
if __name__ == '__main__':
    countries = get_countries()


def shortest_names():
    shortest_len = min(len(country)for country in countries)
    list_of_short_names = []
    for country in countries:
        if len(country) == shortest_len:
            list_of_short_names.append(country)
    print(list_of_short_names)


# print(shortest_names())

def most_vowels():
    vowels = "aiuoe"
    leaderboard = [("", 0)]
    # define vowels
    # loop over countries
    for country_name in countries:
        vowel_count = 0
        for country_character in country_name:
            if country_character.lower() in vowels:
                vowel_count += 1
# copy/paste
        for position in range(len(leaderboard)):
            if vowel_count >= leaderboard[position][1]:
                leaderboard.insert(position, (country_name, vowel_count))
                break
            if position > 2:
                break

    # return print([x[0] for x in leaderboard[:3]])
# copy/paste

most_vowels()

def alphabet_set():
    alphabet = list("abcdefghijklmnopqrstuvwxyz")
    countries_used = []
    countrie_lower = [country.lower() for country in countries]
    for country in countries:
        for char in country:
            if char in alphabet:
                alphabet.remove(char)
                if country not in countries_used:
                    countries_used.append(country)
    if len(alphabet) == 0:
        print(countries_used) 
alphabet_set()