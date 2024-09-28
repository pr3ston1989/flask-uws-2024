from flask import Flask, render_template, jsonify
import requests
from dotenv import load_dotenv
import os

load_dotenv()

api_url = "https://rekrutacja.teamwsuws.pl/events/"

def fetch_events_data(url):
    api_key = os.getenv('API_KEY')
    
    headers = {
        'api-key': api_key,
    }
    response = requests.get(url=url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return {}
    
def events_basic_info(events_data):
    basic_info = []
    for event in events_data:
        current_event = {
            'id': event['id'],
            'title': event['name'],
            'start': event['start_time'],
            'duration': f"{event['duration']}0:00:00"
        }
        basic_info.append(current_event)
    return basic_info


app = Flask(__name__)

@app.route("/")
def home():
    events_data = fetch_events_data(api_url)
    basic_info = events_basic_info(events_data)
    events_selection = "Wszystkie wydarzenia:"
    return render_template("index.html", basic_info=basic_info, events_selection=events_selection)

@app.route("/event/<int:event_id>")
def get_event_details(event_id):
    event_url = f'{api_url}{event_id}'
    more_info = fetch_events_data(event_url)
    more_info['date'] = more_info['start_time'].split('T')[0]
    more_info['time'] = more_info['start_time'].split('T')[1]
    return render_template("event_dialog.html", more_info=more_info)

@app.route("/tag/<tag>")
def get_events_by_tag(tag):
    tag_url = f'{api_url}filter/?tag={tag}'
    events_data = fetch_events_data(tag_url)
    basic_info = events_basic_info(events_data)
    events_selection = f'Wydarzenia oznaczone tagiem "{tag}":'
    return render_template("index.html", basic_info=basic_info, events_selection=events_selection)




if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)