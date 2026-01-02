# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from .database import init_db, get_db_connection
from .scheduler import scheduler, update_scheduler_job

# .env 파일 로드
load_dotenv()

app = FastAPI()

# CORS 설정 (React 프론트엔드와 통신하기 위해 필수)
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "*"  # 테스트용으로 모든 접속 허용
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# 데이터 검증 모델 (Pydantic)
class SettingsUpdate(BaseModel):
    lat: float
    lon: float
    interval_minutes: int

# 서버 시작 시 실행되는 함수
@app.on_event("startup")
def startup_event():
    init_db()               # DB 테이블 생성
    scheduler.start()       # 스케줄러 시작
    update_scheduler_job()  # 초기 설정에 맞춰 작업 등록
    print("🚀 Weather Backend Started!")

# 1. 과거 날씨 데이터 조회 API
@app.get("/history")
def get_history():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        # 최신순으로 100개만 조회
        cursor.execute("SELECT * FROM weather_logs ORDER BY timestamp DESC LIMIT 100")
        return cursor.fetchall()

# 2. 현재 설정 조회 API
@app.get("/config")
def get_config():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT lat, lon, interval_minutes FROM settings WHERE id = 1")
        return cursor.fetchone()

# 3. 설정 변경 API (프론트엔드에서 저장 버튼 누를 때 호출)
@app.post("/config")
def update_config(settings: SettingsUpdate):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE settings 
            SET lat = ?, lon = ?, interval_minutes = ? 
            WHERE id = 1
        """, (settings.lat, settings.lon, settings.interval_minutes))
        conn.commit()
    
    # 설정이 바뀌었으니 스케줄러 주기 업데이트
    update_scheduler_job()
    return {"status": "success", "message": "Configuration updated"}