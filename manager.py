import json
from typing import Final, List

from models import Meal, NutritionFacts


class CalorieManager:
    FILE_NAME: Final = "data.json"
    ENCODING_METHOD: Final = "utf-8"

    meals: List[Meal]

    def __init__(self) -> None:
        self.meals = self.load_from_file()

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

    def save_to_file(self, file=FILE_NAME) -> None:
        try:
            with open(file, "w", encoding=self.ENCODING_METHOD) as file:
                json.dump(self.meals, file, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Wystąpił nieoczekiwany błąd: {e}")

    def load_from_file(self, file=FILE_NAME) -> List[Meal]:
        try:
            with open(file, "r", encoding=self.ENCODING_METHOD) as file:
                return json.load(file)
        except Exception:
            return []
