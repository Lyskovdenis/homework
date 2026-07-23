from typing import List

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from database import SessionLocal, engine
import models
import schemas

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Cookbook API",
    description="API кулинарной книги: рецепты, ингредиенты и просмотры.",
    version="1.0.0",
)


# Dependency: получить сессию БД для каждого запроса
def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post(
    "/recipes",
    response_model=schemas.RecipeRead,
    summary="Создать новый рецепт",
    description="Создаёт новый рецепт с ингредиентами.",
)
def create_recipe(
    recipe_in: schemas.RecipeCreate, db: Session = Depends(get_db)
):
    recipe = models.Recipe(
        title=recipe_in.title,
        cook_time_minutes=recipe_in.cook_time_minutes,
        description=recipe_in.description,
        views=0,
    )
    db.add(recipe)
    db.flush()  # получаем id до коммита

    for ing in recipe_in.ingredients:
        ingredient = models.Ingredient(name=ing.name, recipe_id=recipe.id)
        db.add(ingredient)

    db.commit()
    db.refresh(recipe)
    return recipe


@app.get(
    "/recipes",
    response_model=List[schemas.RecipeListItem],
    summary="Получить список всех рецептов",
    description=(
        "Возвращает таблицу рецептов: название, количество просмотров, "
        "время приготовления. Рецепты отсортированы по просмотрам (desc), "
        "при равенстве — по времени приготовления (asc)."
    ),
)
def list_recipes(db: Session = Depends(get_db)):
    recipes = (
        db.query(models.Recipe)
        .order_by(
            models.Recipe.views.desc(),
            models.Recipe.cook_time_minutes.asc(),
        )
        .all()
    )
    return recipes


@app.get(
    "/recipes/{recipe_id}",
    response_model=schemas.RecipeRead,
    summary="Получить детальную информацию о рецепте",
    description=(
        "Возвращает рецепт с ингредиентами и увеличивает количество "
        "просмотров на 1."
    ),
)
def get_recipe(recipe_id: int, db: Session = Depends(get_db)):
    recipe = (
        db.query(models.Recipe)
        .filter(models.Recipe.id == recipe_id)
        .first()
    )
    if recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")

    # увеличиваем количество просмотров
    recipe.views += 1
    db.commit()
    db.refresh(recipe)
    return recipe


