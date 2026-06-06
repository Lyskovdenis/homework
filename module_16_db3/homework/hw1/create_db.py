import sqlite3
from pathlib import Path
import sys

SQL_FILE = Path("create_schema.sql")
DB_FILE = Path("database.db")

if not SQL_FILE.exists():
    print(f"Файл {SQL_FILE} не найден. Поместите create_schema.sql в текущую папку.")
    sys.exit(1)

sql_script = SQL_FILE.read_text(encoding="utf-8")

# Выполняем скрипт в базе данных SQLite
with sqlite3.connect(DB_FILE) as conn:
    # Включаем проверку внешних ключей
    conn.execute("PRAGMA foreign_keys = ON;")
    cursor = conn.cursor()
    try:
        cursor.executescript(sql_script)
        conn.commit()
        print(f"Схема успешно создана в {DB_FILE}")
    except sqlite3.DatabaseError as e:
        print("Ошибка при выполнении SQL-скрипта:", e)
        sys.exit(1)

# Небольшая проверка: выводим список таблиц
with sqlite3.connect(DB_FILE) as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
    tables = [row[0] for row in cursor.fetchall()]
    print("Таблицы в базе:", ", ".join(tables))