import requests
from bs4 import BeautifulSoup
import re

url = "https://www.jeeb.cat/classificacions/fase1/jornadaxml3.php?p2=11047"

response = requests.get(
    url,
    headers={"User-Agent": "Mozilla/5.0"}
)

print("STATUS:", response.status_code)

soup = BeautifulSoup(response.text, "html.parser")

cards = soup.find_all("div", class_="card")

for card in cards:

    local = card.get("data-local", "").strip()
    visitant = card.get("data-visit", "").strip()

    if (
        local.lower() == "escola thau a"
        or visitant.lower() == "escola thau a"
    ):

        text = card.get_text(" ", strip=True)

        data = re.search(
            r"Data Joc:\s*([A-Za-zÀ-ÿ]+\s+\d{2}-\d{2}-\d{4})",
            text
        )

        hora = re.search(
            r"Hora de Joc:\s*([0-9']+h)",
            text
        )

        camp = re.search(
            r"Nom Camp:\s*(.*?)\s*Direcció:",
            text
        )

        print()
        print("=" * 60)

        print(
            f"🟡 CEEB | {local} vs {visitant}"
        )

        if data:
            print("📅", data.group(1))

        if hora:
            print(
                "🕒",
                hora.group(1).replace("'", ":")
            )

        if camp:
            print(
                "📍",
                camp.group(1).strip()
            )

        print("=" * 60)
