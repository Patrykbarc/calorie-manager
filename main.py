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
        print("\nLicznik kalorii\n")
        print("1. Dodaj posiłek")
        print("2. Pokaż podsumowanie")
        print("3. Pokaż posiłki")
        print("4. Wyjście")

        choice = input("\nWybrano opcję: ")

        if choice == "1":
            name = input("Nazwa posiłku: ").strip()
            if not name:
                print("Błąd: nazwa posiłku nie może być pusta.")
                continue

            try:
                k = int(input("Kalorie: "))
                p = int(input("Białko (g): "))
                f = int(input("Tłuszcze (g): "))
                c = int(input("Węglowodany (g): "))
            except ValueError:
                print("Błąd: podaj liczby całkowite dla wartości odżywczych.")
                continue

            if any(v < 0 for v in [k, p, f, c]):
                print("Błąd: wartości odżywcze nie mogą być ujemne.")
                continue

            new_meal: Meal = {
                "name": name,
                "nutrition_facts": {"kcal": k, "protein": p, "fat": f, "carbs": c},
            }

            manager.add_meal(new_meal)
            print(f"Posiłek {new_meal['name']} został zapisany.\n")

        elif choice == "2":
            if not manager.get_meals():
                print("Brak posiłków do podsumowania.")
                continue

            tn = manager.total_nutritions()
            print("\nPodsumowanie:")
            print(f"  Kalorie:     {tn['kcal']} kcal")
            print(f"  Białko:      {tn['protein']} g")
            print(f"  Tłuszcze:    {tn['fat']} g")
            print(f"  Węglowodany: {tn['carbs']} g")

        elif choice == "3":
            meals_list = manager.get_meals()

            if not meals_list:
                print("Brak dodanych posiłków.")
                continue

            print("\nDodane posiłki:")
            for meal in meals_list:
                nf = meal["nutrition_facts"]
                print(f"  - {meal['name']} ({nf['kcal']} kcal)")

        elif choice == "4":
            print("Zamykanie programu...\n")
            break

        else:
            print("Niepoprawny wybór, spróbuj ponownie.")


if __name__ == "__main__":
    main()
