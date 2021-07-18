import requests
from urllib.parse import urlencode


def get_reviews(album, n=3):
    data = {"q": f"{album} review", "num": n}
    url = f"https://google-search3.p.rapidapi.com/api/v1/search/{urlencode(data)}"

    headers = {
        'x-rapidapi-key': "key",
        'x-rapidapi-host': "google-search3.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers)
    results = []
    for i in response.json()["results"]:
        results.append((i["title"], i["link"]))
    return results
