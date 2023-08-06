import requests


def call_kanye():
    response = requests.get("https://api.kanye.rest")

    if response.status_code == 200:
        return response.json()['quote']
    else:
        return "Connection to API wasn't successful."


print(call_kanye())
