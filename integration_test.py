import unittest
from unittest.mock import patch
import requests
from main import get_weather_by_city, get_location

class TestIntegration(unittest.TestCase):
    @patch("requests.get")
    def test_integration_full_success(self, mock_get):
        """
        测试 get_location 和 get_weather_by_city 的完全成功集成场景
        """
        # Mock `get_location`
        mock_get.side_effect = [
            unittest.mock.Mock(
                status_code=200,
                json=lambda: {
                    "city": "Sample City",
                    "country": "Sample Country",
                    "lat": 12.34,
                    "lon": 56.78
                }
            ),
            unittest.mock.Mock(
                status_code=200,
                json=lambda: {
                    "current_weather": {
                        "temperature": 25.0,
                        "windspeed": 15.0,
                        "weathercode": 3
                    }
                }
            )
        ]

        # Integration test
        location = get_location()
        self.assertEqual(location, {
            "city": "Sample City",
            "country": "Sample Country",
            "lat": 12.34,
            "lon": 56.78
        })

        weather = get_weather_by_city(location["lat"], location["lon"])
        self.assertEqual(weather, {
            "temperature": 25.0,
            "windspeed": 15.0,
            "weather_code": 3
        })

    @patch("requests.get")
    def test_integration_location_failure(self, mock_get):
        """
        测试 get_location 失败的场景，确保对后续逻辑无影响
        """
        # Mock `get_location` failure
        mock_get.side_effect = [
            unittest.mock.Mock(status_code=404),
        ]

        # Integration test
        location = get_location()
        self.assertIsNone(location, "Location should be None on failure")

        # Skipping the call to get_weather_by_city since location failed
        # Integration success criteria: No further processing happens

    @patch("requests.get")
    def test_integration_partial_success(self, mock_get):
        """
        测试 get_location 成功但 get_weather_by_city 部分失败的场景
        """
        # Mock `get_location` success
        mock_get.side_effect = [
            unittest.mock.Mock(
                status_code=200,
                json=lambda: {
                    "city": "Sample City",
                    "country": "Sample Country",
                    "lat": 12.34,
                    "lon": 56.78
                }
            ),
            unittest.mock.Mock(status_code=500)  # Mock `get_weather_by_city` failure
        ]

        # Integration test
        location = get_location()
        self.assertEqual(location, {
            "city": "Sample City",
            "country": "Sample Country",
            "lat": 12.34,
            "lon": 56.78
        })

        weather = get_weather_by_city(location["lat"], location["lon"])
        self.assertEqual(weather, "Error: Unable to fetch weather data")

if __name__ == "__main__":
    unittest.main()
