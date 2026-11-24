import requests
from bs4 import BeautifulSoup

url = "https://www.jeeb.cat/classificacions/fase1/jornadaxml3.php?p2=11047"

response = requests.get(
    url,
    headers={"User-Agent": "Mozilla/5.0"}
)

print("STATUS:", response.status_code)

soup = BeautifulSoup(response.text, "html.parser")

cards = soup.find_all("div", class_="card")

for card in cards:

    local = card.get("data-local", "").lower()
    visit = card.get("data-visit", "").lower()

    if "escola thau a" in local or "escola thau a" in visit:

        print("----- PARTIT TROBAT -----")
        print("LOCAL:", card.get("data-local"))
        print("VISITANT:", card.get("data-visit"))

        text = card.get_text(" ", strip=True)

        print(text[:1000])
        print()
