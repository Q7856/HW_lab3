import random
from datetime import datetime

#当下时间
class WeatherData:
    def __init__(self):
        self.time = get_date_time()
        self.temparature = TEST()
        self.date = "{}/{}/{}".format(self.time[0], self.time[1], self.time[2])
        self.time = "{}:{}:{}".format(self.time[3], self.time[4], self.time[5])

    def print(self):
        print("日期 : {}".format(self.date))
        print("时间 : {}".format(self.time))
        print("温度 : {}°C".format(self.temparature))

    def update(self):
        self.time = get_date_time()
        self.temparature = TEST()
        self.date = "{}/{}/{}".format(self.time[0], self.time[1], self.time[2])
        self.time = "{}:{}:{}".format(self.time[3], self.time[4], self.time[5])

class Location:
    def __init__(self, ip):
        self.ip = ip

def get_date_time():
    now = datetime.now()
    time_list = [now.year, now.month, now.day, now.hour, now.minute, now.second]
    return time_list

def TEST():
    r = random.randint(0,10)
    return r

if __name__ == "__main__":
    info = TEST()
    WD = WeatherData()
    while True:
        WD.print()
        select = input("Please select a num: 1-exit 2-renew ")
        if select == "1" :
            break
        elif select == "2" :
            info = TEST()
            WD.update()
