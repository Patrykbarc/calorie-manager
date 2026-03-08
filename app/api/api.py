from contextlib import asynccontextmanager
from datetime import datetime
from typing import cast

from fastapi import Depends, FastAPI, HTTPException, Request

import app.models as models
from app.core import MEALS_DATA_FILE_NAME
from app.schemas import Meal
from app.services import CalorieManager, FileManager


def get_calorie_manager(request: Request) -> CalorieManager:
    return request.app.state.calorie_manager


def get_file_manager(request: Request) -> FileManager:
    return request.app.state.file_manager


@asynccontextmanager
async def lifespan(app: FastAPI):
    file_manager = FileManager()
    calorie_manager = CalorieManager(file_manager)

    app.state.file_manager = file_manager
    app.state.calorie_manager = calorie_manager

    yield


api = FastAPI(lifespan=lifespan)


@api.get("/meals")
def get_meals(
    manager: CalorieManager = Depends(get_calorie_manager),
):
    try:
        return manager.get_meals()
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Błąd podczas pobierania danych: {e}"
        )


@api.post("/meals")
def create_meal(
    meal: Meal,
    calorie_manager: CalorieManager = Depends(get_calorie_manager),
    file_manager: FileManager = Depends(get_file_manager),
):
    meal_dict: models.Meal = {
        "name": meal.name,
        "timestamp": datetime.now().isoformat(),
        "nutrition_facts": cast(
            models.NutritionFacts, meal.nutrition_facts.model_dump()
        ),
    }

    try:
        calorie_manager.add_meal(meal_dict)
        file_manager.save_to_file(MEALS_DATA_FILE_NAME, calorie_manager.get_meals())
        return f'Posiłek "{meal.name}" został zapisany.\n'
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Błąd podczas zapisywania danych: {e}"
        )


@api.get("/meals/total-nutritions")
def get_total_nutritions(
    calorie_manager: CalorieManager = Depends(get_calorie_manager),
):
    try:
        return calorie_manager.total_nutritions()
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Błąd podczas pobierania wartości odżywczych: {e}"
        )
