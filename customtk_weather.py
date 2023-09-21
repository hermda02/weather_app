import customtkinter as Ctk
import tkinter as tk
import requests 
import datetime
from appdirs import AppDirs
import geocoder
from geopy.geocoders import Nominatim
from PIL import Image

# Simple desktop application made to track weather in a few locations as provided by the user
# Utilizes tkinter as the main framework. Intended to track just three locations by default

# Uses MET Weather API icons from: https://github.com/metno/weathericons/tree/main
# Copyright (c) 2015-2017 Yr

nmi_header = {'User-Agent': 'dcWeather/0.1 github.com/hermda02/weather_app'}

Ctk.set_appearance_mode("Dark")
Ctk.set_default_color_theme("blue")

class displayCityWeather():
    def __init__(self, bottom_frame, city, row):
        self.cityname=city["city"]
        self.lat=str(city["latlon"][0])
        self.lon=str(city["latlon"][1])
        self.weatherData = ""

        if row < 0:
            self.nearbyDisplay = Ctk.CTkLabel(top_frame,text=f"{self.cityname}",font=("Courier",44))
            self.nearbyDisplay.grid(row=0,column=0)
            self.nearbyImage = Ctk.CTkLabel(top_frame,text="")
            self.nearbyImage.grid(row=0,column=1,rowspan=3)
            self.nearbyWeather = Ctk.CTkLabel(top_frame,font=("Courier",44))
            self.nearbyWeather.grid(row=1, rowspan=2, column=0)

        else:
            self.cityLabel = Ctk.CTkLabel(bottom_frame,text=f"{self.cityname}",font=("Courier",24))
            self.cityLabel.grid(row=row, column=0)

            self.weather = Ctk.CTkLabel(bottom_frame, text="", font=("Courier",24))
            self.weather.grid(row=row, column=1)

            self.image = Ctk.CTkLabel(bottom_frame,text="")
            self.image.grid(row=row, column=2)

    def getWeather(self,flag=0):
        ''' getWeather : self
        
        Function to call the API and pull down the data

        '''
        
        api = "https://api.met.no/weatherapi/locationforecast/2.0/complete?lat="+self.lat+"&lon="+self.lon
        self.weatherData = requests.get(api, headers=nmi_header).json()
        # print(self.weatherData["properties"]["meta"]['updated_at'])
        self.extractNMIWeather(flag)

    def extractNMIWeather(self,flag=0):
        ''' extractNMIWeather : self

        Function that parses the data and adjusts the labels in the widget
        
        '''

        units = self.weatherData["properties"]["meta"]["units"]
        now = self.weatherData["properties"]["meta"]['updated_at']

        # print(units)
        weather_now = self.weatherData["properties"]["timeseries"][0]['data']['instant']['details']
        summary_now = self.weatherData["properties"]["timeseries"][0]['data']['next_1_hours']
        weather_next_hour = self.weatherData["properties"]["timeseries"]
        
        if flag == 0:
            image = Ctk.CTkImage(Image.open('png/'+summary_now['summary']['symbol_code']+'.png'),size=(100, 100))
        else:
            image = Ctk.CTkImage(Image.open('png/'+summary_now['summary']['symbol_code']+'.png'),size=(150, 150))

        temp = weather_now['air_temperature']
        # min_temp = weather_now['air_temperature_percentile_10']
        # max_temp = weather_now['air_temperature_percentile_90']
        # pressure = weather_now['air_pressure_at_sea_level']
        # humidity = weather_now['air_pressure_at_sea_level']
        # wind = weather_now['wind_speed']
        # timezone = data['timezone']
        # local_time = now#time.strftime('%H:%M:%S', time.gmtime(data['dt'] + int(timezone)))
        # sunrise = time.strftime('%H:%M:%S', time.gmtime(data['sys']['sunrise'] + int(timezone)))
        # sunset = time.strftime('%H:%M:%S', time.gmtime(data['sys']['sunset'] + int(timezone)))

        final_info = str(temp) + "°C" 
        # final_data = "\n"+ "Min Temp: " + str(min_temp) + "°C" + "\n" + "Max Temp: " + str(max_temp) + "°C" +"\n" + "Pressure: " + str(pressure) + "\n" +"Humidity: " + str(humidity) + "\n" + "Wind Speed: " + str(wind) #+ "\n" + "Sunrise: " + sunrise + "," + "Sunset: " + sunset + "\n"
        if flag == 0:
            self.weather.configure(text=final_info)
            self.image.configure(image=image)
            # self.weather.configure(text=final_data)
        else:
            self.nearbyWeather.configure(text=final_info)
            self.nearbyImage.configure(image=image)

def value(t):
    x = t.get('1.0','end-1c')
    return x

def getCity(*event):

    city_name=value(cityEntry)
    city_location = geolocator.geocode(city_name)
    city_lat = city_location.latitude
    city_lon = city_location.longitude
    city = {
        "city": city_name,
        "latlon": [city_lat,city_lon]
    }
    cities.append(city)
    cityEntry.delete("1.0", "end")
    update_clock()
    update_weather()

def update_clock():
    # Get current clock time
    current_time = datetime.datetime.now().strftime("Time: %H:%M")

    # And update on the app
    timelabel.configure(text=current_time)

    # run again every 1000 ms
    applet.after(1000,update_clock)

def update_weather():

    wnum = 3

    # Loop through cities to add weather info
    for city in cities:
        # If we already have the info, skip the city
        if city in displayed:
            wnum += 1
            continue
        else:
            wnum += 1
            cityWeather = displayCityWeather(applet,city,wnum)
            weathers.append(cityWeather)
            displayed.append(city)
            cityWeather.getWeather()

    # run again every 1000 ms
    applet.after(1000,update_clock)


if __name__ == "__main__":

    # Global API key for OpenWeather
    api_key = "822be8f00df6e04cba9aca715e331cc3"

    # Read the users IP address to find their city
    iploc = geocoder.ip('me')
    lat_lon = iploc.latlng
    geolocator = Nominatim(user_agent="blah blah blah")
    location = geolocator.reverse(lat_lon).raw
    ipcity=location['address']['city']

    # Save local city info as dict
    local_city = {
        "city": ipcity,
        "latlon": lat_lon
    }

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

    # Global lists
    global cities
    global displayed
    global weathers
    global wnum # number of weather locations (used for grid location)

    cities = []
    displayed = []
    weathers = []

    # Define app data locations and config file name
    dirs = AppDirs("dch_weather","hermda02")
    config_filename = "appdata.json"

    # Initialize
    applet = Ctk.CTk()
    applet.maxsize(800,600)
    applet.title("DCH Weather App")
    applet.configure(bg='black')
    # applet.config(bg='black')

    # Create frame for local weather
    top_frame = Ctk.CTkFrame(applet, width=600, height=300)
    top_frame.grid(row=0, rowspan=3, columnspan=3, padx=10, pady=5)
    top_frame.grid_columnconfigure((0,1), weight=3, uniform="column")
    top_frame.grid_columnconfigure((2), weight=1, uniform="column")
    top_frame.grid_rowconfigure((0,1,2),weight=1,uniform='row')

    # Create frame for weather info
    bottom_frame = Ctk.CTkFrame(applet, width=600, height=200)
    bottom_frame.grid(row=4, rowspan=4, columnspan=3, padx=10, pady=5)
    bottom_frame.grid_columnconfigure((0,1,2), weight=1, uniform="column")
    bottom_frame.grid_rowconfigure((1,2,3), weight=1, uniform="row")

    # Frame for the time info
    time_frame = Ctk.CTkFrame(top_frame, width=200, height=100)
    time_frame.grid(row=0, column=3, padx=5, pady=5)

    timelabel = Ctk.CTkLabel(time_frame,font=("Courier",24),text="")
    timelabel.grid(row=0,column=0)

    # Frame for the user input
    entry_frame = Ctk.CTkFrame(applet, width=600, height=100)
    entry_frame.grid(row=8,column=1)

    # Define entry field and button
    cityEntry = Ctk.CTkTextbox(entry_frame, height=1, width=300)
    # cityEntry.focus()
    cityEntry.grid(row=0, column=0,columnspan=2)
    cityEntry.bind('<Return>', getCity)

    addButton = Ctk.CTkButton(entry_frame, text="Add", command=getCity)
    addButton.grid(row=0, column=3)

    localWeather = displayCityWeather(applet, local_city, -1)
    localWeather.getWeather(flag=1)

    update_weather()

    display_locations = []

    applet.mainloop()

