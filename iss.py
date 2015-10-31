import requests
from datetime import datetime


def get_next_pass(lat, lon):
    iss_url = 'http://api.open-notify.org/iss-pass.json'
    location = {'lat': lat, 'lon': lon}
    response = requests.get(iss_url, params=location).json()

    next_pass = response['response'][0]['risetime']
    return datetime.fromtimestamp(next_pass)
