from datetime import datetime

from calorie_manager import CalorieManager
from constants.constants import MEALS_DATA_FILE_NAME
from file_manager import FileManager
from models import Meal
from settings_manager import SettingsManager


class CLI:
    def __init__(
        self,
        manager: CalorieManager,
        file_manager: FileManager,
        settings_manager: SettingsManager,
    ) -> None:
        self.manager = manager
        self.file_manager = file_manager
        self.settings_manager = settings_manager

        self._handle_user_settings()

    def run(self) -> None:
        while True:
            now = self._get_timestamp().strftime("%Y-%m-%d %H:%M:%S")

            print(f"\n=== Licznik kalorii | {now} ===")
            print("1. Dodaj posiłek")
            print("2. Pokaż podsumowanie")
            print("3. Pokaż posiłki")
            print("4. Pokaż ustawienia")
            print("5. Edytuj ustawienia")
            print("6. Zamknij program")

            choice = input("\nWybierz opcję: ")

            match choice:
                case "1":
                    self._handle_add_meal()
                case "2":
                    self._handle_show_summary()
                case "3":
                    self._handle_show_meals()
                case "4":
                    self._handle_show_user_settings()
                case "5":
                    self._handle_update_settings()
                case "6":
                    print("Zamykanie programu...\n")
                    break
                case _:
                    print("Niepoprawny wybór, spróbuj ponownie.")

    def _get_timestamp(self) -> datetime:
        return datetime.now()

    def _handle_user_settings(self) -> None:
        user_settings = self.settings_manager.get_user_settings()

        if user_settings is None:
            self.settings_manager.run_user_settings_form()
        else:
            pass

    def _handle_show_user_settings(self):
        user_settings = self.settings_manager.get_user_settings()

        if user_settings:
            print(
                f"\nImię: {user_settings.name},\nKcal: {user_settings.calories_daily}"
            )
        else:
            print(
                "\nBrak zapisanych ustawień. Skonfiguruj swój profil, aby zobaczyć szczegóły."
            )

    def _handle_update_settings(self):
        self.settings_manager.run_user_settings_form()
        user_settings = self.settings_manager.get_user_settings()

        if user_settings:
            print(
                f"\nPomyślnie zaktualizowano ustawienia.\nImię: {user_settings.name}\nKcal: {user_settings.calories_daily}"
            )
        else:
            print(
                "\nNie udało się zaktualizować ustawień. Proces został przerwany lub wystąpił błąd zapisu."
            )

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
            self.file_manager.save_to_file(
                MEALS_DATA_FILE_NAME, self.manager.get_meals()
            )
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
        raw_meals_list = self.manager.get_meals()

        meals_list = {}

        for meal in raw_meals_list:
            iso_timestamp = datetime.fromisoformat(meal["timestamp"])
            timestamp = iso_timestamp.strftime("%Y-%m-%d")

            if timestamp not in meals_list:
                meals_list[timestamp] = []

            meals_list[timestamp].append(
                {
                    "name": meal["name"],
                    "nutrition_facts": meal["nutrition_facts"],
                }
            )

        if not meals_list:
            print("Brak dodanych posiłków.")
            return

        print("\nDodane posiłki:")
        for timestamp, values in meals_list.items():
            print(f"\n{timestamp}")
            for meal in values:
                nf = meal["nutrition_facts"]
                print(f"  - {meal['name']} ({nf['kcal']})")
