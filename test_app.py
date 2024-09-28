import pytest
from app import app, events_basic_info, format_data, url_to_anchor

@pytest.fixture
def client():
    with app.test_client() as client:
            yield client

def test_events_basic_info():
    events_data = [
        {
            'id': 3,
            'name': 'Jubileuszowy Piknik Naukowy',
            'start_time': '2024-10-02T10:00:00',
            'duration': 2,
            'short_description': '''Jubileuszowy Piknik Naukowy UwS to dzień pełen atrakcji dla dzieci
                                    i dorosłych, z warsztatami, grami i występami.'''
        },
        {
            'id': 4,
            'name': 'Dyktando Siedleckie',
            'start_time': '2024-10-12T13:00:00',
            'duration': 1,
            'short_description': '''Dyktando Siedleckie to prestiżowy konkurs ortograficzny
                                    z nagrodami, w którym mogą wziąć udział miłośnicy języka polskiego.''',
        },
        {
            'id': 5,
            'name': 'Konfernecja naukowa management 2024',
            'start_time': '2024-09-23T14:00:00',
            'duration': 2,
            'short_description': '''XVII Międzynarodowa Konferencja MANAGEMENT 2024 to wydarzenie
                                    o rozwoju organizacji, pełne wykładów i inspirujących dyskusji.'''
        }]
    
    result = events_basic_info(events_data)

    assert len(result) == len(events_data)
    assert result[1]['duration'] == '01:00:00'
    assert result[2]['id'] == 5
    assert result[0]['start'] == '2024-10-02T10:00:00'

def test_home(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Wszystkie wydarzenia:" in response.data

def test_get_event_details(client):
     response = client.get("/event/6")
     assert response.status_code == 200
     assert b'<a href="https://' in response.data
     assert b"Siedlc" in response.data

def test_get_events_by_tag(client):
    response = client.get("/tag/Konferencja")     
    assert response.status_code == 200
    assert b'<h1> Wydarzenia oznaczone tagiem &#34;Konferencja&#34;: </h1>' in response.data

def test_get_event_details_not_found(client):
     response = client.get("/event/123")
     assert response.status_code == 500
     
def test_get_events_by_tag_not_found(client):
     response = client.get("/tag/nieistniejacy_tag")
     assert response.status_code == 500

def test_format_data():
     data = {
             'start_time': '2024-10-12T13:00:00',
             'long_description': '''"Mamy zaszczyt ogłosić, że kolejna edycja naszego prestiżowego konkursu ortograficznego ""Dyktando Siedleckie"" już niedługo!📝'''}
     
     result = format_data(data)
     assert result['date'] == '2024-10-12'
     assert result['time'] == '13:00:00'
     assert result['long_description'] == '''Mamy zaszczyt ogłosić, że kolejna edycja naszego prestiżowego konkursu ortograficznego "Dyktando Siedleckie" już niedługo!📝'''

def test_url_to_anchor():
    text = 'https://wydarzenia.uws.edu.pl/\n'
    result = url_to_anchor(text)
    assert result == '<a href="https://wydarzenia.uws.edu.pl/">https://wydarzenia.uws.edu.pl/</a>\n'