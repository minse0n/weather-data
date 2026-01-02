import requests

class WeatherService:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"

    def fetch_current_weather(self, city_name: str) -> dict:
        
        params = {
            "q": city_name,
            "appid": self.api_key,
            "units": "metric",
            "lang": "en"
        }
        
        try:
            response = requests.get(self.base_url, params=params, timeout=10)
            
            response.raise_for_status()
            
            data = response.json()

            return {
                "city": data["name"],
                "temp": data["main"]["temp"],
                "humidity": data["main"]["humidity"]
            }
            
        except requests.exceptions.RequestException as e:
            print(f"⚠️ API Communication Error: {e}")
            return None
        except KeyError as e:
            print(f"⚠️ API Data Parsing Error: Missing key {e}")
            return None