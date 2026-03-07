from contextlib import asynccontextmanager

from fastapi import FastAPI, Request

from calorie_manager import CalorieManager
from file_manager import FileManager


@asynccontextmanager
async def lifespan(app: FastAPI):
    file_manager = FileManager()
    calorie_manager = CalorieManager(file_manager)

    app.state.calorie_manager = calorie_manager
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/meals")
def get_meals(request: Request):
    calorie_manager = request.app.state.calorie_manager
    return calorie_manager.get_meals()
