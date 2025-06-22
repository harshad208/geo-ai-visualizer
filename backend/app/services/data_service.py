import sqlite3
from typing import List, Dict, Any

DB_PATH = "app/data/startups.db"
TABLE_NAME = "startups"

def _get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  
    return conn

def _format_to_geopoint(row: sqlite3.Row) -> Dict[str, Any]:
    """Converts a database row to a GeoJSON Feature structure."""
    return {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [row["longitude"], row["latitude"]]
        },
        "properties": {
            "company_name": row["company_name"],
            "city": row["city"],
            "funding_usd": row["funding_usd"]
        }
    }

def get_all_startups() -> List[Dict[str, Any]]:
    conn = _get_db_connection()
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {TABLE_NAME}")
    rows = cursor.fetchall()
    conn.close()
    return [_format_to_geopoint(row) for row in rows]

def get_top_funded(limit: int = 10) -> List[Dict[str, Any]]:
    conn = _get_db_connection()
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {TABLE_NAME} ORDER BY funding_usd DESC LIMIT ?", (limit,))
    rows = cursor.fetchall()
    conn.close()
    return [_format_to_geopoint(row) for row in rows]

def get_startups_by_city(city: str) -> List[Dict[str, Any]]:
    conn = _get_db_connection()
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {TABLE_NAME} WHERE lower(city) = lower(?)", (city,))
    rows = cursor.fetchall()
    conn.close()
    return [_format_to_geopoint(row) for row in rows]