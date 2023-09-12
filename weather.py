import tkinter as tk
import requests 
import time
import datetime
from appdirs import AppDirs
import os
import json

# Simple desktop application made to track weather in a few locations as provided by the user
# Utilizes tkinter as the main framework. Intended to track just three locations by default

class displayCityWeather():
    def __init__(self,city,applet):
        self.cityname=city
        self.weatherData = ""

        self.cityLabel = tk.Label(applet,text=f"{city}")
        self.cityLabel.pack()

        self.condition = tk.Label(applet)
        self.condition.pack()

        self.weather = tk.Label(applet)
        self.weather.pack()

    def getWeather(self):
        
        api = "https://api.openweathermap.org/data/2.5/weather?q="+self.cityname+"&appid="+api_key
        json_city_data = requests.get(api).json()
        self.extractWeather(json_city_data)

    def extractWeather(self,data):#,pars):

        condition = data['weather'][0]['main']
        temp = int(data['main']['temp'] - 273.15)
        min_temp = int(data['main']['temp_min'] - 273.15)
        max_temp = int(data['main']['temp_max'] - 273.15)
        pressure = data['main']['pressure']
        humidity = data['main']['humidity']
        wind = data['wind']['speed']
        sunrise = time.strftime('%I:%M:%S', time.gmtime(data['sys']['sunrise']))# - 21600))
        sunset = time.strftime('%I:%M:%S', time.gmtime(data['sys']['sunset']))# - 21600))

        final_info = condition + "\n" + str(temp) + "°C" 
        final_data = "\n"+ "Min Temp: " + str(min_temp) + "°C" + "\n" + "Max Temp: " + str(max_temp) + "°C" +"\n" + "Pressure: " + str(pressure) + "\n" +"Humidity: " + str(humidity) + "\n" + "Wind Speed: " + str(wind) + "\n" + "Sunrise: " + sunrise + "\n" + "Sunset: " + sunset + "\n"

        self.condition.configure(text=final_info)
        self.weather.configure(text=final_data)

# Global API key for OpenWeather
api_key = "822be8f00df6e04cba9aca715e331cc3"

# List of all potential weather parameters
weather_pars = [
    "temp",
    "min_temp",
    "max_temp",
    "pressure",
    "humidity",
    "wind",
    "sunrise",
    "sunset"
]

def value(t):
    x = t.get('1.0','end-1c')
    return x

def getCity(*event):
    city=value(cityEntry)
    cities.append(city)

def update_clock():
    # Get current clock time
    current_time = datetime.datetime.now().strftime("Time: %H:%M:%S")

    # And update on the app
    timelabel.config(text=current_time)

    # run again every 1000 ms
    applet.after(1000,update_clock)

def update_weather():

    print(cities)

    for city in cities:
        if city in displayed:
            continue
        cityWeather = displayCityWeather(city,applet)
        cityWeather.getWeather()
        displayed.append(city)
        weathers.append(cityWeather)

    # run again every 1000 ms
    applet.after(1000,update_clock)
    applet.after(5000,update_weather)

# def refresh_app():

global cities
global displayed
global weathers

cities = []
displayed = []
weathers = []

config_filename = "appdata.json"

# Define app data locations
dirs = AppDirs("dch_weather","hermda02")

applet = tk.Tk()
applet.geometry("800x600")
applet.title("DCH Weather App")



timelabel = tk.Label(applet)
timelabel.pack()

cityEntry = tk.Text(applet, height=1,width=12)
cityEntry.focus()
cityEntry.pack()
cityEntry.bind('<Return>',getCity)

addButton = tk.Button(applet,text="Add",command=getCity).pack()


update_weather()

display_locations = []

applet.mainloop()