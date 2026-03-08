from pydantic import BaseModel


class NutritionFacts(BaseModel):
    kcal: int
    protein: float
    fat: float
    carbs: float


class MealCreate(BaseModel):
    name: str
    nutrition_facts: NutritionFacts


class MealResponse(MealCreate):
    id: str
    timestamp: str
