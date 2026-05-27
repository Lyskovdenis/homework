from threading import Semaphore, Thread
import time
import sys

sem: Semaphore = Semaphore()
stop_flag = False  # Флаг для остановки потоков

def fun1():
    while not stop_flag:  # Проверяем флаг
        sem.acquire()
        print(1)
        sem.release()
        time.sleep(0.25)

def fun2():
    while not stop_flag:
        sem.acquire()
        print(2)
        sem.release()
        time.sleep(0.25)

t1: Thread = Thread(target=fun1)
t2: Thread = Thread(target=fun2)

t1.start()
t2.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print('\nReceived keyboard interrupt, quitting threads.')
    stop_flag = True
    t1.join()  # Ждём завершения потоков
    t2.join()
    sys.exit(0)