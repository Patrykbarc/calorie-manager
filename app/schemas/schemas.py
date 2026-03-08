from typing import Optional

from pydantic import BaseModel


class NutritionFacts(BaseModel):
    kcal: int
    protein: float
    fat: float
    carbs: float


class Meal(BaseModel):
    name: str
    timestamp: Optional[str] = None
    nutrition_facts: NutritionFacts
