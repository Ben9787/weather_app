import main
import pytest
import requests

base_URL = "http://127.0.0.1:8000/weather"
# data = {'coord': {'lon': -5.9333, 'lat': 54.5833},
#         'weather': [{'id': 803, 'main': 'Clouds', 'description': 'broken clouds', 'icon': '04d'}], 'base': 'stations',
#         'main': {'temp': 12.93, 'feels_like': 12.32, 'temp_min': 12.9, 'temp_max': 14.1, 'pressure': 1004,
#                  'humidity': 78, 'sea_level': 1004, 'grnd_level': 992}, 'visibility': 7000,
#         'wind': {'speed': 9.77, 'deg': 280}, 'clouds': {'all': 75}, 'dt': 1720089525,
#         'sys': {'type': 1, 'id': 1376, 'country': 'GB', 'sunrise': 1720065298, 'sunset': 1720126865}, 'timezone': 3600,
#         'id': 2655984, 'name': 'Belfast', 'cod': 200}


#def test_process_data():




def test_fetch_weather(city):
    """
    Test for status codes, response times and data formats
    """
    response = requests.get(base_URL, params={'city': city})
    assert response.status_code == 200, f"Status code is {response.status_code}"

    data = response.json()
    assert "min_temp" in data