import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from apscheduler.schedulers.background import BackgroundScheduler
from dotenv import load_dotenv

from database import WeatherRepository
from service import WeatherService

load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

db_repo = WeatherRepository()
weather_service = WeatherService(API_KEY)
scheduler = BackgroundScheduler()

class SettingsModel(BaseModel):
    lat: float
    lon: float
    interval: int

def job_fetch_and_store():

    lat = float(db_repo.get_setting("target_lat", "53.0793"))
    lon = float(db_repo.get_setting("target_lon", "8.8017"))
    
    print(f"Fetching weather for Lat: {lat}, Lon: {lon}...")
    
    weather_data = weather_service.fetch_current_weather(lat, lon)
    
    if weather_data:
        db_repo.save(weather_data["timezone"], weather_data["temp"], weather_data["humidity"], lat, lon, weather_data["weather"])
        print(f"Saved: {weather_data['timezone']} ({weather_data['temp']}°C) {weather_data['weather']}")

@app.on_event("startup")
def start_app():
    interval = int(db_repo.get_setting("interval_minutes", "30"))
    scheduler.add_job(job_fetch_and_store, 'interval', minutes=interval, id="weather_job")
    scheduler.start()
    job_fetch_and_store()

@app.get("/api/status")
def get_status():
    return {
        "lat": float(db_repo.get_setting("target_lat", "53.0793")),
        "lon": float(db_repo.get_setting("target_lon", "8.8017")),
        "interval": int(db_repo.get_setting("interval_minutes", "30"))
    }

@app.get("/api/history")
def get_history():
    return db_repo.get_all(limit=20)

@app.post("/api/settings")
def update_settings(settings: SettingsModel):
    db_repo.update_setting("target_lat", str(settings.lat))
    db_repo.update_setting("target_lon", str(settings.lon))
    db_repo.update_setting("interval_minutes", str(settings.interval))
    
    try:
        scheduler.reschedule_job("weather_job", trigger='interval', minutes=settings.interval)
        job_fetch_and_store()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
    return {"message": "Settings updated", "data": settings}