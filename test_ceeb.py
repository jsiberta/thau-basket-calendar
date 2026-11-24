import requests
import re

url = "https://www.jeeb.cat/classificacions/fase1/jornadaxml3.php?p2=11047"

response = requests.get(
    url,
    headers={
        "User-Agent": "Mozilla/5.0"
    }
)

print("STATUS:", response.status_code)

matches = re.findall(
    r"Escola Thau",
    response.text,
    re.IGNORECASE
)

print("THAU:", len(matches))

pos = response.text.lower().find("escola thau")

if pos > 0:
    print(response.text[pos:pos+3000])
