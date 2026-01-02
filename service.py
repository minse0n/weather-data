import requests

class WeatherService:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.openweathermap.org/data/3.0/onecall"

    def fetch_current_weather(self, lat: float, lon: float) -> dict:
        
        params = {
            "lat": lat,
            "lon": lon,
            "appid": self.api_key,
            "units": "metric",
            "exclude": "minutely,hourly,daily,alerts"
        }
        
        try:
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            return {
                "lat": data["lat"],
                "lon": data["lon"],
                "timezone": data["timezone"],
                "temp": data["current"]["temp"],
                "humidity": data["current"]["humidity"],
                "weather": data["current"]["weather"][0]["description"]
            }
            
        except requests.exceptions.RequestException as e:
            print(f"API Communication Error: {e}")
            return None
        except KeyError as e:
            print(f"API Data Parsing Error: Missing key {e}")
            return None