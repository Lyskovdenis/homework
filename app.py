import os  # Для работы с путями к файлам
import re  # Для работы с регулярными выражениями
import random  # Для генерации случайных значений
from datetime import datetime, timedelta  # Для работы с временем
from flask import Flask  # Для создания веб-сервера

# Создаём объект Flask-приложения
app = Flask(__name__)

# --------------------
# Задача 1: /hello_world
# --------------------
# Создаём endpoint, который возвращает текст "Привет, мир!"


@app.route('/hello_world')
def get_hello():
   return "Привет, мир!"  # Возвращаем строку пользователю

# --------------------
# Задача 2: /cars
# --------------------
# Список машин создаём один раз в глобальной области видимости
cars = ['Chevrolet', 'Renault', 'Ford', 'Lada']


@app.route('/cars')
def get_cars():
   # Возвращаем список машин через запятую
   return ", ".join(cars)

# --------------------
# Задача 3: /cats
# --------------------
# Список пород кошек тоже в глобальной области видимости
cats = ['Корниш рекс', 'Русская голубая', 'Шотландская вислоухая', 'Мэйн-Кун', 'Манчкин']


@app.route('/cats')
def get_cats():
   # Возвращаем случайную породу кошки
   return random.choice(cats)

# --------------------
# Задача 4: /get_time/now
# --------------------
app = Flask(__name__)


@app.route('/time')
def get_time():
    current_time = datetime.now()
    return f'Точное время: {current_time}'

# --------------------
# Задача 5: /get_time/future
# --------------------


@app.route('/time_after_hour')
def get_time_after_hour():
    # Вычисляем время через один час
    current_time_after_hour = datetime.now() + timedelta(hours=1)
    return f'Точное время через час будет {current_time_after_hour}'

# --------------------
# Задача 6: /get_random_word
# --------------------
# Глобальная переменная для хранения списка слов из книги


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BOOK_FILE = os.path.join(BASE_DIR, 'war_and_peace.txt')

def get_words_from_book(file_path):
    """Функция для получения списка слов из файла без знаков препинания."""
    with open(file_path, 'r', encoding='utf-8') as book:
        text = book.read()
        # Находим все слова (последовательности букв)
        words = re.findall(r'\b\w+\b', text, re.UNICODE)
    return words

# Загружаем список слов один раз при старте приложения
try:
    all_words = get_words_from_book(BOOK_FILE)
except FileNotFoundError:
    all_words = []
    print(f"Ошибка: Файл {BOOK_FILE} не найден.")

@app.route('/get_random_word')
def get_random_word():
    if not all_words:
        return "Список слов пуст или книга не найдена."
    return random.choice(all_words)

# --------------------
# Задача 7: /counter
# --------------------
# Глобальная переменная-счётчик


@app.route('/counter')
def counter_view():
    counter_view.visits += 1
    return f'Количество посещений: {counter_view.visits}'

# Инициализация атрибута функции
counter_view.visits = 0

@app.route('/')
def index():
    return 'Сервер запущен. Счетчик доступен по адресу <a href="/counter">/counter</a>'

if __name__ == '__main__':
   # Запускаем сервер на порту 8080 с включенным режимом отладки
   app.run(debug=True, port=8080)
