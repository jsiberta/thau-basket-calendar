from icalendar import Calendar
import requests

ICS_URLS = [
    "https://calendaris.cat/s/5pL7962F.ics",
    "https://calendaris.cat/s/ZWhWBfGa.ics",
]

calendar = Calendar()

calendar.add("prodid", "-//THAU Basket Combined//")
calendar.add("version", "2.0")

for url in ICS_URLS:

    print(f"Descarregant {url}")

    response = requests.get(url, timeout=60)

    response.raise_for_status()

    source_cal = Calendar.from_ical(response.text)

    for component in source_cal.walk():
        if component.name == "VEVENT":
            calendar.add_component(component)

with open("thau_basket.ics", "wb") as f:
    f.write(calendar.to_ical())

print("Calendari unificat generat correctament")
