import requests


def fetch_user_snippets():
    user = requests.get(
        "https://run.mocky.io/v3/3b7fdcfc-53b9-43e7-9042-53d1870c8693"
    ).json()  # fetch user
    snippets = requests.get(
        "https://run.mocky.io/v3/7f76961a-58b0-4ee2-b6a0-3c4faf90f4ed"
    ).json()  # fetch snippets
    snippets = [
        s["snippet"] if s["user_id"] == user["meta"]["user_id"] else print("no such id")
        for s in snippets
    ]
    print("-->", snippets)
    # print("--> s['snippet']", s["snippet"])
    return snippets


fetch_user_snippets()