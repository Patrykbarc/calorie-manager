from typing import TypedDict


class NutritionFacts(TypedDict):
    kcal: int
    protein: float
    fat: float
    carbs: float


class Meal(TypedDict):
    name: str
    timestamp: str
    nutrition_facts: NutritionFacts
