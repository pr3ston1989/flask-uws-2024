from flask import Flask, render_template, abort
import requests
from dotenv import load_dotenv
import os
import re
import zulu

load_dotenv()

api_url = "https://rekrutacja.teamwsuws.pl/events/"


app = Flask(__name__)

def url_to_anchor(text):
    """
    url_to_anchor jako argument przyjmuje dowolny tekst i zamienia w nim
    wszystkie linki na anchor tagi prawidłowo wyświetlające się w HTML.
    """
    pattern = r'(https?://[^\s]+)'
    def replace(match):
        url = match.group(0)
        return f'<a href="{url}">{url}</a>'
    return re.sub(pattern, replace, text)


def fetch_events_data(url):
    """
    fetch_events_data przyjmuje link do endpointu i wysyła zapytanie do API,
    następnie zwraca otrzymane dane w formacie JSON lub błąd.
    """
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

def events_basic_info(events_data):
    """
    events_basic_info przyjmuje jako argument dane zwrócone przez API.
    Tworzy listę nowych słowników zawierających podstawowe dane
    o wydarzeniach i odpowiednio je formatuje w celu automatycznego
    wyświetlenia w FullCalendar.
    """
    default_datetime = str(zulu.now()).split('.')[0]
    basic_info = []
    for event in events_data:
        if event.get('id'):
            current_event = {
                'id': event['id'],
                'title': event.get('name', 'Brak tytułu'),
                'start': event.get('start_time', default_datetime),
                'short_description': event.get('short_description', 'Brak opisu'),
                # FullCalendar wymaga formatu HH:MM:SS dla czasu trwania wydarzeń.
                'duration': f"{event.get('duration', 1)}:00:00",
            }
        basic_info.append(current_event)
    return basic_info

def format_data(data):
    """
    format_data jako argument przyjmuje szczegółowe dane o konkretnym wydarzeniu.
    Służy do formatowania danych z API do prawidłowego wyświetlenia w HTML.
    Dzieli wejściowy czas rozpoczęcia na datę oraz godzinę (w przypadku braku tej informacji
    zwraca domyślną wartość, jaką jest data i czas z momentu wysłania zapytania).
    W szczegółowym opisie wydarzenia zamienia znaki nowej linii na tagi <br>,
    usuwa zbędne cudzysłowy, a także zamienia linki na anchor tagi, po czym zwraca sformatowane dane.
    """
    default_datetime = str(zulu.now()).split('.')[0]
    data['date'] = data.get('start_time', default_datetime).split('T')[0]
    data['time'] = data.get('start_time', default_datetime).split('T')[1]
    data['long_description'] = url_to_anchor(data.get('long_description', "Brak opisu."))
    data['long_description'] = data['long_description'].replace('\n', '<br>')
    data['long_description'] = data['long_description'].strip('"')
    data['long_description'] = data['long_description'].replace('""', '"')
    return data

@app.route("/")
def home():
    """Ścieżka do strony głównej - wyświetla kalendarz ze wszystkimi wydarzeniami."""
    events_data = fetch_events_data(api_url)
    basic_info = events_basic_info(events_data)
    events_selection = "Wszystkie wydarzenia:"
    return render_template("index.html", basic_info=basic_info, events_selection=events_selection)


@app.route("/event/<int:event_id>")
def get_event_details(event_id):
    """Ścieżka do konretnego wydarzenia, wypełnia szablon danymi i zwraca HTML."""
    event_url = f'{api_url}{event_id}'
    more_info = fetch_events_data(event_url)
    if not more_info:
        abort(404, description="Wydarzenie nie istnieje.")   
    more_info = format_data(more_info) 

    return render_template("event_dialog.html", more_info=more_info)


@app.route("/tag/<tag>")
def get_events_by_tag(tag):
    """Ścieżka do strony kalendarza wydarzeń dla konkretnego tagu."""
    tag_url = f'{api_url}filter/?tag={tag}'
    events_data = fetch_events_data(tag_url)
    if not events_data:
        abort(404, description=f"Nie znaleziono wydarzeń oznaczonych tagiem '{tag}'.")
    basic_info = events_basic_info(events_data)
    events_selection = f'Wydarzenia oznaczone tagiem "{tag}":'
    return render_template("index.html", events_selection=events_selection, basic_info=basic_info)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)