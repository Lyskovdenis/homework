from flask import Flask

app = Flask(__name__)
storage = {}


@app.route("/add/<date>/<int:number>")
def add(date, number):
    year, month, day = int(date[:4]), int(date[4:6]), int(date[6:])
    storage.setdefault(year, {}).setdefault(month, {}).setdefault(day, 0)
    storage[year][month][day] += number
    storage[year]['total'] = storage[year].get('total', 0) + number
    storage[year][month]['total'] = storage[year][month].get('total', 0) + number
    return 'Успешно добавлено'


@app.route("/calculate/<int:year>")
def calculate_year(year):
    return str(storage.get(year, {}).get('total', 0))


@app.route("/calculate/<int:year>/<int:month>")
def calculate_month(year, month):
    return str(storage.get(year, {}).get(month, {}).get('total', 0))


if __name__ == "__main__":
    app.run(debug=True)
