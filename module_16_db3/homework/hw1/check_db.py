import sqlite3

with sqlite3.connect("database.db") as conn:
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
    print("Таблицы:", [row[0] for row in cursor.fetchall()])

    for table in ["actors", "movie", "director", "movie_cast", "oscar_awarded", "movie_direction"]:
        print(f"\n--- {table} ---")
        cursor.execute(f"SELECT * FROM {table}")
        rows = cursor.fetchall()
        for row in rows:
            print(row)