import requests
from bs4 import BeautifulSoup
import csv

# URL of the Wikipedia page
url = "https://en.wikipedia.org/wiki/Timeline_of_the_21st_century"

# Fetch the webpage
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

# Extract events
events = []
seen_events = set()  # To track unique events
content = soup.find("div", class_="mw-parser-output")  # Main content area

if content:
    current_year = None  # To track the year
    current_date = None  # To track the specific date for events

    for div in content.find_all("div", class_="mw-heading mw-heading3"):
        # Extract the year
        h3 = div.find("h3")
        if h3:
            year = h3.get_text(strip=True)
            current_year = year
            current_date = None  # Reset the date when a new year starts

        # Find the next <ul> containing events
        ul = div.find_next_sibling("ul")
        if ul and current_year:
            for li in ul.find_all("li"):
                event_text = li.get_text(" ", strip=True)
                # Split date and event if available
                if ": " in event_text:
                    date, event = event_text.split(": ", 1)
                    current_date = date.strip()  # Track the date for later events
                else:
                    event = event_text
                    date = current_date if current_date else "Unknown date"

                # Split events if there are multiple events on the same date
                events_list = event.split(" . ")  # Split on the period
                for ev in events_list:
                    ev = ev.strip()
                    if ev:  # Ensure the event is not empty
                        # Ensure each event is unique
                        unique_key = (current_year, date.strip(), ev)
                        if unique_key not in seen_events:  # Check for duplicates
                            seen_events.add(unique_key)
                            events.append(
                                {
                                    "Year": current_year,
                                    "Date": date.strip(),
                                    "Event": ev,
                                }
                            )

# Save results to a CSV file
output_file = "timeline_events.csv"

# Specify the CSV header
csv_header = ["Year", "Date", "Event"]

# Write to the CSV file
with open(output_file, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=csv_header)
    writer.writeheader()
    writer.writerows(events)

print(f"Data has been saved to {output_file}.")
