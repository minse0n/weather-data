import sqlite3
from datetime import datetime

class WeatherRepository:
    def __init__(self, db_name="weather.db"):
        self.db_name = db_name
        self._init_db()

    def _get_connection(self):
        """DB 연결 객체를 생성하여 반환 (스레드 안전성을 위해 매번 생성)"""
        conn = sqlite3.connect(self.db_name, check_same_thread=False)
        conn.row_factory = sqlite3.Row 
        return conn

    def _init_db(self):
        """초기 테이블 생성"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS weather_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    city TEXT,
                    temp REAL,
                    humidity INTEGER,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()

    def save(self, city: str, temp: float, humidity: int):
        """날씨 데이터 저장"""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO weather_logs (city, temp, humidity) VALUES (?, ?, ?)",
                    (city, temp, humidity)
                )
                conn.commit()
                
        except sqlite3.Error as e:
            print(f"Database Error: {e}")

    def get_all(self, limit: int = 100):
        """최신 데이터 조회"""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT * FROM weather_logs ORDER BY timestamp DESC LIMIT ?", 
                    (limit,)
                )
                return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Database Error: {e}")
            return []