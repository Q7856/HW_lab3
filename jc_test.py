import unittest
from unittest.mock import patch
from main import (
    WeatherData, 
    Location, 
    get_location, 
    get_weather_by_city, 
    get_date_time, 
    another_city
)

class TestWeatherTool(unittest.TestCase):
    # 测试底层模块
    @patch("main.requests.get")
    def test_get_location(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "city": "Test City",
            "country": "Test Country",
            "lat": 40.7128,
            "lon": -74.0060
        }
        location = get_location()
        self.assertEqual(location["city"], "Test City")
        self.assertEqual(location["country"], "Test Country")
        self.assertEqual(location["lat"], 40.7128)
        self.assertEqual(location["lon"], -74.0060)

    @patch("main.requests.get")
    def test_get_weather_by_city(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "current_weather": {
                "temperature": 25.0,
                "windspeed": 10.0,
                "weathercode": 1
            }
        }
        weather = get_weather_by_city(40.7128, -74.0060)
        self.assertEqual(weather["temperature"], 25.0)
        self.assertEqual(weather["windspeed"], 10.0)
        self.assertEqual(weather["weather_code"], 1)

    def test_get_date_time(self):
        now = get_date_time()
        self.assertEqual(len(now), 6)
        self.assertIsInstance(now[0], int)  # year
        self.assertIsInstance(now[1], int)  # month

    # 集成测试：WeatherData类
    @patch("main.get_location")
    @patch("main.get_weather_by_city")
    def test_weather_data(self, mock_weather, mock_location):
        mock_location.return_value = {
            "city": "Test City",
            "country": "Test Country",
            "lat": 40.7128,
            "lon": -74.0060
        }
        mock_weather.return_value = {
            "temperature": 25.0,
            "windspeed": 10.0,
            "weather_code": 1
        }
        wd = WeatherData()
        self.assertEqual(wd.temparature, 25.0)
        self.assertEqual(wd.windspeed, 10.0)
        self.assertEqual(wd.weather_code, 1)
        self.assertEqual(wd.loc.city, "Test City")

    # 集成测试：another_city函数
    @patch("main.get_coordinates_geocode_xyz")
    @patch("main.get_weather_by_city")
    def test_another_city(self, mock_weather, mock_coordinates):
        mock_coordinates.return_value = {
            "lat": 40.7128,
            "lon": -74.0060,
            "city": "Another City",
            "country": "Another Country"
        }
        mock_weather.return_value = {
            "temperature": 18.0,
            "windspeed": 5.0,
            "weather_code": 3
        }
        with patch("builtins.input", side_effect=["Another City", "1"]):
            result = another_city()
            self.assertTrue(result)

if __name__ == "__main__":
    unittest.main()