from flask import Flask

app = Flask(__name__)

# storage structure: { year: { month: total_month, 'total': total_year } }
storage = {}

@app.route('/add/<date>/<int:number>')
def add_expense(date, number):
    # Date format: YYYYMMDD
    year = int(date[:4])
    month = int(date[4:6])

    # Initialize year and month structure efficiently
    year_data = storage.setdefault(year, {'total': 0})
    year_data[month] = year_data.get(month, 0) + number
    year_data['total'] += number

    return f"Трата в размере {number} руб. за {date} успешно добавлена."

@app.route('/calculate/<int:year>')
def calculate_year(year):
    year_total = storage.get(year, {}).get('total', 0)
    return f"Суммарные траты за {year} год: {year_total} руб."

@app.route('/calculate/<int:year>/<int:month>')
def calculate_month(year, month):
    month_total = storage.get(year, {}).get(month, 0)
    return f"Суммарные траты за {month}/{year}: {month_total} руб."

if __name__ == '__main__':
    app.run(debug=True)


def create_app():
    return None