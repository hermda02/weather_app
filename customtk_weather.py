import customtkinter as Ctk
import requests 
from appdirs import AppDirs
import ipinfo
from geopy.geocoders import Nominatim
from PIL import Image
import os
import json
import pendulum
from timezonefinder import TimezoneFinder

# Simple desktop application made to track weather in a few locations as provided by the user
# Utilizes tkinter as the main framework. Intended to track just three locations by default

# Uses MET Weather API icons from: https://github.com/metno/weathericons/tree/main
# Copyright (c) 2015-2017 Yr

nmi_header = {'User-Agent': 'dcWeather/0.1 github.com/hermda02/weather_app'}

Ctk.set_appearance_mode('Dark')
Ctk.set_default_color_theme('blue')

class cityWeather():
    """Creates the instance for pulling down, storing, and displaying weather data"""
    def __init__(self, bottom_frame, city, row):
        """Initizalizes the weather class
        
        ...

        Attributes
        ----------
        cityname : str
            a string containing the name of the city
        lat : str
            latitude of the city
        lon : str
            longitude of the city
        tz : str
            timezone of the city
        weatherData : str
            json formatted weather data as retrieved from the NMI API
        nearbyImage : CTkLabel
            CTkLabel instance for nearby weather image
        nearbyLabel : CTkLabel
            CTkLabel instance for nearby location name
        nearbyWeather : CTkLabel
            CTkLabel instance for nearby temperature
        image : CTkLabel
            CTkLabel instance for chosen location weather image
        label : CTkLabel
            CTkLabel instance for chosen location name
        eeather : CTkLabel
            CTkLabel instance for chosen location temperature            

        Methods
        -------
        getWeather(flag=0)
            Pulls down the weather data from the API

        extractNMIWeather(flag=0)
            Parses and formats weather data. Places data into tkinter frame            
        """
        self.cityname = city['city']
        self.lat = str(city['latlon'][0])
        self.lon = str(city['latlon'][1])
        self.tz = str(city['timezone'])
        self.weatherData = ''
        local_time = now.in_tz(self.tz)

        if row < 0:
            self.nearbyLabel = Ctk.CTkLabel(top_frame,text=f'{self.cityname}',font=('Courier',44))
            self.nearbyLabel.grid(row=0,column=0)
            self.nearbyImage = Ctk.CTkLabel(top_frame,text='')
            self.nearbyImage.grid(row=0,column=1,rowspan=3)
            self.nearbyWeather = Ctk.CTkLabel(top_frame,font=('Courier',44))
            self.nearbyWeather.grid(row=1, rowspan=2, column=0)

        else:
            self.label = Ctk.CTkLabel(bottom_frame,text=f'{self.cityname} \n {local_time.format("HH:mm")}',font=('Courier',24),anchor='center')
            self.label.grid(row=row, column=0,sticky='E')
            self.image = Ctk.CTkLabel(bottom_frame,text='')
            self.image.grid(row=row, column=2)
            self.weather = Ctk.CTkLabel(bottom_frame, text='', font=('Courier',24))
            self.weather.grid(row=row, column=1)


    def getWeather(self,flag=0):
        ''' getWeather : self
        
        Function to call the API and pull down the data.

        Parameters
        ----------
        flag : int
            flag to determine if this is the local weather or a user added location

        '''
        
        api = 'https://api.met.no/weatherapi/locationforecast/2.0/complete?lat='+self.lat+'&lon='+self.lon
        self.weatherData = requests.get(api, headers=nmi_header).json()

    def extractNMIWeather(self,flag=0):
        ''' extractNMIWeather : self

        Function that parses the data and adjusts the labels in the widget
        
        Parameters
        ----------
        flag : int
            flag to determine if this is the local weather or a user added location

        '''

        units = self.weatherData['properties']['meta']['units']

        weather_now = self.weatherData['properties']['timeseries'][0]['data']['instant']['details']
        summary_now = self.weatherData['properties']['timeseries'][0]['data']['next_1_hours']
        weather_next_hour = self.weatherData['properties']['timeseries']
        
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

        final_info = str(temp) + '°C' 
        # final_data = '\n'+ 'Min Temp: ' + str(min_temp) + '°C' + '\n' + 'Max Temp: ' + str(max_temp) + '°C' +'\n' + 'Pressure: ' + str(pressure) + '\n' +'Humidity: ' + str(humidity) + '\n' + 'Wind Speed: ' + str(wind) #+ '\n' + 'Sunrise: ' + sunrise + ',' + 'Sunset: ' + sunset + '\n'
        if flag == 0:
            self.weather.configure(text=final_info)
            self.image.configure(image=image)
        else:
            self.nearbyWeather.configure(text=final_info)
            self.nearbyImage.configure(image=image)

def value(t):
    """ Returns the value from the text field
    
    Parameters
    ----------

    t : CTkTextbox
        The textbox class for customtkinter
    """
    x = t.get('1.0','end-1c')
    return x

def getCity(*event):
    """ 
    Parse the city from the user input and gather relevant information of weather data gathering
    Updates the city list, and calls the clock and weather update
    
    Parameters
    ----------
    event : event, optional
        Allows the function to be used by entering <return> in the text box
    
    """

    city_name=value(cityEntry)
    city_location = geolocator.geocode(city_name)
    city_lat = city_location.latitude
    city_lon = city_location.longitude
    city_tz = tz_obj.timezone_at(lat=float(city_lat), lng=float(city_lon))
    city = {
        'city': city_name,
        'latlon': [city_lat,city_lon],
        'timezone': city_tz
    }
    cities.append(city)
    cityEntry.delete('1.0', 'end')
    update_clock()
    update_weather()

def update_clock():
    """
    Returns the local time
    """
    # Get current clock time
    current_time = now.format('HH:mm')

    # And update on the app
    timelabel.configure(text=current_time)

    # run again every 1000 ms
    applet.after(1000,update_clock)

def update_weather():
    """
    Iterates through cities in the city list, pulling down any data from cities that have
    not yet had their data recovered. Creates the cityWeather object and uses its methods
    
    """

    wnum = 3

    # Loop through cities to add weather info
    for city in cities:
        # If we already have the info, skip the city
        if city in displayed:
            wnum += 1
            continue
        else:
            wnum += 1
            weather = cityWeather(applet,city,wnum)
            weathers.append(weather)
            displayed.append(city)
            weather.getWeather()
            weather.extractNMIWeather()

    # run again every 1000 ms
    applet.after(1000,update_clock)
   
def initAppData():
    """
    Defines the application data directories.
    Either reads the current application data or creates an empty list of cities.
    """
    # create appdata directories
    if not os.path.exists(dirs.user_data_dir):
        os.makedirs(dirs.user_data_dir)
    
    user_data = os.path.join(dirs.user_data_dir,config_filename)

    if os.path.isfile(user_data):
        with open(user_data, 'r') as infile:
            data = json.load(infile)
    else:
        data = []

    return data


def dumpAppData():
    """
    Takes the city data and dumps it to the application user data file
    """
    with open(os.path.join(dirs.user_data_dir,config_filename), 'w') as outfile:
        json.dump(cities, outfile)

if __name__ == '__main__':

    # List of all potential weather parameters
    weather_pars = [
        'temp',
        'min_temp',
        'max_temp',
        'pressure',
        'humidity',
        'wind',
        'sunrise',
        'sunset',
        'timezone'
    ]

    # Global lists
    global cities
    global displayed
    global weathers
    global now
    global wnum # number of weather locations (used for grid location)

    # API for ipinfo
    ipinfo_api_key = '9f9248602a99a3'

    # Define app data locations and config file name
    appname = 'dch_weather'
    appauthor = 'hermda02'
    dirs = AppDirs(appname, appauthor)
    config_filename = 'appdata.json'

    # Initialize data structures
    now = pendulum.now()
    tz_obj = TimezoneFinder()
    cities = initAppData()
    displayed = []
    weathers = []

    # Read the users IP address to find their city
    url = 'https://api.ipify.org'
    response = requests.get(url)
    user_ip = response.text

    handler = ipinfo.getHandler(ipinfo_api_key)
    details = handler.getDetails(user_ip)

    # Use lat-lon to get the city name
    lat_lon = [details.latitude,details.longitude]
    geolocator = Nominatim(user_agent='blah blah blah')
    location = geolocator.reverse(lat_lon).raw
    ipcity=location['address']['city']
    local_tz = now.tz.name

    # Save local city info as dict
    local_city = {
        'city': ipcity,
        'latlon': lat_lon,
        'timezone': local_tz
    }


    # Initialize
    applet = Ctk.CTk()
    applet.maxsize(800,600)
    applet.title('DCH Weather App')
    applet.configure(bg='black')

    # Create frame for local weather
    top_frame = Ctk.CTkFrame(applet, width=600, height=300)
    top_frame.grid(row=0, rowspan=3, columnspan=3, padx=10, pady=5)
    top_frame.grid_columnconfigure((0,1), weight=3, uniform='column')
    top_frame.grid_columnconfigure((2), weight=1, uniform='column')
    top_frame.grid_rowconfigure((0,1,2),weight=1,uniform='row')

    # Create frame for weather info
    bottom_frame = Ctk.CTkFrame(applet, width=800, height=200)
    bottom_frame.grid(row=4, rowspan=4, columnspan=3, padx=10, pady=5)
    bottom_frame.grid_columnconfigure((0,1,2), weight=1, uniform='column')
    bottom_frame.grid_rowconfigure((1,2,3), weight=1, uniform='row')
    bottom_frame.grid_propagate(False)

    # Frame for the time info
    time_frame = Ctk.CTkFrame(top_frame, width=200, height=100)
    time_frame.grid(row=0, column=3, padx=5, pady=5)

    timelabel = Ctk.CTkLabel(time_frame,font=('Courier',24),text='')
    timelabel.grid(row=0,column=0)

    # Frame for the user input
    entry_frame = Ctk.CTkFrame(applet, width=600, height=100)
    entry_frame.grid(row=8,column=1)

    # Define entry field and button
    cityEntry = Ctk.CTkTextbox(entry_frame, height=1, width=300)
    # cityEntry.focus()
    cityEntry.grid(row=0, column=0,columnspan=2)
    cityEntry.bind('<Return>', getCity)

    addButton = Ctk.CTkButton(entry_frame, text='Add', command=getCity)
    addButton.grid(row=0, column=3)

    localWeather = cityWeather(applet, local_city, -1)
    localWeather.getWeather(flag=1)
    localWeather.extractNMIWeather(flag=1)

    update_weather()

    display_locations = []

    applet.mainloop()

    dumpAppData()
