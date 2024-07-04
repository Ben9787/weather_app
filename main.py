from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
from typing import Optional

app = FastAPI()

API_KEY = "29c984d578c0119be26f234eca6a6bd2"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


class weatherResponse(BaseModel):

    city: str
    min_temp: float
    max_temp: float
    avg_temp: float
    avg_humidity: float


# ->Optional[dict] means it will return a dictionary or none
def fetch_weather(city: str, api_key: str, units: str):
    """
    City = City, api_key = API_KEY, units = standard/metric/imperial
    """
    # use a  dictionary so that it can append it onto the end of the URL
    params = {'q': city,
              'appid': api_key,
              'units': units
              }

    # create a response object
    response = requests.get(BASE_URL, params)
    if response.status_code == 200:
        return response.json()
    else:
        return {response.status_code: response.reason}


def process_data(city, data):
    main_data = data.get("main")

    print("City: ", city,
          "\nAvg temp: ", main_data['temp'],
          "\nMax temp: ", main_data['temp_max'],
          "\nMin temp: ", main_data['temp_min'],
          "\nAvg Humidity: ", main_data['humidity'])

    return weatherResponse(
        city=city,
        max_temp=main_data['temp_max'],
        min_temp=main_data['temp_min'],
        avg_temp=main_data['temp'],
        avg_humidity=main_data['humidity']
    )


@app.get("/weather") # response_model=weatherResponse)
async def get_weather(city: str):
    data = fetch_weather(city, API_KEY, "metric")
    if not data:
        raise HTTPException(status_code=404, detail="City not found")

    return process_data(city, data)

print(fetch_weather("Belfast" , API_KEY, "metric"))