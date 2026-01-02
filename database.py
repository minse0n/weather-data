import sqlite3
from datetime import datetime

class WeatherRepository:
    def __init__(self, db_name="weather.db"):
        self.db_name = db_name
        self._init_db()

    def _get_connection(self):
        """
        [핵심] DB 연결 객체를 생성하여 반환하는 헬퍼 함수
        이 함수가 없어서 에러가 났던 것입니다.
        """
        conn = sqlite3.connect(self.db_name, check_same_thread=False)
        conn.row_factory = sqlite3.Row  # 컬럼명으로 데이터 접근 가능하게 설정
        return conn

    def _init_db(self):
        """초기 테이블 생성 (날씨 기록 & 설정)"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # 1. 날씨 기록 테이블
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS weather_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    city TEXT,
                    temp REAL,
                    humidity INTEGER,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # 2. 설정 테이블 (Level 2 기능)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS settings (
                    key TEXT PRIMARY KEY,
                    value TEXT
                )
            """)
            
            # 기본 설정값 초기화 (없을 때만 삽입)
            cursor.execute("INSERT OR IGNORE INTO settings (key, value) VALUES ('target_city', 'Bremen')")
            cursor.execute("INSERT OR IGNORE INTO settings (key, value) VALUES ('interval_minutes', '30')")
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
            print(f"❌ Database Error (Save): {e}")

    def get_all(self, limit: int = 100):
        """최신 데이터 조회"""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT * FROM weather_logs ORDER BY timestamp DESC LIMIT ?", 
                    (limit,)
                )
                # sqlite3.Row 객체를 딕셔너리로 변환하여 반환 (FastAPI 호환성)
                return [dict(row) for row in cursor.fetchall()]
        except sqlite3.Error as e:
            print(f"❌ Database Error (Get All): {e}")
            return []

    def get_setting(self, key: str, default: str = ""):
        """설정값 조회"""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT value FROM settings WHERE key = ?", (key,))
                row = cursor.fetchone()
                return row["value"] if row else default
        except sqlite3.Error as e:
            print(f"❌ Database Error (Get Setting): {e}")
            return default

    def update_setting(self, key: str, value: str):
        """설정값 업데이트"""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)", 
                    (key, value)
                )
                conn.commit()
        except sqlite3.Error as e:
            print(f"❌ Database Error (Update Setting): {e}")