from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    cook_time_minutes = Column(Integer, nullable=False)
    description = Column(Text, nullable=False)
    views = Column(Integer, nullable=False, default=0)

    ingredients = relationship(
        "Ingredient", back_populates="recipe", cascade="all, delete-orphan"
    )


class Ingredient(Base):
    __tablename__ = "ingredients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)

    recipe_id = Column(Integer, ForeignKey("recipes.id"), nullable=False)
    recipe = relationship("Recipe", back_populates="ingredients")