# Kalendarz wydarzeń

Projekt we Flask pobierający wydarzenia z API i wyświetlający je w kalendarzu FullCalendar.

## Instalacja

### Krok 1: Sklonowanie repozytorium

```sh
git clone <https://github.com/pr3ston1989/flask-uws-2024.git>
cd flask-uws-2024
```

### Krok 2: Utworzenie środowiska wirtualnego i instalacja zależności

#### Windows:

```sh
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

#### Linux: 

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Krok 3: Ustawienie zmiennej środowiskowej dla klucza API

```sh
set API_KEY=klucz_api
```

```bash
export API_KEY="klucz_api"
```

### Krok 4: Uruchomienie aplikacji

```sh
flask run
```

Aplikacja domyślnie działa na porcie 5000 i powinna być dostępna pod [tym](http://127.0.0.1:5000/) adresem.

### Opcjonalnie: Testowanie aplikacji

`pytest`

## Live Demo

[Link do aplikacji](http://ec2-3-8-3-192.eu-west-2.compute.amazonaws.com/)

sudo docker pull dpietrzak89/flask-uws

sudo docker run -d --name flask-app -e API_KEY=kluczAPI -p 5000:5000 dpietrzak89/flask-uws