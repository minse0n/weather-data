# app/scheduler.py
import requests
import os
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from datetime import datetime
from .database import get_db_connection

# 스케줄러 인스턴스 생성
scheduler = BackgroundScheduler()
API_KEY = os.getenv("OPENWEATHER_API_KEY")

def fetch_weather_job():
    """실제 날씨를 가져와서 DB에 저장하는 작업"""
    try:
        # 1. DB에서 현재 설정(좌표) 가져오기
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT lat, lon FROM settings WHERE id = 1")
            config = cursor.fetchone()
            
            if not config: return
            lat, lon = config['lat'], config['lon']

            # 2. OpenWeatherMap API 호출 (좌표 기준)
            url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
            response = requests.get(url)
            
            if response.status_code != 200:
                print(f"⚠️ API Error: {response.text}")
                return
            
            data = response.json()
            city_name = data.get("name", "Unknown")
            temp = data["main"]["temp"]
            humidity = data["main"]["humidity"]

            # 3. 결과 저장
            cursor.execute(
                "INSERT INTO weather_logs (city, lat, lon, temp, humidity) VALUES (?, ?, ?, ?, ?)",
                (city_name, lat, lon, temp, humidity)
            )
            conn.commit()
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Saved: {city_name} ({temp}°C)")

    except Exception as e:
        print(f"❌ Error in job: {e}")

def update_scheduler_job():
    """설정이 변경되었을 때 호출되어 스케줄러 주기를 재설정함"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT interval_minutes FROM settings WHERE id = 1")
        row = cursor.fetchone()
        interval = row['interval_minutes'] if row else 30

    # 기존 작업이 있다면 제거
    if scheduler.get_job('weather_job'):
        scheduler.remove_job('weather_job')
    
    # 새로운 주기로 작업 등록
    scheduler.add_job(
        fetch_weather_job, 
        trigger=IntervalTrigger(minutes=interval), 
        id='weather_job',
        replace_existing=True
    )
    print(f"🔄 Scheduler updated: Runs every {interval} minutes.")