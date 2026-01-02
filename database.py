import sqlite3
from datetime import datetime

class WeatherRepository:
    def __init__(self, db_name="weather.db"):
        self.db_name = db_name
        self._init_db()

    def _get_connection(self):

        conn = sqlite3.connect(self.db_name, check_same_thread=False)
        conn.row_factory = sqlite3.Row 
        return conn

    def _init_db(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS weather_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    city TEXT, 
                    temp REAL,
                    lat FLOAT,
                    lon FLOAT,
                    humidity INTEGER,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    DESCRIPTION TEXT
                )
            """)

            # Ensure older DBs have all expected columns (migrate if necessary)
            cursor.execute("PRAGMA table_info(weather_logs)")
            existing_cols = [row[1] if isinstance(row, tuple) else row["name"] for row in cursor.fetchall()]

            if "lat" not in existing_cols:
                cursor.execute("ALTER TABLE weather_logs ADD COLUMN lat FLOAT")
            if "lon" not in existing_cols:
                cursor.execute("ALTER TABLE weather_logs ADD COLUMN lon FLOAT")
            if "description" not in existing_cols and "DESCRIPTION" not in existing_cols:
                cursor.execute("ALTER TABLE weather_logs ADD COLUMN description TEXT")

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS settings (
                    key TEXT PRIMARY KEY,
                    value TEXT
                )
            """)
            
            cursor.execute("INSERT OR IGNORE INTO settings (key, value) VALUES ('target_lat', '53.0793')")
            cursor.execute("INSERT OR IGNORE INTO settings (key, value) VALUES ('target_lon', '8.8017')")
            cursor.execute("INSERT OR IGNORE INTO settings (key, value) VALUES ('interval_minutes', '30')")
            conn.commit()
    
    def save(self, city: str, temp: float, humidity: int, lat: float, lon: float, description: str):
        """Save weather data"""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO weather_logs (city, temp, humidity, lat, lon, description) VALUES (?, ?, ?, ?, ?, ?)",
                    (city, temp, humidity, lat, lon, description)
                )
                conn.commit()
        except sqlite3.Error as e:
            print(f"Database Error (Save): {e}")

    def get_all(self, limit: int = 100):
        """Retrieve latest data"""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT * FROM weather_logs ORDER BY timestamp DESC LIMIT ?", 
                    (limit,)
                )
                # Convert sqlite3.Row objects to dicts for FastAPI compatibility
                return [dict(row) for row in cursor.fetchall()]
        except sqlite3.Error as e:
            print(f"Database Error (Get All): {e}")
            return []

    def get_setting(self, key: str, default: str = ""):
        """Retrieve a setting value"""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT value FROM settings WHERE key = ?", (key,))
                row = cursor.fetchone()
                return row["value"] if row else default
        except sqlite3.Error as e:
            print(f"Database Error (Get Setting): {e}")
            return default

    def update_setting(self, key: str, value: str):
        """Update a setting value"""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)", 
                    (key, value)
                )
                conn.commit()
        except sqlite3.Error as e:
            print(f"Database Error (Update Setting): {e}")