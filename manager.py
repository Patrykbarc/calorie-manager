from typing import List

from models import Meal, NutritionFacts


class CalorieManager:
    meals: List[Meal]

    def __init__(self) -> None:
        self.meals = []

    def add_meal(self, meal: Meal) -> None:
        self.meals.append(meal)

    def total_nutritions(self) -> NutritionFacts:
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
