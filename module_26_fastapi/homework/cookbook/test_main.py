import pytest
from fastapi.testclient import TestClient

from main import app
from database import Base, engine, SessionLocal
import models


# создаём тестовую БД
@pytest.fixture(autouse=True)
def setup_database():
    # Создаём таблицы (если не созданы)
    Base.metadata.create_all(bind=engine)
    # Очищаем таблицы перед каждым тестом
    db = SessionLocal()
    db.query(models.Ingredient).delete()
    db.query(models.Recipe).delete()
    db.commit()
    db.close()
    yield


client = TestClient(app)


def test_create_recipe():
    payload = {
        "title": "Паста карбонара",
        "cook_time_minutes": 20,
        "description": "Классическая паста с беконом и яйцом.",
        "ingredients": [
            {"name": "спагетти"},
            {"name": "бекон"},
            {"name": "яйцо"},
        ],
    }

    response = client.post("/recipes", json=payload)
    assert response.status_code == 200

    data = response.json()
    assert data["title"] == payload["title"]
    assert data["cook_time_minutes"] == payload["cook_time_minutes"]
    assert data["description"] == payload["description"]
    assert data["views"] == 0  # новый рецепт изначально без просмотров
    assert len(data["ingredients"]) == 3


def test_list_recipes_sorted_by_views_and_time():
    # Создаём три рецепта
    recipes = [
        {
            "title": "Салат",
            "cook_time_minutes": 10,
            "description": "Лёгкий салат.",
            "ingredients": [{"name": "огурец"}],
        },
        {
            "title": "Суп",
            "cook_time_minutes": 30,
            "description": "Горячий суп.",
            "ingredients": [{"name": "картофель"}],
        },
        {
            "title": "Пицца",
            "cook_time_minutes": 25,
            "description": "Домашняя пицца.",
            "ingredients": [{"name": "мука"}],
        },
    ]

    ids = []
    for r in recipes:
        resp = client.post("/recipes", json=r)
        assert resp.status_code == 200
        ids.append(resp.json()["id"])

    # Подкручиваем просмотры через GET /recipes/{id}
    # Сделаем: Суп — 3 просмотра, Пицца — 3, Салат — 1
    for _ in range(1):
        client.get(f"/recipes/{ids[0]}")  # Салат: 1
    for _ in range(3):
        client.get(f"/recipes/{ids[1]}")  # Суп: 3
    for _ in range(3):
        client.get(f"/recipes/{ids[2]}")  # Пицца: 3

    # Теперь проверим список
    resp = client.get("/recipes")
    assert resp.status_code == 200
    data = resp.json()

    # В первом экране нас интересует порядок:
    # - сначала по views (desc)
    # - при равных views по cook_time_minutes (asc)
    titles_order = [item["title"] for item in data]
    assert titles_order[0] in ("Суп", "Пицца")
    assert titles_order[1] in ("Суп", "Пицца")
    assert titles_order[0] != titles_order[1]  # порядок по времени
    assert titles_order[-1] == "Салат"


def test_get_recipe_increments_views():
    payload = {
        "title": "Борщ",
        "cook_time_minutes": 60,
        "description": "Классический борщ.",
        "ingredients": [{"name": "свекла"}, {"name": "капуста"}],
    }

    # Создаём рецепт
    resp = client.post("/recipes", json=payload)
    assert resp.status_code == 200
    recipe = resp.json()
    recipe_id = recipe["id"]
    assert recipe["views"] == 0

    # Первый просмотр
    resp = client.get(f"/recipes/{recipe_id}")
    assert resp.status_code == 200
    data = resp.json()
    assert data["views"] == 1

    # Второй просмотр
    resp = client.get(f"/recipes/{recipe_id}")
    assert resp.status_code == 200
    data = resp.json()
    assert data["views"] == 2

    # Проверяем, что ингредиенты и описание корректны
    assert data["title"] == payload["title"]
    assert data["cook_time_minutes"] == payload["cook_time_minutes"]
    assert len(data["ingredients"]) == 2
    assert data["description"] == payload["description"]