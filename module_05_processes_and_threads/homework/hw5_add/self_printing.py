"""
Напишите код, который выводит сам себя.
Обратите внимание, что скрипт может быть расположен в любом месте.
"""

result = 0
for n in range(1, 11):
    result += n ** 2

# Secret magic code
if __name__ == "__main__":
    with open(__file__, "r", encoding="utf-8") as f:
        print(f.read(), end="")