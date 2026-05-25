import logging
import random
import threading
import time
from dataclasses import dataclass
from queue import PriorityQueue, Empty
from typing import Callable, Any, Tuple

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)


@dataclass(order=True)
class Task:
    priority: int
    func: Callable[[float], Any]
    arg: float

    def run(self) -> None:
        logger.info(f">running Task(priority={self.priority}).\t {self.func.__name__}({self.arg})")
        self.func(self.arg)


class Producer(threading.Thread):
    def __init__(self, queue: PriorityQueue, num_tasks: int = 10) -> None:
        super().__init__(name="Producer")
        self.queue = queue
        self.num_tasks = num_tasks

    def run(self) -> None:
        logger.info("Producer: Running")
        for i in range(self.num_tasks):
            priority = random.randint(0, 6)
            delay = random.random()
            task = Task(priority=priority, func=time.sleep, arg=delay)
            # кладём кортеж: (priority, order, task)
            self.queue.put((task.priority, i, task))
        # сигнальный элемент с особым приоритетом и None вместо task
        self.queue.put((999, self.num_tasks, None))
        logger.info("Producer: Done")


class Consumer(threading.Thread):
    def __init__(self, queue: PriorityQueue) -> None:
        super().__init__(name="Consumer")
        self.queue = queue

    def run(self) -> None:
        logger.info("Consumer: Running")
        while True:
            priority, order, task = self.queue.get()
            try:
                if task is None:
                    break  # сигнал завершения
                task.run()
            finally:
                self.queue.task_done()
        logger.info("Consumer: Done")


def main() -> None:
    q: PriorityQueue[tuple[int, int, Task | None]] = PriorityQueue()
    producer = Producer(q, num_tasks=10)
    consumer = Consumer(q)

    producer.start()
    consumer.start()

    producer.join()
    q.join()
    consumer.join()


if __name__ == "__main__":
    main()