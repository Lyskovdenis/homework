import time
import logging
import sqlite3
import threading
from typing import List, Dict, Any
import requests

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

DB_NAME = "swapi_people.db"
BASE_URL = "https://swapi.py4e.com/api/people/"


def init_db() -> None:
    """Инициализирует базу данных SQLite."""
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS people")
    cur.execute(
        """
        CREATE TABLE people (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            birth_year TEXT,
            gender TEXT
        )
        """
    )
    conn.commit()
    conn.close()


def fetch_person(person_id: int) -> Dict[str, Any]:
    """Получает данные одного персонажа через API."""
    url = f"{BASE_URL}{person_id}/"
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    return resp.json()


def save_people_to_db(people: List[Dict[str, Any]]) -> None:
    """Сохраняет список персонажей в БД."""
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.executemany(
        "INSERT INTO people (name, birth_year, gender) VALUES (?, ?, ?)",
        [(p.get("name"), p.get("birth_year"), p.get("gender")) for p in people],
    )
    conn.commit()
    conn.close()


# -------- Вариант 1: последовательные запросы --------

def load_people_sequential(n: int = 20) -> float:
    """Загружает данные последовательно."""
    init_db()
    start = time.perf_counter()
    people: List[Dict[str, Any]] = []

    print(f"\n--- Запуск последовательной загрузки ({n} чел.) ---")
    for person_id in range(1, n + 1):
        try:
            person = fetch_person(person_id)
            people.append(person)
            logger.info(f"[seq] Получен: {person['name']}")
        except Exception as e:
            logger.error(f"[seq] Ошибка ID {person_id}: {e}")

    save_people_to_db(people)
    elapsed = time.perf_counter() - start
    return elapsed


# -------- Вариант 2: параллельно в потоках --------

def load_people_parallel(n: int = 20) -> float:
    """Загружает данные параллельно с использованием потоков."""
    init_db()
    start = time.perf_counter()
    people: List[Dict[str, Any]] = []
    people_lock = threading.Lock()

    def worker(person_id: int) -> None:
        try:
            person = fetch_person(person_id)
            with people_lock:
                people.append(person)
            logger.info(f"[thread] Получен: {person['name']}")
        except Exception as e:
            logger.error(f"[thread] Ошибка ID {person_id}: {e}")

    print(f"\n--- Запуск параллельной загрузки ({n} чел.) ---")
    threads = []
    for person_id in range(1, n + 1):
        t = threading.Thread(target=worker, args=(person_id,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    save_people_to_db(people)
    elapsed = time.perf_counter() - start
    return elapsed


def main() -> None:
    count = 20
    seq_time = load_people_sequential(count)
    par_time = load_people_parallel(count)

    print("\n" + "=" * 30)
    print(f"РЕЗУЛЬТАТЫ (загрузка {count} персонажей):")
    print(f"Последовательно: {seq_time:.2f} сек.")
    print(f"Параллельно:     {par_time:.2f} сек.")
    print(f"Ускорение:       {seq_time / par_time:.1f}x")
    print("=" * 30)


if __name__ == "__main__":
    main()