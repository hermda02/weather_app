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
    def __init__(self,city,bottom_frame,row):
        self.cityname=city
        self.weatherData = ""

        self.cityLabel = tk.Label(bottom_frame,text=f"{city}")
        self.cityLabel.grid(row=row, column=0)

        self.condition = tk.Label(bottom_frame)
        self.condition.grid(row=row, column=1)

        self.weather = tk.Label(bottom_frame)
        self.weather.grid(row=row, column=2)

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
        timezone = data['timezone']
        local_time = time.strftime('%H:%M:%S', time.gmtime(data['dt'] + int(timezone)))
        sunrise = time.strftime('%H:%M:%S', time.gmtime(data['sys']['sunrise'] + int(timezone)))
        sunset = time.strftime('%H:%M:%S', time.gmtime(data['sys']['sunset'] + int(timezone)))

        final_info = "Local Time: " + local_time + "\n" + condition + "\n" + str(temp) + "°C" 
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
    "sunset",
    "timezone"
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

    wnum = 1

    # Loop through cities to add weather info
    for city in cities:
        # If we already have the info, skip the city
        if city in displayed:
            continue
        # Else initialize
        else:
            wnum += 1
            cityWeather = displayCityWeather(city,applet,wnum)
            weathers.append(cityWeather)
            displayed.append(city)
        cityWeather.getWeather()

    # run again every 1000 ms
    applet.after(1000,update_clock)
    applet.after(5000,update_weather)


# Global lists
global cities
global displayed
global weathers
global wnum # number of weather locations (used for grid location)

cities = []#"Oslo", "Johannesburg"]
displayed = []
weathers = []

# Initialize wnum
# wnum = 2

# Define app data locations and config file name
dirs = AppDirs("dch_weather","hermda02")
config_filename = "appdata.json"

# Initialize
applet = tk.Tk()
applet.maxsize(800,600)
applet.title("DCH Weather App")
applet.config(bg='black')

# Create frame for general info
top_frame = tk.Frame(applet, width=600, height=100, bg='white')
top_frame.grid(row=0, columnspan=3, padx=10, pady=5)
tk.Label(top_frame,text="General Info").grid(row=0, column=0, padx=5, pady=5)

middle_frame = tk.Frame(applet,width=600,height=50,bg='grey')
middle_frame.grid(row=1, columnspan=3, padx=10, pady=5)
tk.Label(middle_frame,text="Weather").grid(row=0, column=0, padx=5, pady=5)

# Create frame for weather info
bottom_frame = tk.Frame(applet, width=600, height=500, bg='grey')
bottom_frame.grid(row=2, rowspan=3, columnspan=3, padx=10, pady=5)
bottom_frame.grid_columnconfigure((0,1,2), weight=1, uniform="column")
bottom_frame.grid_rowconfigure((1,2,3), weight=1, uniform="row")


# Frame for the time info
time_frame = tk.Frame(top_frame, width=200, height=100, bd=3)
time_frame.grid(row=0, column=0, padx=5, pady=5)

timelabel = tk.Label(time_frame)
timelabel.grid(row=0,column=0)

# Frame for the user input
entry_frame = tk.Frame(top_frame,width=600,height=100,bd=3)
entry_frame.grid(row=0,column=1)

# Define entry field and button
cityEntry = tk.Text(entry_frame, height=1,width=12)
# cityEntry.focus()
cityEntry.grid(row=0,column=2)
cityEntry.bind('<Return>',getCity)

addButton = tk.Button(top_frame,text="Add",justify='left',command=getCity)
addButton.grid(row=0,column=3)

# # Add Weather labels
cityLabel = tk.Label(bottom_frame, text="Location").grid(row=0, column=0, padx=5, pady=5)
currentLabel = tk.Label(bottom_frame, text="Current Weather").grid(row=0, column=1, padx=5, pady=5)
detailLabel = tk.Label(bottom_frame, text="Details").grid(row=0, column=2, padx=5, pady=5)

update_weather()

display_locations = []

applet.mainloop()