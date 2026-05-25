import logging
import random
import threading
import time
from typing import List

TOTAL_TICKETS: int = 10
MAX_TICKETS: int = 50
NUM_SELLERS: int = 3

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(name)s: %(message)s')
logger: logging.Logger = logging.getLogger('Театр')


class Director(threading.Thread):
    def __init__(self, semaphore: threading.Semaphore, sellers: List['Seller']) -> None:
        super().__init__(name='Директор')
        self.sem = semaphore
        self.sellers = sellers

    def run(self) -> None:
        global TOTAL_TICKETS
        # Пока жив хотя бы один продавец
        while any(seller.is_alive() for seller in self.sellers):
            time.sleep(0.5)  # Интервал мониторинга
            with self.sem:
                # Порог: если билетов меньше или столько же, сколько продавцов,
                # и мы не превысили лимит печати
                if 0 < TOTAL_TICKETS <= len(self.sellers) and (TOTAL_TICKETS + 10 <= MAX_TICKETS):
                    tickets_to_print = 6
                    TOTAL_TICKETS += tickets_to_print
                    logger.info(
                        f'--- Директор напечатал {tickets_to_print} билетов. Всего доступно: {TOTAL_TICKETS} ---')
                    time.sleep(1)  # Симуляция времени печати


class Seller(threading.Thread):
    def __init__(self, semaphore: threading.Semaphore) -> None:
        super().__init__()
        self.sem: threading.Semaphore = semaphore
        self.tickets_sold: int = 0
        logger.info(f'Продавец {self.name} начал работу')

    def run(self) -> None:
        global TOTAL_TICKETS
        while True:
            self.random_sleep()
            with self.sem:
                if TOTAL_TICKETS <= 0:
                    break
                self.tickets_sold += 1
                TOTAL_TICKETS -= 1
                logger.info(f'{self.name} продал билет; осталось {TOTAL_TICKETS}')
        logger.info(f'Продавец {self.name} закончил работу. Всего продано: {self.tickets_sold}')

    def random_sleep(self) -> None:
        time.sleep(random.uniform(0.1, 0.5))


def main() -> None:
    # Семафор инициализирован числом 3 (представляет 3 открытые кассы)
    semaphore = threading.BoundedSemaphore(NUM_SELLERS)

    sellers: List[Seller] = []
    for _ in range(NUM_SELLERS):
        seller = Seller(semaphore)
        sellers.append(seller)

    director = Director(semaphore, sellers)

    # Запуск потоков
    for seller in sellers:
        seller.start()
    director.start()

    # Ожидание завершения
    for seller in sellers:
        seller.join()
    director.join()

    logger.info("Все билеты проданы, зал полон.")


if __name__ == '__main__':
    main()