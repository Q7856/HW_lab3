from unittest.mock import patch
from hypothesis import given, strategies as st
import random
from time import sleep
from main import another_city

# 模拟 get_coordinates_geocode_xyz
def mock_get_coordinates_geocode_xyz(city):
    """
    模拟地理编码服务，返回随机地理坐标或 None。
    """
    if random.random() > 0.3:  # 70% 几率返回有效坐标
        return {
            "city": city,
            "country": "MockCountry",
            "lat": random.uniform(-90, 90),
            "lon": random.uniform(-180, 180)
        }
    return None  # 30% 几率返回 None

# 模拟 Location 和 WeatherData 类
class Location:
    def __init__(self, city, country, lat, lon):
        self.city = city
        self.country = country
        self.lat = lat
        self.lon = lon

class WeatherData:
    def __init__(self, location):
        self.location = location

    def print(self):
        print(f"Weather data for {self.location.city}, {self.location.country}")

@given(city_input=st.text(alphabet="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ ", min_size=0, max_size=50))
@patch('main.get_coordinates_geocode_xyz', side_effect=mock_get_coordinates_geocode_xyz)
@patch('main.Location', side_effect=Location)
@patch('main.WeatherData', side_effect=WeatherData)
def test_another_city(mock_get_coordinates, Location, WeatherData,city_input):
    """
    对 `another_city` 函数进行模糊测试。
    """
    result = another_city(city_input)

    # 验证逻辑
    if city_input.strip() == "":
        # 空输入应该返回 None
        assert result is None, f"Expected None for empty input, got {result}"
    else:
        # 非空输入结果应为 True 或 None
        assert result in [True, None], f"Unexpected result {result} for input {city_input}"
