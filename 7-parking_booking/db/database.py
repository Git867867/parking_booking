"""Модуль подключения к базе данных SQLite."""
import sqlite3

DB_PATH = "data/parking.sqlite"


def get_connection():
    """Создать соединение с БД и включить проверку внешних ключей."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn
