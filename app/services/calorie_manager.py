from typing import List

from app.core import MEALS_DATA_FILE_NAME
from app.models import Meal, NutritionFacts

from .file_manager import FileManager


class CalorieManager:
    meals: List[Meal]

    def __init__(self, file_manager: FileManager) -> None:
        self.file_manager = file_manager
        self.meals = file_manager.read_file(MEALS_DATA_FILE_NAME) or []

    def add_meal(self, meal: Meal) -> None:
        self.meals.append(meal)

    def get_total_nutritions(self) -> NutritionFacts:
        total: NutritionFacts = {"kcal": 0, "carbs": 0, "fat": 0, "protein": 0}

        for meal in self.meals:
            nf = meal["nutrition_facts"]

            total["kcal"] += nf["kcal"]
            total["protein"] += nf["protein"]
            total["fat"] += nf["fat"]
            total["carbs"] += nf["carbs"]

        return total

    def get_meals(self) -> List[Meal]:
        return self.meals

    def delete_meal(self, id: str) -> List[Meal] | None:
        self.meals = [meal for meal in self.meals if meal.get("id") != id]
        self.file_manager.save_to_file(MEALS_DATA_FILE_NAME, self.meals)
