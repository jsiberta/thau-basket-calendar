from icalendar import Calendar, Event
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import requests
import pytz
import re

ICS_URLS = [
    (
        "🔵 SENIOR",
        "https://calendaris.cat/s/5pL7962F.ics",
    ),
    (
        "🟢 SOTS25",
        "https://calendaris.cat/s/ZWhWBfGa.ics",
    ),
]

calendar = Calendar()

calendar.add("prodid", "-//THAU Basket Combined//")
calendar.add("version", "2.0")

#
# FEDERATS
#
for prefix, url in ICS_URLS:

    print(f"Descarregant {url}")

    response = requests.get(url, timeout=60)
    response.raise_for_status()

    source_cal = Calendar.from_ical(response.text)

    for component in source_cal.walk():

        if component.name == "VEVENT":

            original_summary = str(
                component.get("SUMMARY", "")
            )

            component["SUMMARY"] = (
                f"{prefix} | {original_summary}"
            )

            calendar.add_component(component)

#
# CEEB
#
print("Descarregant partits CEEB")

url = (
    "https://www.jeeb.cat/classificacions/"
    "fase1/jornadaxml3.php?p2=11047"
)

response = requests.get(
    url,
    headers={
        "User-Agent": "Mozilla/5.0"
    },
    timeout=60
)

soup = BeautifulSoup(
    response.text,
    "html.parser"
)

cards = soup.find_all(
    "div",
    class_="card"
)

tz = pytz.timezone(
    "Europe/Madrid"
)

for card in cards:

    local = card.get(
        "data-local",
        ""
    ).strip()

    visitant = card.get(
        "data-visit",
        ""
    ).strip()

    if not (
        local.lower() == "escola thau a"
        or visitant.lower() == "escola thau a"
    ):
        continue

    text = card.get_text(
        " ",
        strip=True
    )

    data_match = re.search(
        r"Data Joc:\s*[A-Za-zÀ-ÿ]+\s+(\d{2}-\d{2}-\d{4})",
        text
    )

    hora_match = re.search(
        r"Hora de Joc:\s*([0-9']+h)",
        text
    )

    camp_match = re.search(
        r"Nom Camp:\s*(.*?)\s*Direcció:",
        text
    )

    if (
        not data_match
        or not hora_match
    ):
        continue

    data = data_match.group(1)

    hora = (
        hora_match.group(1)
        .replace("h", "")
        .replace("'", ":")
    )

    try:

        dt = datetime.strptime(
            f"{data} {hora}",
            "%d-%m-%Y %H:%M"
        )

        dt = tz.localize(dt)

    except Exception:
        continue

    camp = ""

    if camp_match:
        camp = (
            camp_match
            .group(1)
            .strip()
        )

    event = Event()

    event.add(
        "summary",
        f"🟡 CEEB | {local} vs {visitant}"
    )

    event.add(
        "dtstart",
        dt
    )

    event.add(
        "dtend",
        dt + timedelta(hours=2)
    )

    event.add(
        "location",
        camp
    )

    calendar.add_component(
        event
    )

with open(
    "thau_basket.ics",
    "wb"
) as f:
    f.write(
        calendar.to_ical()
    )

print(
    "Calendari unificat generat correctament"
)
