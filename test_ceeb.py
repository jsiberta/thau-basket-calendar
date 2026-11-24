import requests

url = "https://www.jeeb.cat/classificacions/fase1/jornadaxml3.php?p2=11047"

response = requests.get(
    url,
    headers={
        "User-Agent": "Mozilla/5.0"
    }
)

print("STATUS:", response.status_code)

count = response.text.lower().count("escola thau")

print("PARTITS THAU TROBATS:", count)
