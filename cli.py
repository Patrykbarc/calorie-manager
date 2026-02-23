from datetime import datetime

from manager import CalorieManager
from models import Meal


class CLI:
    def __init__(self, manager: CalorieManager) -> None:
        self.manager = manager

    def run(self) -> None:
        while True:
            now = self._get_timestamp().strftime("%Y-%m-%d %H:%M:%S")

            print(f"\n----- {now} -----\n")
            print("Licznik kalorii\n")
            print("1. Dodaj posiłek")
            print("2. Pokaż podsumowanie")
            print("3. Pokaż posiłki")
            print("\n4. Wyjście")

            choice = input("\nWybierz opcję: ")
            print("-----")

            if choice == "1":
                self._handle_add_meal()
            elif choice == "2":
                self._handle_show_summary()
            elif choice == "3":
                self._handle_show_meals()
            elif choice == "4":
                print("Zamykanie programu...\n")
                break
            else:
                print("Niepoprawny wybór, spróbuj ponownie.")

    def _get_timestamp(self) -> datetime:
        return datetime.now()

    def _handle_add_meal(self) -> None:
        name = input("Nazwa posiłku: ").strip()
        if not name:
            print("Błąd: nazwa posiłku nie może być pusta.")
            return

        try:
            k = int(input("Kalorie: "))
            p = int(input("Białko (g): "))
            f = int(input("Tłuszcze (g): "))
            c = int(input("Węglowodany (g): "))
        except ValueError:
            print("Błąd: podaj liczby całkowite dla wartości odżywczych.")
            return

        if any(v < 0 for v in [k, p, f, c]):
            print("Błąd: wartości odżywcze nie mogą być ujemne.")
            return

        new_meal: Meal = {
            "name": name,
            "timestamp": self._get_timestamp().isoformat(),
            "nutrition_facts": {"kcal": k, "protein": p, "fat": f, "carbs": c},
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
