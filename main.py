from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import sqlite3
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
    :returns: json file of all weather data if successful
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
        return None


def process_data(city, data):
    """

    :param city:
    :param data:
    :return:    weatherResponse as an object
    :return:    city=city,
    :return:    max_temp=main_data['temp_max'],
    :return:    min_temp=main_data['temp_min'],
    :return:    avg_temp=main_data['temp'],
    :return:    avg_humidity=main_data['humidity']
    """
    main_data = data.get("main")

    print("City: ", city,
          "\nAvg temp: ", main_data['temp'],
          "\nMax temp: ", main_data['temp_max'],
          "\nMin temp: ", main_data['temp_min'],
          "\nAvg Humidity: ", main_data['humidity'])
    #upload_to_db(city)
    return weatherResponse(
        city=city,
        max_temp=main_data['temp_max'],
        min_temp=main_data['temp_min'],
        avg_temp=main_data['temp'],
        avg_humidity=main_data['humidity']
    )


@app.get("/weather")  # response_model=weatherResponse)
def get_weather(city: str):
    data = fetch_weather(city, API_KEY, "metric")
    if data is None:
        raise HTTPException(status_code=404, detail="City not found")
    upload_to_db(city, data)
    return process_data(city, data)


# print(fetch_weather("Belfast" , API_KEY, "metric"))

def data_format(city, data):
    data = process_data(city, data)
    data_city = data.city
    data_avg_temp = data.avg_temp
    data_max_temp = data.max_temp
    data_min_temp = data.min_temp
    data_humidity = data.avg_humidity
    data_submit = [data_city, data_avg_temp, data_max_temp, data_min_temp, data_humidity]
    # print(data_submit)

    return data_submit


def upload_to_db(city, data):
    con = sqlite3.connect("weather_app.db")
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS city_data(city_name UNIQUE, avg_temp, max_temp, min_temp, avg_humidity)")
    cur.execute("INSERT OR REPLACE INTO city_data VALUES(?, ?, ?, ?, ?)", data_format(city, data))
    con.commit()
    con.close()


# Seeing if database is working

con = sqlite3.connect("weather_app.db", timeout=10)
cur = con.cursor()
res = cur.execute("SELECT * FROM city_data")
print(res.fetchall())

# uvicorn main:app --reload in the terminal
