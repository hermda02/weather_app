import tkinter as tk
import requests 
import time
from appdirs import AppDirs
import os
import json

def getWeather(applet):
    api_key = "822be8f00df6e04cba9aca715e331cc3"
    city = textfield.get()
    # try:
    #     city, country = textfield.get()
    # except:
    #     print("Doesn't work")
    lon_lat_api = "http://api.openweathermap.org/geo/1.0/direct?q="+city+"&limit=5&appid="+api_key
    location_data = requests.get(lon_lat_api).json()
    lon = float(location_data[0]['lon'])
    lat = float(location_data[0]['lat'])
    api = "https://api.openweathermap.org/data/2.5/weather?q="+city+"&appid="+api_key
    json_data = requests.get(api).json()


    lon_lat_string = 'lon = '+ str(lon) + '\n lat = ' + str(lat)
    label1.config(text = lon_lat_string)

    api = "https://api.openweathermap.org/data/2.5/weather?q="+city+"&appid="+api_key
    json_data = requests.get(api).json()
    condition = json_data['weather'][0]['main']
    temp = int(json_data['main']['temp'] - 273.15)
    min_temp = int(json_data['main']['temp_min'] - 273.15)
    max_temp = int(json_data['main']['temp_max'] - 273.15)
    pressure = json_data['main']['pressure']
    humidity = json_data['main']['humidity']
    wind = json_data['wind']['speed']
    sunrise = time.strftime('%I:%M:%S', time.gmtime(json_data['sys']['sunrise']))# - 21600))
    sunset = time.strftime('%I:%M:%S', time.gmtime(json_data['sys']['sunset']))# - 21600))

    final_info = condition + "\n" + str(temp) + "°C" 
    final_data = "\n"+ "Min Temp: " + str(min_temp) + "°C" + "\n" + "Max Temp: " + str(max_temp) + "°C" +"\n" + "Pressure: " + str(pressure) + "\n" +"Humidity: " + str(humidity) + "\n" +"Wind Speed: " + str(wind) + "\n" + "Sunrise: " + sunrise + "\n" + "Sunset: " + sunset

    # return final_data

    # lon_lat_string = 'lon = '+ str(lon) + '\n lat = ' + str(lat)
    # label1.configure(text = lon_lat_string)
    label1.configure(text = final_info)
    label2.configure(text = final_data)

def addCity(cities,city):
    if city in cities:
        return
    else:
        cities.append(city)

applet = tk.Tk()
applet.geometry("800x600")
applet.title("DCH Weather App")

f = ("poppins", 15, "bold")
t = ("poppins", 35, "bold")

textfield = tk.Entry(applet, font=t)
textfield.pack(pady=20)#,side=tk.LEFT)
textfield.focus()
textfield.bind('<Return>',getWeather)

label1 = tk.Label(applet, font = t)
label1.pack(side=tk.LEFT)
label2 = tk.Label(applet, font = f)
label2.pack(side=tk.LEFT)

# Define app data locations
dirs = AppDirs("dch_weather","hermda02")

config_filename = "appdata.json"

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

cites = []

# Create dropdwn menu of things to display
display_menu = tk.OptionMenu(applet, *weather_pars)
display_menu.pack(side=tk.TOP)

# Weather parameters to be displayed
display_pars = ""

print(dirs.user_data_dir+'/'+config_filename)
print(os.path.isfile(dirs.user_data_dir+'/'+config_filename))

# if os.path.isfile(dirs.user_data_dir+'/'+config_filename):
#     config = 



display_locations = []

applet.mainloop()