import unittest
from unittest.mock import patch
import requests
from main import get_weather_by_city

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
        self.assertEqual(f"Error: 'temperature'",get_weather_by_city(12.34, 56.78))

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
        self.assertEqual(f"Error: 'windspeed'",get_weather_by_city(12.34, 56.78))

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
        self.assertEqual(f"Error: 'weathercode'",get_weather_by_city(12.34, 56.78))

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

if __name__ == "__main__":
    unittest.main()

