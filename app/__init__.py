from flask import Flask, render_template
import requests
from dotenv import load_dotenv
import os

load_dotenv()

def fetch_events_data():
    api_url = "https://rekrutacja.teamwsuws.pl/events/"
    api_key = os.getenv('API_KEY')
    
    headers = {
        'api-key': api_key,
    }
    response = requests.get(url=api_url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None
    
def events_basic_info(events_data):
    basic_info = []
    for event in events_data:
        current_event = {
            'title': event['name'],
            'start': event['start_time'].split('T')[0],
        }
        basic_info.append(current_event)
    return basic_info


app = Flask(__name__)

@app.route("/")
def home():
    events_data = fetch_events_data()
    basic_info = events_basic_info(events_data)
    return render_template("index.html", basic_info=basic_info)


if __name__ == "__main__":
    app.run(debug=True)