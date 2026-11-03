from icalendar import Calendar, Event
from datetime import datetime, timedelta
import pytz

cal = Calendar()
cal.add("prodid", "-//THAU Basket Calendar//")
cal.add("version", "2.0")

tz = pytz.timezone("Europe/Madrid")

event = Event()
event.add("summary", "Prova THAU Basket")
event.add(
    "dtstart",
    tz.localize(datetime(2026, 11, 10, 18, 0))
)
event.add(
    "dtend",
    tz.localize(datetime(2026, 11, 10, 20, 0))
)
event.add("location", "Barcelona")

cal.add_component(event)

with open("thau_basket.ics", "wb") as f:
    f.write(cal.to_ical())

print("Calendari generat: thau_basket.ics")
