import re
import requests
from io import BytesIO
from datetime import datetime, timedelta

import pytz
from PyPDF2 import PdfReader
from icalendar import Calendar, Event

PDF_URLS = [
    (
        "C.E. THAU Senior",
        "https://www.basquetcatala.cat/partits/calendari_equip_global/pdf/91369",
    ),
    (
        "C.E. THAU B Sots25",
        "https://www.basquetcatala.cat/partits/calendari_equip_global/pdf/91370",
    ),
]

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/131.0 Safari/537.36"
    ),
    "Referer": "https://www.basquetcatala.cat/",
}

tz = pytz.timezone("Europe/Madrid")

cal = Calendar()
cal.add("prodid", "-//THAU Basket Calendar//")
cal.add("version", "2.0")

date_re = re.compile(r"(\d{2}-\d{2}-\d{4})\s+(\d{2}:\d{2})")

for team_name, url in PDF_URLS:

    print(f"Descarregant {team_name}")

    response = requests.get(
        url,
        headers=HEADERS,
        timeout=60,
    )

    response.raise_for_status()

    pdf = PdfReader(BytesIO(response.content))

    text = "\n".join(
        page.extract_text() or ""
        for page in pdf.pages
    )

    matches = list(date_re.finditer(text))

    print(f"Trobats {len(matches)} partits")

    for i, match in enumerate(matches):

        start_pos = match.start()

        if i + 1 < len(matches):
            end_pos = matches[i + 1].start()
        else:
            end_pos = len(text)

        block = text[start_pos:end_pos]

        date_str = match.group(1)
        time_str = match.group(2)

        try:
            dt = datetime.strptime(
                f"{date_str} {time_str}",
                "%d-%m-%Y %H:%M"
            )

            dt = tz.localize(dt)

        except Exception:
            continue

        first_line = block.split("\n")[0]

        summary = re.sub(
            r"^\d{2}-\d{2}-\d{4}\s+\d{2}:\d{2}\s*",
            "",
            first_line,
        ).strip()

        location = ""

        loc_match = re.search(
            r"Instal·lació:\s*(.*)",
            block,
            re.DOTALL,
        )

        if loc_match:
            location = loc_match.group(1).strip()

        event = Event()

        event.add("summary", summary)
        event.add("dtstart", dt)
        event.add("dtend", dt + timedelta(hours=2))
        event.add("location", location)
        event.add("description", team_name)

        cal.add_component(event)

with open("thau_basket.ics", "wb") as f:
    f.write(cal.to_ical())

print("Calendari THAU generat correctament")
