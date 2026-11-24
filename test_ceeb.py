import requests

url = "https://www.jeeb.cat/classificacions/fase1/jornadaxml3.php?p2=11047"

response = requests.get(
    url,
    headers={"User-Agent": "Mozilla/5.0"}
)

html = response.text.lower()

print("STATUS:", response.status_code)

print(
    "THAU LOCAL:",
    html.count('data-local="escola thau a"')
)

print(
    "THAU VISITANT:",
    html.count('data-visit="escola thau a"')
)
