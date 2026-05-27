import requests
import time
import threading
from datetime import datetime
from queue import Queue

# Флаг для остановки потоков
STOP_FLAG = False

# Очередь для хранения логов (thread-safe)
log_queue: Queue = Queue()

# Блокировка для синхронизации записи в файл
file_lock: threading.Lock = threading.Lock()


def get_current_timestamp() -> float:
    """Получает текущий timestamp."""
    return time.time()


def get_date_from_server(timestamp: float) -> str:
    """
    Получает дату с сервера по timestamp.
    Использует http://127.0.0.1:8080/timestamp/<timestamp>
    """
    url = f"http://127.0.0.1:8080/timestamp/{timestamp}"
    response = requests.get(url, timeout=5)
    response.raise_for_status()
    return response.text.strip()


def worker(thread_id: int) -> None:
    """
    Работает 20 секунд, каждую секунду пишет лог в очередь.
    Формат лога: <timestamp> <дата>
    """
    start_time = time.time()

    while not STOP_FLAG and (time.time() - start_time) < 20:
        # Получаем текущий timestamp непосредственно перед запросом
        timestamp = get_current_timestamp()

        # Получаем дату с сервера
        date_str = get_date_from_server(timestamp)

        # Формируем лог и добавляем в очередь
        log_entry = f"{timestamp} {date_str}"
        log_queue.put(log_entry)

        # Ждём 1 секунду перед следующим логированием
        time.sleep(1)


def write_logs_to_file(filename: str = "logs.txt") -> None:
    """
    Записывает логи из очереди в файл, отсортированные по timestamp.
    Вызывается после завершения всех потоков.
    """
    # Собираем все логи из очереди
    logs = []
    while not log_queue.empty():
        logs.append(log_queue.get())

    # Сортируем по timestamp (первое число в строке)
    logs.sort(key=lambda x: float(x.split()[0]))

    # Записываем в файл в блоке синхронизации
    with file_lock:
        with open(filename, 'w', encoding='utf-8') as f:
            for log in logs:
                f.write(log + '\n')


def main() -> None:
    """Запускает 10 потоков, ждёт их завершения, записывает логи в файл."""
    global STOP_FLAG

    threads = []

    # Запускаем 10 потоков последовательно с интервалом в 1 секунду
    for i in range(10):
        thread = threading.Thread(target=worker, args=(i,), daemon=False)
        threads.append(thread)
        thread.start()
        time.sleep(1)  # Интервал 1 секунда между запуском потоков

    # Ждём завершения всех потоков (каждый работает 20 секунд)
    for thread in threads:
        thread.join()

    # После завершения всех потоков записываем логи в файл
    STOP_FLAG = True
    write_logs_to_file()

    print("Логи успешно записаны в файл logs.txt")


if __name__ == "__main__":
    main()