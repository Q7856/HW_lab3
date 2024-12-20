import random
import requests
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
        weather_data = get_weather_by_city(self.loc.lat,self.loc.lon)
        self.time = get_date_time()
        self.temparature = float(weather_data["temperature"])
        self.windspeed = float(weather_data["windspeed"])
        self.weather_code = int(weather_data["weather_code"])
        self.date = "{}/{}/{}".format(self.time[0], self.time[1], self.time[2])
        self.time = "{}:{}:{}".format(self.time[3], self.time[4], self.time[5])

    def print(self):
        print("")
        print("日期 : {}".format(self.date))
        print("时间 : {}".format(self.time))
        print("温度 : {}°C".format(self.temparature))
        print("风速 : {}km/h".format(self.windspeed))
        if self.weather_code in weather_type.keys():
            print("天气 : {}".format(weather_type[self.weather_code]))
        else:
            print("天气 : -")
        print("地点 : {}, {}".format(self.loc.city,self.loc.country))
        print("")

    def update(self):
        #检查当前设备位置是否有更新
        new_loc = Location()
        if new_loc.city != self.loc.city:
            self.loc = new_loc
        
        #检查最新时间过去了多久，超过15分钟重新获取weather
        new_time =  get_date_time()
        if (new_time[0] == self.time[0]) and (new_time[1] == self.time[1]) and (new_time[2] == self.time[2]) and (new_time[3] == self.time[3]) and (new_time[4] == self.time[4]):
            if (new_time[5] - self.time[5]) > 15:
                weather_data = get_weather_by_city(self.loc.lat,self.loc.lon)
                self.temparature = float(weather_data["temperature"])
                self.windspeed = float(weather_data["windspeed"])
                self.weather_code = int(weather_data["weather_code"])
        else:
            weather_data = get_weather_by_city(self.loc.lat,self.loc.lon)
            self.temparature = float(weather_data["temperature"])
            self.windspeed = float(weather_data["windspeed"])
            self.weather_code = int(weather_data["weather_code"])

        self.time = get_date_time()
        self.date = "{}/{}/{}".format(self.time[0], self.time[1], self.time[2])
        self.time = "{}:{}:{}".format(self.time[3], self.time[4], self.time[5])

#位置
class Location:
    """city country lat lon
    
    """
    def __init__(self, city = None, country = None):
        if (city == None) and (country == None):
            loc = get_location()
            city = loc["city"]
            country = loc["country"]
        self.city = city
        self.country = country
        self.lat = loc["lat"]
        self.lon = loc["lon"]


def get_date_time():
    "获取现在时间"
    now = datetime.now()
    time_list = [now.year, now.month, now.day, now.hour, now.minute, now.second]
    return time_list


def get_location():
    """
    获取位置
    成功返回 {"city":city, "country":country, "lat":lat, "lon":lon}
    """
    try:
        response = requests.get("http://ip-api.com/json")
        if response.status_code == 200:
            data = response.json()
            city = data.get("city", "Unknown City")
            country = data.get("country", "Unknown Country")
            lat = data.get("lat", "Unknown Lat")
            lon = data.get("lon", "Unkonown Lon")
            return {"city":city, "country":country, "lat":lat, "lon":lon}
        else:
            print("Unable to fetch location data")
    except Exception as e:
        print(f"An error occured: {e}")

def get_weather_by_city(lat,lon):
    """
        通过 lat lon 获取天气
        成功返回 {"temperature":temparature,"windspeed":windspeed,"weather_code":weather_code}
    """
    url = f"http://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            temparature = data["current_weather"]["temperature"]
            windspeed = data["current_weather"]["windspeed"]
            weather_code = data["current_weather"]["weathercode"]
            return {"temperature":temparature,"windspeed":windspeed,"weather_code":weather_code}
        else:
            return "Error: Unable to fetch weather data"
    except Exception as e:
        return f"Error: {e}"

def another_city():
    city = input("Select the city you want to view: ")


def TEST():
    r = random.randint(0,10)
    return r


if __name__ == "__main__":
    WD = WeatherData()
    while True:
        WD.print()
        select = input("Please select a num: \n1-exit  2-renew 3-other_place:  ")
        if select == "1" :
            break
        elif select == "2" :
            WD.update()
        elif select == "3":
            another_city()
