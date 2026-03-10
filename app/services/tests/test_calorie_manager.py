from unittest.mock import MagicMock

import pytest

from app.services import CalorieManager


@pytest.fixture
def sample_meal():
    return {
        "id": "abc-123",
        "name": "Owsianka",
        "timestamp": "2026-03-10T08:00:00",
        "nutrition_facts": {"kcal": 300, "protein": 10, "fat": 5, "carbs": 50},
    }


@pytest.fixture
def file_manager():
    mock = MagicMock()
    mock.read_file.return_value = []
    return mock


@pytest.fixture
def calorie_manager(file_manager):
    return CalorieManager(file_manager=file_manager)


def test_add_meal(calorie_manager, sample_meal):
    calorie_manager.add_meal(sample_meal)
    meals = calorie_manager.get_meals()

    assert len(meals) == 1
    assert meals == [sample_meal]


def test_delete_meal(calorie_manager, sample_meal):
    calorie_manager.add_meal(sample_meal)
    calorie_manager.delete_meal(sample_meal.get("id"))
    meals = calorie_manager.get_meals()

    assert len(meals) == 0


def test_update_meal(calorie_manager, sample_meal):
    mock_data = {
        "id": "abc-123",
        "name": "Schabowy",
        "timestamp": "2026-04-10T08:00:00",
        "nutrition_facts": {"kcal": 200, "protein": 20, "fat": 50, "carbs": 55},
    }

    calorie_manager.add_meal(sample_meal)
    meal_to_update_id = sample_meal.get("id")

    calorie_manager.update_meal(id=meal_to_update_id, data=mock_data)
    meals = calorie_manager.get_meals()

    assert meals == [mock_data]
