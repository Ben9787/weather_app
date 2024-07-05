import sqlite3
import main

con = sqlite3.connect("Weather_app.db")
cur = con.cursor()
city = main.
data = main.fetch_weather()
main_data = main.process_data(city,data)