import unittest
from unittest.mock import patch
import requests
from main import get_weather_by_city
from main import get_location

class TestGetWeatherByCity(unittest.TestCase):

    @patch("requests.get")
    def test_successful_request_full_data(self, mock_get):
        """测试完整数据返回的情况"""
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "current_weather": {
                "temperature": 25.0,
                "windspeed": 15.0,
                "weathercode": 3
            }
        }
        result = get_weather_by_city(12.34, 56.78)
        self.assertEqual(result, {
            "temperature": 25.0,
            "windspeed": 15.0,
            "weather_code": 3
        })

    @patch("requests.get")
    def test_missing_temperature(self, mock_get):
        """测试缺少 temperature 字段的情况"""
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "current_weather": {
                "windspeed": 15.0,
                "weathercode": 3
            }
        }
        self.assertEqual(f"Error: 'temperature'", get_weather_by_city(12.34, 56.78))

    @patch("requests.get")
    def test_missing_windspeed(self, mock_get):
        """测试缺少 windspeed 字段的情况"""
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "current_weather": {
                "temperature": 25.0,
                "weathercode": 3
            }
        }
        self.assertEqual(f"Error: 'windspeed'", get_weather_by_city(12.34, 56.78))

    @patch("requests.get")
    def test_missing_weathercode(self, mock_get):
        """测试缺少 weathercode 字段的情况"""
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "current_weather": {
                "temperature": 25.0,
                "windspeed": 15.0
            }
        }
        self.assertEqual(f"Error: 'weathercode'", get_weather_by_city(12.34, 56.78))

    @patch("requests.get")
    def test_status_code_not_200(self, mock_get):
        """测试请求返回状态码非 200 的情况"""
        mock_get.return_value.status_code = 404
        result = get_weather_by_city(12.34, 56.78)
        self.assertEqual(result, "Error: Unable to fetch weather data")

    @patch("requests.get")
    def test_timeout_error(self, mock_get):
        """测试超时异常的情况"""
        mock_get.side_effect = requests.exceptions.Timeout
        result = get_weather_by_city(12.34, 56.78)
        self.assertTrue("Error:" in result)

    @patch("requests.get")
    def test_connection_error(self, mock_get):
        """测试连接错误的情况"""
        mock_get.side_effect = requests.exceptions.ConnectionError
        result = get_weather_by_city(12.34, 56.78)
        self.assertTrue("Error:" in result)

    @patch("requests.get")
    def test_invalid_json(self, mock_get):
        """测试返回无效 JSON 数据的情况"""
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.side_effect = ValueError
        result = get_weather_by_city(12.34, 56.78)
        self.assertTrue("Error:" in result)

    @patch("requests.get")
    def test_empty_json(self, mock_get):
        """测试返回空 JSON 数据的情况"""
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {}
        result = get_weather_by_city(12.34, 56.78)
        self.assertTrue("Error:" in result)

    @patch("requests.get")
    def test_partial_successful_data(self, mock_get):
        """测试部分数据返回，字段不完整但 status_code 成功的情况"""
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "current_weather": {
                "temperature": 22.0
            }
        }
        result = get_weather_by_city(12.34, 56.78)
        self.assertTrue("Error:" in result)

class TestGetLocation(unittest.TestCase):

    @patch("requests.get")
    def test_successful_request_full_data(self, mock_get):
        """测试完整数据返回的情况"""
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "city": "Sample City",
            "country": "Sample Country",
            "lat": 12.34,
            "lon": 56.78
        }
        result = get_location()
        self.assertEqual(result, {
            "city": "Sample City",
            "country": "Sample Country",
            "lat": 12.34,
            "lon": 56.78
        })

    @patch("requests.get")
    def test_missing_city(self, mock_get):
        """测试缺少 city 字段的情况"""
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "country": "Sample Country",
            "lat": 12.34,
            "lon": 56.78
        }
        result = get_location()
        self.assertEqual(result["city"], "Unknown City")

    @patch("requests.get")
    def test_missing_lat(self, mock_get):
        """测试缺少 lat 字段的情况"""
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "city": "Sample City",
            "country": "Sample Country",
            "lon": 56.78
        }
        result = get_location()
        self.assertEqual(result["lat"], "Unknown Lat")

    @patch("requests.get")
    def test_missing_lon(self, mock_get):
        """测试缺少 lon 字段的情况"""
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "city": "Sample City",
            "country": "Sample Country",
            "lat": 12.34
        }
        result = get_location()
        self.assertEqual(result["lon"], "Unknown Lon")

    @patch("requests.get")
    def test_status_code_not_200(self, mock_get):
        """测试请求返回状态码非 200 的情况"""
        mock_get.return_value.status_code = 404
        result = get_location()
        self.assertIsNone(result)

    @patch("requests.get")
    def test_timeout_error(self, mock_get):
        """测试超时异常的情况"""
        mock_get.side_effect = requests.exceptions.Timeout
        result = get_location()
        self.assertIsNone(result)

    @patch("requests.get")
    def test_connection_error(self, mock_get):
        """测试连接错误的情况"""
        mock_get.side_effect = requests.exceptions.ConnectionError
        result = get_location()
        self.assertIsNone(result)

    @patch("requests.get")
    def test_invalid_json(self, mock_get):
        """测试无效 JSON 数据的情况"""
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.side_effect = ValueError
        result = get_location()
        self.assertIsNone(result)

    @patch("requests.get")
    def test_empty_json(self, mock_get):
        """测试返回空 JSON 数据的情况"""
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {}
        result = get_location()
        self.assertEqual(result, {
            "city": "Unknown City",
            "country": "Unknown Country",
            "lat": "Unknown Lat",
            "lon": "Unknown Lon"
        })

    @patch("requests.get")
    def test_partial_successful_data(self, mock_get):
        """测试部分数据缺失，但状态码成功的情况"""
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "city": "Sample City"
        }
        result = get_location()
        self.assertEqual(result, {
            "city": "Sample City",
            "country": "Unknown Country",
            "lat": "Unknown Lat",
            "lon": "Unknown Lon"
        })

if __name__ == "__main__":
    unittest.main()
