from flask import Flask, render_template, abort
import requests
from dotenv import load_dotenv
import os

load_dotenv()

api_url = "https://rekrutacja.teamwsuws.pl/events/"


app = Flask(__name__)


# Funkcja pobierająca dane z API.
def fetch_events_data(url):
    api_key = os.getenv('API_KEY')    
    headers = {
        'api-key': api_key,
    }
    try:
        response = requests.get(url=url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_error:
        print(f"HTTP error occured: {http_error}")
        abort(500, description="Wystąpił błąd serwera, nie udało się pobrać danych z API.")

# Funkcja formatująca dane dla wyświetlenia w FullCalendar.
def events_basic_info(events_data):
    basic_info = []
    for event in events_data:
        current_event = {
            'id': event['id'],
            'title': event['name'],
            'start': event['start_time'],
            'short_description': event['short_description'],
            # FullCalendar wymaga formatu HH:MM:SS dla czasu wydarzeń.
            'duration': f"0{event['duration']}:00:00",
        }
        basic_info.append(current_event)
    return basic_info

# Ścieżka wyświetlająca kalendarz ze wszystkimi wydarzeniami zwróconymi przez API.
@app.route("/")
def home():
    events_data = fetch_events_data(api_url)
    basic_info = events_basic_info(events_data)
    events_selection = "Wszystkie wydarzenia:"
    return render_template("index.html", basic_info=basic_info, events_selection=events_selection)

# Ścieżka wypełnia szablon szczegółowymi informacjami o wydarzeniu.
@app.route("/event/<int:event_id>")
def get_event_details(event_id):
    event_url = f'{api_url}{event_id}'
    more_info = fetch_events_data(event_url)
    print(more_info)
    if not more_info:
        abort(404, description="Wydarzenie nie istnieje.")

    more_info['date'] = more_info['start_time'].split('T')[0]
    more_info['time'] = more_info['start_time'].split('T')[1]
    return render_template("event_dialog.html", more_info=more_info)

# Ścieżka wyświetlająca kalendarz z wydarzeniami oznaczonymi konkretnym tagiem.
@app.route("/tag/<tag>")
def get_events_by_tag(tag):
    tag_url = f'{api_url}filter/?tag={tag}'
    events_data = fetch_events_data(tag_url)
    if not events_data:
        abort(404, description=f"Nie znaleziono wydarzeń oznaczonych tagiem '{tag}'.")
    basic_info = events_basic_info(events_data)
    events_selection = f'Wydarzenia oznaczone tagiem "{tag}":'
    return render_template("index.html", events_selection=events_selection, basic_info=basic_info)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)