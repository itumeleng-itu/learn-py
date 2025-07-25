import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook 
import os

def scrape_website():
    url = "https://test-scrape-site.onrender.com/historical-events.html"

    try:
        response = requests.get(url)  # sending http get requests to my url link
        response.raise_for_status()  # if link is not found, respond with an error

        soup = BeautifulSoup(response.text, "html.parser")

        items = soup.find_all('li')
        events = []

        for item in items:
            lines = item.get_text(separator="\n").split("\n")
            data = {'Year': 'N/A', 'Event': 'N/A', 'Location': 'N/A', 'Description': 'N/A'}

            for i in range(len(lines)):
                line = lines[i].strip()
                if line.startswith("Year:"):
                    data['Year'] = lines[i + 1].strip() if i + 1 < len(lines) else 'N/A'
                elif line.startswith("Event:"):
                    data['Event'] = lines[i + 1].strip() if i + 1 < len(lines) else 'N/A'
                elif line.startswith("Location:"):
                    data['Location'] = lines[i + 1].strip() if i + 1 < len(lines) else 'N/A'
                elif line.startswith("Description:"):
                    data['Description'] = lines[i + 1].strip() if i + 1 < len(lines) else 'N/A'

            events.append(data)

        wb = Workbook() 
        ws = wb.active
        ws.title = "Historical Events"

        ws.append(['Year', 'Event', 'Location', 'Description'])

        for event in events:
            ws.append([event['Year'], event['Event'], event['Location'], event['Description']])

        filename = "scraped_events_output.xlsx"
        wb.save(filename)

        print(f"Data saved to {filename}")
        print(os.path.abspath(filename))
        return len(events)

    except Exception as e:
        print(f"An error occurred: {e}")
        return 0


if __name__ == "__main__":
    count = scrape_website()
    print(f"Total events scraped: {count}")