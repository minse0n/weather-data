import os
from datetime import datetime
from fastapi import FastAPI
from dotenv import load_dotenv
from apscheduler.schedulers.background import BackgroundScheduler

from database import WeatherRepository
from service import WeatherService

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")
TARGET_CITY = os.getenv("TARGET_CITY", "Bremen")
INTERVAL = int(os.getenv("INTERVAL_MINUTES", 30))

if not API_KEY:
    print("Error: API Key is missing in .env file.")
    exit(1)

app = FastAPI(title="Weather Data App")
db_repo = WeatherRepository()
weather_service = WeatherService(API_KEY)

def job_fetch_and_store():

    print(f"🔄 [{datetime.now().strftime('%H:%M:%S')}] Fetching weather for {TARGET_CITY}...")
    
    weather_data = weather_service.fetch_current_weather(TARGET_CITY)
    
    if weather_data:
        db_repo.save(
            city=weather_data["city"], 
            temp=weather_data["temp"], 
            humidity=weather_data["humidity"]
        )
        print(f"Saved: {weather_data['city']} | {weather_data['temp']}°C | Hum: {weather_data['humidity']}%")
    else:
        print("Failed to fetch or save data.")

@app.on_event("startup")
def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(job_fetch_and_store, 'interval', minutes=INTERVAL)
    scheduler.start()
    
    print(f"Application Started.")
    print(f"Target City: {TARGET_CITY}")
    print(f"Interval: {INTERVAL} minutes")

    job_fetch_and_store()

@app.get("/")
def root():
    return {"message": "Weather Data Service is Running"}

@app.get("/history")
def get_history(limit: int = 50):
    rows = db_repo.get_all(limit=limit)
    return {
        "count": len(rows),
        "limit": limit,
        "data": rows
    }