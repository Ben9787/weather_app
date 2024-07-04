import main
import pytest
import requests

base_URL = "http://127.0.0.1:8000/weather"
API_KEY = "29c984d578c0119be26f234eca6a6bd2"
data = {'coord': {'lon': -5.9333, 'lat': 54.5833}, 'weather': [{'id': 802, 'main': 'Clouds', 'description': 'scattered clouds', 'icon': '03d'}], 'base': 'stations', 'main': {'temp': 15.92, 'feels_like': 14.87, 'temp_min': 15.26, 'temp_max': 16.88, 'pressure': 1003, 'humidity': 50, 'sea_level': 1003, 'grnd_level': 991}, 'visibility': 10000, 'wind': {'speed': 11.83, 'deg': 270}, 'clouds': {'all': 45}, 'dt': 1720105160, 'sys': {'type': 1, 'id': 1376, 'country': 'GB', 'sunrise': 1720065298, 'sunset': 1720126865}, 'timezone': 3600, 'id': 2655984, 'name': 'Belfast', 'cod': 200}

def test_fetch_weather():
    """
    Test for status codes, response times and data formats
    """
    city = "Belfast"
    response = requests.get(base_URL, params={'city': city})
    assert response.status_code == 200, f"Status code is {response.status_code}"

    data = response.json()      #Comment is what it says if the assert fails
    assert "min_temp" in data, "min temp is missing in the response"
    assert "max_temp" in data, "max temp is missing in the response"
    assert "avg_temp" in data, "avg temp is missing in the response"
    assert "avg_humidity" in data, "humidity is missing in the response"

def test_process_data():
    """
    Test whether the data is present and correct
    :return:
    """
    assert main.process_data("Belfast", data), "Process data returned null"


