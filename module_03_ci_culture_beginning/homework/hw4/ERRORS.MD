# Ошибки в классе `Person` и их исправления

Ниже перечислены ошибки, найденные с помощью юнит‑тестов, и способы их исправления.

---

## 1. Некорректный расчёт возраста в `get_age`

**Исходный код:**

```python
def get_age(self):
    now = datetime.datetime.now()
    return self.yob - now.year
```

**Проблема:**

Возраст вычислялся как `год_рождения - текущий_год`, что даёт отрицательное значение.  
Например, при текущем годе 2026 и `yob = 1990` функция возвращала `1990 - 2026 = -36`.

**Исправление:**

```python
def get_age(self) -> int:
    now = datetime.datetime.now()
    return now.year - self.yob
```

Тест, обнаруживший проблему:

```python
def test_get_age_returns_correct_age(self):
    expected_age = self.current_year - self.person.yob
    self.assertEqual(self.person.get_age(), expected_age)
```

---

## 2. `set_name` не меняет имя

**Исходный код:**

```python
def set_name(self, name):
    self.name = self.name
```

**Проблема:**

Метод присваивает `self.name` самому себе, игнорируя переданный аргумент `name`.  
Имя объекта не меняется, тест на изменение имени падает.

**Исправление:**

```python
def set_name(self, name: str) -> None:
    self.name = name
```

Тест, обнаруживший проблему:

```python
def test_set_name_changes_name(self):
    self.person.set_name("Пётр")
    self.assertEqual(self.person.get_name(), "Пётр")
```

---

## 3. `set_address` не присваивает адрес

**Исходный код:**

```python
def set_address(self, address):
    self.address == address
```

**Проблема:**

Использован оператор сравнения `==` вместо присваивания `=`, в результате адрес не меняется.  
Тест на изменение адреса показывает, что значение поля `address` остаётся прежним.

**Исправление:**

```python
def set_address(self, address: str) -> None:
    self.address = address
```

Тест, обнаруживший проблему:

```python
def test_set_address_changes_address(self):
    self.person.set_address("Москва, ул. Пушкина, д. 1")
    self.assertEqual(self.person.get_address(), "Москва, ул. Пушкина, д. 1")
```

---

## 4. `is_homeless` использует несуществующую переменную и неверную логику

**Исходный код:**

```python
def is_homeless(self):
    '''
    returns True if address is not set, false in other case
    '''
    return address is None
```

**Проблемы:**

1. Используется переменная `address` без `self.` — это имя не определено в области видимости метода.  
   Вызов `is_homeless` приводит к `NameError`.
2. Логика учитывает только `None`, но по умолчанию адрес — пустая строка `''`, и это тоже «нет адреса».

**Исправление:**

```python
def is_homeless(self) -> bool:
    """
    Возвращает True, если адрес не задан (None или пустая строка),
    False в противном случае.
    """
    return not self.address
```

Таким образом, метод возвращает `True` как при `address=None`, так и при `address=""`.

Тесты, обнаружившие проблему:

```python
def test_is_homeless_true_when_address_empty(self):
    self.assertTrue(self.person.is_homeless())

def test_is_homeless_true_when_address_none(self):
    p = Person(name="Анна", year_of_birth=2000, address=None)
    self.assertTrue(p.is_homeless())

def test_is_homeless_false_when_address_set(self):
    self.person.set_address("СПб, Невский проспект, д. 10")
    self.assertFalse(self.person.is_homeless())
```

---