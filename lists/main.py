# Do not modify these lines
__winc_id__ = '6eb355e1a60f48a28a0bbbd0c88d9ab4'
__human_name__ = 'lists'

# Add your code after this line


def alphabetical_order(movies):
    print(sorted(movies))
    movies.sort()
    return(movies)


def won_golden_globe(movie_name):
    golden_globe_winners = ["string", "string2", "string3", "string4"]
    return (movie_name.lower() in golden_globe_winners)


def remove_albums(albums):
    toto_list = [1, 3, 5]
    for album in albums:
        if album in toto_list:
            albums.remove(album)
    print(albums)
            # albums.remove(album)
    # loop over a
    # check if a is in toto_list
    # remove that index/item from a
    # return a


for i in range(10):
    if i % 2 == 0:
        print(i)
        