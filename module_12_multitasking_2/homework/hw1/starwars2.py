import time
import logging
import sqlite3
import requests
from multiprocessing import Pool
from multiprocessing.pool import ThreadPool
from typing import List, Dict, Any, Optional


# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)


DB_NAME = "swapi_people.db"
# Исправлен API URL на официальный swapi.dev
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


def fetch_person(person_id: int) -> Optional[Dict[str, Any]]:
    """Получает данные одного персонажа через API."""
    url = f"{BASE_URL}{person_id}/"
    try:
        resp = requests.get(url, timeout=5)
        resp.raise_for_status()
        data = resp.json()
        logger.info(f"Получен: {data.get('name')}")
        return data
    except Exception as e:
        logger.error(f"Ошибка ID {person_id}: {e}")
        return None


def save_people_to_db(people: List[Dict[str, Any]]) -> None:
    """Сохраняет список персонажей в БД."""
    valid_people = [p for p in people if p is not None]
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.executemany(
        "INSERT INTO people (name, birth_year, gender) VALUES (?, ?, ?)",
        [
            (p.get("name") or "", p.get("birth_year") or "", p.get("gender") or "")
            for p in valid_people
        ],
    )
    conn.commit()
    conn.close()


# -------- Вариант 1: Пул процессов (multiprocessing.Pool) --------


def load_people_pool(n: int = 20) -> float:
    """Загружает данные параллельно с использованием пула процессов."""
    init_db()
    start = time.perf_counter()
    print(f"\n--- Запуск Pool (процессы, {n} чел.) ---")

    with Pool(processes=4) as pool:
        people = pool.map(fetch_person, range(1, n + 1))

    save_people_to_db(people)
    elapsed = time.perf_counter() - start
    return elapsed


# -------- Вариант 2: Пул потоков (multiprocessing.pool.ThreadPool) --------


def load_people_thread_pool(n: int = 20) -> float:
    """Загружает данные параллельно с использованием пула потоков."""
    init_db()
    start = time.perf_counter()
    print(f"\n--- Запуск ThreadPool (потоки, {n} чел.) ---")

    with ThreadPool(processes=10) as pool:
        people = pool.map(fetch_person, range(1, n + 1))

    save_people_to_db(people)
    elapsed = time.perf_counter() - start
    return elapsed


def main() -> None:
    count = 20

    # Сначала запускаем пул процессов
    pool_time = load_people_pool(count)

    # Затем запускаем пул потоков
    thread_pool_time = load_people_thread_pool(count)

    print("\n" + "=" * 40)
    print(f"РЕЗУЛЬТАТЫ (загрузка {count} персонажей):")
    print(f"Pool (процессы):       {pool_time:.2f} сек.")
    print(f"ThreadPool (потоки):   {thread_pool_time:.2f} сек.")
    print("=" * 40)


if __name__ == "__main__":
    main()