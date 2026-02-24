from datetime import datetime

from manager import CalorieManager
from models import Meal


class CLI:
    def __init__(self, manager: CalorieManager) -> None:
        self.manager = manager

    def run(self) -> None:
        while True:
            now = self._get_timestamp().strftime("%Y-%m-%d %H:%M:%S")

            print(f"\n=== Licznik kalorii | {now} ===")
            print("1. Dodaj posiłek")
            print("2. Pokaż podsumowanie")
            print("3. Pokaż posiłki")
            print("4. Zamknij program")

            choice = input("\nWybierz opcję: ")

            match choice:
                case "1":
                    self._handle_add_meal()
                case "2":
                    self._handle_show_summary()
                case "3":
                    self._handle_show_meals()
                case "4":
                    print("Zamykanie programu...\n")
                    break
                case _:
                    print("Niepoprawny wybór, spróbuj ponownie.")

    def _get_timestamp(self) -> datetime:
        return datetime.now()

    def _handle_add_meal(self) -> None:
        print("(Zostaw pole puste i naciśnij Enter, aby anulować)\n")

        name = input("Nazwa posiłku: ").strip()

        if not name:
            print("Anulowano dodawanie posiłku.")
            return

        meal_macro_prompts = {
            "k": {"prompt": "Kalorie: "},
            "p": {"prompt": "Białko (g): "},
            "f": {"prompt": "Tłuszcze (g): "},
            "c": {"prompt": "Węglowodany (g): "},
        }

        results: dict[str, float] = {}

        try:
            for key, info in meal_macro_prompts.items():
                user_input = input(info["prompt"]).strip().replace(",", ".")

                if not user_input:
                    print("Anulowano dodawanie posiłku.")
                    return

                results[key] = float(user_input)

            k, p, f, c = results["k"], results["p"], results["f"], results["c"]
            print(f"\nZapisano: K:{k}, P:{p}, F:{f}, C:{c}")
        except ValueError:
            print("Błąd: podaj liczby całkowite dla wartości odżywczych.")
            return

        if any(v < 0 for v in [k, p, f, c]):
            print("Błąd: wartości odżywcze nie mogą być ujemne.")
            return

        new_meal: Meal = {
            "name": name,
            "timestamp": self._get_timestamp().isoformat(),
            "nutrition_facts": {"kcal": int(k), "protein": p, "fat": f, "carbs": c},
        }

        self.manager.add_meal(new_meal)

        try:
            self.manager.save_to_file()
            print(f"Posiłek {new_meal['name'].lower()} został zapisany.\n")
        except Exception as e:
            print(f"Błąd podczas zapisywania danych: {e}")

    def _handle_show_summary(self) -> None:
        if not self.manager.get_meals():
            print("Brak posiłków do podsumowania.")
            return

        tn = self.manager.total_nutritions()
        print("\nPodsumowanie:")
        print(f"  Kalorie:     {tn['kcal']} kcal")
        print(f"  Białko:      {tn['protein']} g")
        print(f"  Tłuszcze:    {tn['fat']} g")
        print(f"  Węglowodany: {tn['carbs']} g")

    def _handle_show_meals(self) -> None:
        meals_list = self.manager.get_meals()

        if not meals_list:
            print("Brak dodanych posiłków.")
            return

        print("\nDodane posiłki:")
        for meal in meals_list:
            nf = meal["nutrition_facts"]
            print(f"  - {meal['name']} ({nf['kcal']} kcal)")
