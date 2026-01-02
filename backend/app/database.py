# app/database.py
import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_NAME = os.path.join(BASE_DIR, "weather.db")

def get_db_connection():
    """DB 연결 객체 반환 (딕셔너리 형태로 조회 가능하게 설정)"""
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    conn.row_factory = sqlite3.Row 
    return conn

def init_db():
    """테이블 초기화 함수"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS weather_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                city TEXT,
                lat REAL,
                lon REAL,
                temp REAL,
                humidity INTEGER,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS settings (
                id INTEGER PRIMARY KEY CHECK (id = 1),
                lat REAL DEFAULT 53.0793, 
                lon REAL DEFAULT 8.8017,
                interval_minutes INTEGER DEFAULT 30
            )
        """)

        cursor.execute("""
            INSERT OR IGNORE INTO settings (id, lat, lon, interval_minutes) 
            VALUES (1, 53.0793, 8.8017, 30)
        """)
        
        conn.commit()