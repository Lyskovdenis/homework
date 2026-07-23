from typing import List
from pydantic import BaseModel, Field


class IngredientBase(BaseModel):
    name: str = Field(..., description="Название ингредиента")


class IngredientRead(IngredientBase):
    id: int = Field(..., description="Идентификатор ингредиента")

    class Config:
        orm_mode = True


class RecipeBase(BaseModel):
    title: str = Field(..., description="Название блюда")
    cook_time_minutes: int = Field(
        ..., description="Время приготовления в минутах", ge=1
    )
    description: str = Field(..., description="Текстовое описание рецепта")


class RecipeCreate(RecipeBase):
    ingredients: List[IngredientBase] = Field(
        ..., description="Список ингредиентов для рецепта"
    )


class RecipeRead(RecipeBase):
    id: int = Field(..., description="Идентификатор рецепта")
    views: int = Field(..., description="Количество просмотров рецепта")
    ingredients: List[IngredientRead] = Field(
        ..., description="Список ингредиентов рецепта"
    )

    class Config:
        orm_mode = True


class RecipeListItem(BaseModel):
    id: int = Field(..., description="Идентификатор рецепта")
    title: str = Field(..., description="Название блюда")
    views: int = Field(..., description="Количество просмотров")
    cook_time_minutes: int = Field(
        ..., description="Время приготовления в минутах"
    )

    class Config:
        orm_mode = True