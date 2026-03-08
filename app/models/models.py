from typing import NotRequired, TypedDict


class NutritionFacts(TypedDict):
    kcal: int
    protein: float
    fat: float
    carbs: float


class Meal(TypedDict):
    id: NotRequired[str]
    name: str
    timestamp: str
    nutrition_facts: NutritionFacts
