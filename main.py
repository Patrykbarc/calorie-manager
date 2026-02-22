from typing import List, TypedDict


class NutritionFacts(TypedDict):
    kcal: int
    protein: int
    fat: int
    carbs: int


class Meal(TypedDict):
    name: str
    nutrition_facts: NutritionFacts


class CalorieManager:
    meals: List[Meal]

    def __init__(self) -> None:
        self.meals = []

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


def main():
    manager = CalorieManager()

    while True:
        print("Licznik kalorii\n")
        print("1. Dodaj posiłek")
        print("2. Pokaż podsumowanie")
        print("3. Pokaż posiłki")
        print("4. Wyjście")

        choice = input("Wybierz opcję: ")

        if choice == "1":
            name = input("Nazwa posiłku: ")

            k = int(input("Kalorie: "))
            p = int(input("Białko (g): "))
            f = int(input("Tłuszcze (g): "))
            c = int(input("Węglowodany (g): "))

            new_meal: Meal = {
                "name": name,
                "nutrition_facts": {"kcal": k, "protein": p, "fat": f, "carbs": c},
            }

            manager.add_meal(new_meal)
            print(f"Posiłek {new_meal['name']} został zapisany.\n")

        elif choice == "2":
            total = manager.total_nutritions()
            print(f"Podsumowanie: {total}")

        elif choice == "3":
            meals_list = manager.get_meals()

            for meal in meals_list:
                print(meal["name"])

        elif choice == "4":
            print("Zamykanie programu...\n")
            break

        else:
            print("Niepoprawny wybór, spróbuj ponownie.")


if __name__ == "__main__":
    main()
