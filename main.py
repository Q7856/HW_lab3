import requests
from time import sleep
from datetime import datetime


weather_type = {0:"晴",
                1:"晴", 2:"多云", 3:"阴天",
                45:"雾", 48:"沉积雾凇",
                51:"小雨", 53:"中雨", 55:"大雨",
                56:"冻雨", 57:"冻雨",
                61:"小雨", 63:"中雨", 65:"大雨",
                66:"冻雨-强度轻", 67:"冻雨-强度大",
                71:"小雪", 73:"中雪", 75:"大雪",
                77:"雪粒",
                80:"小雨", 81:"中雨", 82:"强降雨",
                85:"小雪", 86:"大雪",
    }

#当下时间的天气
class WeatherData:
    def __init__(self, loc = None):
        if loc == None:
            loc = Location()
        self.loc = loc
        weather_data = {"temperature":"-","windspeed":"-","weather_code":"-"}
        if self.loc.status == True:
            weather_data = get_weather_by_city(self.loc.lat,self.loc.lon)
        self.weather_status = weather_data.get("status",False)
        if self.weather_status :
            self.temparature = float(weather_data["temperature"])
            self.windspeed = float(weather_data["windspeed"])
            self.weather_code = int(weather_data["weather_code"])
        else:
            self.temparature = "-"
            self.windspeed = "-"
            self.weather_code = "-"

        self.time = get_date_time()
        self.date = f"{self.time[0]}/{self.time[1]}/{self.time[2]}"
        self.time = f"{self.time[3]}:{self.time[4]}:{self.time[5]}"

    def print(self):
        """print"""
        if(self.weather_status == False):
            print("Failed to get Weather Data")
        print("")
        print(f"日期 : {self.date}")
        print(f"时间 : {self.time}")
        print(f"温度 : {self.temparature}°C")
        print(f"风速 : {self.windspeed}km/h")
        if self.weather_code in weather_type.keys():
            print(f"天气 : {weather_type[self.weather_code]}")
        else:
            print("天气 : -")
        print(f"地点 : {self.loc.city}, {self.loc.country}")
        print("")

    def update(self):
        """update"""
        #检查当前设备位置是否有更新
        new_loc = Location()
        if new_loc.city != self.loc.city:
            self.loc = new_loc
        #检查最新时间过去了多久，超过15分钟重新获取weather
        new_time =  get_date_time()
        if (new_time[0] == self.time[0]) and (new_time[1] == self.time[1]) and (new_time[2] == self.time[2]) and (new_time[3] == self.time[3]) and (new_time[4] == self.time[4]):
            if (new_time[5] - self.time[5]) > 15:
                weather_data = get_weather_by_city(self.loc.lat,self.loc.lon)
                self.weather_status = weather_data.get("status",False)
                if self.weather_status:
                    self.temparature = float(weather_data["temperature"])
                    self.windspeed = float(weather_data["windspeed"])
                    self.weather_code = int(weather_data["weather_code"])
                else:
                    self.temparature = "-"
                    self.windspeed = "-"
                    self.weather_code = "-"
        else:
            weather_data = get_weather_by_city(self.loc.lat,self.loc.lon)
            self.weather_status = weather_data.get("status",False)
            if self.weather_status:
                self.temparature = float(weather_data["temperature"])
                self.windspeed = float(weather_data["windspeed"])
                self.weather_code = int(weather_data["weather_code"])
            else:
                self.temparature = "-"
                self.windspeed = "-"
                self.weather_code = "-"

        self.time = get_date_time()
        self.date = f"{self.time[0]}/{self.time[1]}/{self.time[2]}"
        self.time = f"{self.time[3]}:{self.time[4]}:{self.time[5]}"

#位置
class Location:
    """city country lat lon
    
    """
    def __init__(self, city = None, country = None, lat = None, lon = None,status = True):
        if (city is None) and (country is None):
            loc = get_location()
            if loc == None:
                city = None
                country = None
                lat = None
                lon = None
                status = False
            else:
                city = loc["city"]
                country = loc["country"]
                lat = loc["lat"]
                lon = loc["lon"]
        self.city = city
        self.country = country
        self.lat = lat
        self.lon = lon
        self.status = status


def get_date_time():
    "获取现在时间"
    now = datetime.now()
    time_list = [now.year, now.month, now.day, now.hour, now.minute, now.second]
    return time_list


def get_location():
    """
    获取本地位置
    成功返回 {"city":city, "country":country, "lat":lat, "lon":lon}
    """
    try:
        response = requests.get("http://ip-api.com/json", timeout = 5)
        if response.status_code == 200:
            data = response.json()
            city = data.get("city", "Unknown City")
            country = data.get("country", "Unknown Country")
            lat = data.get("lat", "Unknown Lat")
            lon = data.get("lon", "Unknown Lon")
            return {"city":city, "country":country, "lat":lat, "lon":lon}
        else:
            print("Unable to fetch location data")
            return None
    except Exception as e:
        #print(f"An error occured: {e}")
        return None

def get_weather_by_city(lat,lon):
    """
        通过 lat lon 获取天气
        成功返回 {"temperature":temparature,"windspeed":windspeed,"weather_code":weather_code}
    """
    url = f"http://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    try:
        response = requests.get(url, timeout = 5)
        if response.status_code == 200:
            data = response.json()
            temparature = data["current_weather"]["temperature"]
            windspeed = data["current_weather"]["windspeed"]
            weather_code = data["current_weather"]["weathercode"]
            return {"temperature":temparature,"windspeed":windspeed,"weather_code":weather_code, "status":True}
        else:
            return {"temperature":None,"windspeed":None,"weather_code":None}
    except Exception as e:
        return {"temperature":None,"windspeed":None,"weather_code":None}

def get_coordinates_geocode_xyz(city):
    if city == "":
        return None
    url = f"http://geocode.xyz/{city}?json=1"
    try:
        response = requests.get(url,timeout = 5)
        if response.status_code == 200:
            data = response.json()
            if "latt" in data and "longt" in data:
                lat = float(data["latt"])
                lon = float(data["longt"])
                city = data["standard"]["city"]
                country = data["standard"]["countryname"]
                return {"lat":lat, "lon":lon, "city":city, "country":country}
            else:
                #print(f"Error: No data found for {city}")
                return None
        else:
            #print(f"Error: Unable to fetch data. Status code: {response.status_code}")
            return None
    except Exception as e:
        #print(f"An error occured: {e}")
        return None


def another_city(city):
    if city == "":
        return None
    times = 5
    loc = get_coordinates_geocode_xyz(city)
    while loc is None and times > 0:
        loc = get_coordinates_geocode_xyz(city)
        times-=1
        sleep(2)
    if loc is None:
        return None
    location = Location(loc["city"], loc["country"], loc["lat"], loc["lon"])
    others_weather = WeatherData(location)
    others_weather.print()
    del others_weather
    return True

if __name__ == "__main__":
    WD = WeatherData()
    WD.print()
    while True:
        select = input("Please select a num: \n1-exit  2-renew 3-other_place:  ")
        if select == "1" :
            break
        elif select == "2" :
            WD.update()
            WD.print()
        elif select == "3":
            city = input("\nSelect the city you want to view: ")
            if another_city(city) == None:
                print(f"\nFailed to get WeatherData of {city}, Please try again later\n")
