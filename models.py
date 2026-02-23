from typing import TypedDict


class NutritionFacts(TypedDict):
    kcal: int
    protein: int
    fat: int
    carbs: int


class Meal(TypedDict):
    name: str
    timestamp: str
    nutrition_facts: NutritionFacts
