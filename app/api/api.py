import uuid
from contextlib import asynccontextmanager
from datetime import datetime
from typing import cast

from fastapi import Depends, FastAPI, HTTPException, Request, Response, status

import app.models as models
from app.core import MEALS_DATA_FILE_NAME
from app.schemas import MealCreate
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


@api.get("/healthz")
def get_healthz(response: Response):
    response.status_code = status.HTTP_200_OK


@api.get("/meals")
def get_meals(
    manager: CalorieManager = Depends(get_calorie_manager),
):
    try:
        return manager.get_meals()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Błąd podczas pobierania danych: {e}",
        )


@api.post("/meals")
def create_meal(
    meal: MealCreate,
    calorie_manager: CalorieManager = Depends(get_calorie_manager),
    file_manager: FileManager = Depends(get_file_manager),
):
    meal_dict: models.Meal = {
        "id": str(uuid.uuid4()),
        "name": meal.name,
        "timestamp": datetime.now().isoformat(),
        "nutrition_facts": cast(
            models.NutritionFacts, meal.nutrition_facts.model_dump()
        ),
    }

    try:
        calorie_manager.add_meal(meal_dict)
        file_manager.save_to_file(MEALS_DATA_FILE_NAME, calorie_manager.get_meals())
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Błąd podczas zapisywania danych: {e}",
        )


@api.get("/meals/total-nutritions")
def get_total_nutritions(
    calorie_manager: CalorieManager = Depends(get_calorie_manager),
):
    try:
        return calorie_manager.get_total_nutritions()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Błąd podczas pobierania wartości odżywczych: {e}",
        )


@api.delete("/meals/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_meal(
    id: str,
    calorie_manager: CalorieManager = Depends(get_calorie_manager),
):
    try:
        success = calorie_manager.delete_meal(id=id)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Wystąpił wewnętrzny błąd serwera.",
        )

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Posiłek o id {id} nie istnieje.",
        )

    return None


@api.put("/meals/{id}", status_code=status.HTTP_204_NO_CONTENT)
def update_meal(
    id: str,
    data: MealCreate,
    calorie_manager: CalorieManager = Depends(get_calorie_manager),
):
    try:
        meal_dict: models.Meal = {
            "id": id,
            "name": data.name,
            "timestamp": datetime.now().isoformat(),
            "nutrition_facts": cast(
                models.NutritionFacts, data.nutrition_facts.model_dump()
            ),
        }

        success = calorie_manager.update_meal(id=id, data=meal_dict)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Wystąpił wewnętrzny błąd serwera.",
        )

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Posiłek o id {id} nie istnieje.",
        )

    return None
