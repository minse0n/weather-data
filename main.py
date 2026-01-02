# main.py
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware # [필수] CORS
from pydantic import BaseModel
from apscheduler.schedulers.background import BackgroundScheduler
from dotenv import load_dotenv

from database import WeatherRepository
from service import WeatherService

load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")

app = FastAPI()

# 1. CORS 설정 (React에서의 접근 허용)
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

# Pydantic 모델 (Data Transfer Object) - 명확한 데이터 구조 정의
class SettingsModel(BaseModel):
    city: str
    interval: int

# --- 비즈니스 로직 ---
def job_fetch_and_store():
    target_city = db_repo.get_setting("target_city", "Bremen")
    print(f"🔄 Fetching weather for {target_city}...")
    weather_data = weather_service.fetch_current_weather(target_city)
    
    if weather_data:
        db_repo.save(weather_data["city"], weather_data["temp"], weather_data["humidity"])
        print(f"✅ Saved: {weather_data['city']}")

@app.on_event("startup")
def start_app():
    interval = int(db_repo.get_setting("interval_minutes", "30"))
    scheduler.add_job(job_fetch_and_store, 'interval', minutes=interval, id="weather_job")
    scheduler.start()
    job_fetch_and_store()

# --- API Endpoints (JSON Only) ---

@app.get("/api/status")
def get_status():
    """현재 설정 상태 반환"""
    return {
        "city": db_repo.get_setting("target_city", "Bremen"),
        "interval": int(db_repo.get_setting("interval_minutes", "30"))
    }

@app.get("/api/history")
def get_history():
    """기록 조회"""
    return db_repo.get_all(limit=20)

@app.post("/api/settings")
def update_settings(settings: SettingsModel):
    """설정 변경 (JSON 입력)"""
    # 1. DB 저장
    db_repo.update_setting("target_city", settings.city)
    db_repo.update_setting("interval_minutes", str(settings.interval))
    
    # 2. 스케줄러 재설정
    try:
        scheduler.reschedule_job("weather_job", trigger='interval', minutes=settings.interval)
        # 즉시 실행하여 데이터 갱신 확인
        job_fetch_and_store()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
    return {"message": "Settings updated", "data": settings}