import sys
from datetime import datetime, timedelta
from typing import List

import requests
from app.models import Meal, NutritionFacts
from app.services import SettingsManager
from fastapi import status


class CLI:
    API_BASE_PATH = "http://127.0.0.1:8000"

    def __init__(
        self,
        settings_manager: SettingsManager,
    ) -> None:
        self.settings_manager = settings_manager
        self._handle_user_settings()
        self._check_healthz()

    def run(self) -> None:
        while True:
            now = self._get_timestamp().strftime("%Y-%m-%d %H:%M:%S")

            print(f"\n=== Licznik kalorii | {now} ===")
            print("1. Dodaj posiłek")
            print("2. Usuń posiłek")
            print("3. Pokaż podsumowanie")
            print("4. Pokaż posiłki")
            print("5. Pokaż ustawienia")
            print("6. Edytuj ustawienia")
            print("7. Pokaż tygodniowe podsumowanie")
            print("8. Zaktualizuj posiłek")
            print("\n9. Zamknij program")

            choice = input("\nWybierz opcję: ")

            match choice:
                case "1":
                    self._handle_add_meal()
                case "2":
                    self._handle_delete_meal()
                case "3":
                    self._handle_show_summary()
                case "4":
                    self._handle_show_meals()
                case "5":
                    self._handle_show_user_settings()
                case "6":
                    self._handle_update_settings()
                case "7":
                    self._handle_weekly_summary()
                case "8":
                    self._handle_update_meal()
                case "9":
                    print("Zamykanie programu...\n")
                    break
                case _:
                    print("Niepoprawny wybór, spróbuj ponownie.")

    def _check_healthz(self):
        try:
            requests.get(f"{self.API_BASE_PATH}/healthz")
        except requests.exceptions.ConnectionError:
            print(
                "Błąd: Nie można połączyć się z serwerem. Upewnij się, że serwer jest uruchomiony."
            )
            sys.exit(1)
        except requests.exceptions.Timeout:
            print("Błąd: Timeout połączenia z serwerem. Serwer nie odpowiada w czasie.")
            sys.exit(1)
        except Exception as e:
            print(f"Błąd serwera: {e}")
            sys.exit(1)

    def _get_timestamp(self) -> datetime:
        return datetime.now()

    def _run_meal_prompt_form(self) -> Meal | None:
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

        return new_meal

    def _handle_user_settings(self) -> None:
        user_settings = self.settings_manager.get_user_settings()

        if user_settings is None:
            self.settings_manager.run_user_settings_form()
        else:
            pass

    def _handle_get_meal_list(self) -> List[Meal]:
        return requests.get(f"{self.API_BASE_PATH}/meals").json()

    def _handle_add_meal(self) -> None:
        new_meal = self._run_meal_prompt_form()

        if new_meal is None:
            return

        try:
            requests.post(f"{self.API_BASE_PATH}/meals", json=new_meal).json()

            print(f"Posiłek {new_meal['name'].lower()} został zapisany.\n")
        except Exception as e:
            print(f"Błąd podczas zapisywania danych: {e}")

    def _handle_delete_meal(self) -> None:
        while True:
            raw_meals_list = self._handle_get_meal_list()

            if not raw_meals_list:
                print("Brak posiłków do usunięcia")
                return

            self._handle_show_meals()

            choice = input(
                '\nAby anulować naciśnij "Enter".'
                "\nWpisz numer porządkowy do usunięcia: "
            ).strip()

            if not choice:
                print("Anulowano usuwanie posiłku")
                return

            try:
                idx = int(choice) - 1

                if 0 <= idx < len(raw_meals_list):
                    meal_to_delete = raw_meals_list[idx]
                    meal_id = meal_to_delete.get("id")

                    res = requests.delete(f"{self.API_BASE_PATH}/meals/{meal_id}")

                    if res.status_code == status.HTTP_204_NO_CONTENT:
                        print(f"\nPomyślnie usunięto posiłek: {meal_to_delete['name']}")
                    else:
                        print("Wystąpił błąd serwera podczas usuwania.")
                else:
                    print(f"Błąd: Wybierz numer z zakresu 1 - {len(raw_meals_list)}.")
            except ValueError:
                print("Błąd: To nie jest liczba. Podaj numer porządkowy (np. 1).")

    def _handle_show_summary(self) -> None:
        meals: List[Meal] = self._handle_get_meal_list()

        if not meals:
            print("Brak posiłków do podsumowania.")
            return

        tn: NutritionFacts = requests.get(
            f"{self.API_BASE_PATH}/meals/total-nutritions"
        ).json()

        print(tn)

        print("\nPodsumowanie:")
        print(f"  Kalorie:     {tn['kcal']} kcal")
        print(f"  Białko:      {tn['protein']} g")
        print(f"  Tłuszcze:    {tn['fat']} g")
        print(f"  Węglowodany: {tn['carbs']} g")

    def _handle_show_meals(self) -> None:
        raw_meals_list: List[Meal] = self._handle_get_meal_list()

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

        idx = 0
        print("\nDodane posiłki:")
        for timestamp, values in meals_list.items():
            print(f"\n{timestamp}:")

            total_kcal = 0
            for meal in values:
                idx += 1
                nf = meal["nutrition_facts"]
                total_kcal += nf["kcal"]

                print(f"[{idx}] {meal['name']} ({nf['kcal']} kcal)")
            print(f"Suma: {total_kcal} kcal")

    def _handle_show_user_settings(self) -> None:
        user_settings = self.settings_manager.get_user_settings()

        if user_settings:
            print(
                f"\nImię: {user_settings.name},\nKcal: {user_settings.calories_daily}"
            )
        else:
            print(
                "\nBrak zapisanych ustawień. Skonfiguruj swój profil, aby zobaczyć szczegóły."
            )

    def _handle_update_settings(self) -> None:
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

    def _handle_weekly_summary(self) -> None:
        meals: List[Meal] = self._handle_get_meal_list()
        raw_calories_daily = self.settings_manager.get_user_settings()

        if not raw_calories_daily:
            print("Cel dzienny nie został ustalony.")
            return

        calories_goal = raw_calories_daily.calories_daily

        meals_list = {}
        last_week = datetime.now() - timedelta(days=7)

        for meal in meals:
            iso_timestamp = datetime.fromisoformat(meal["timestamp"])
            timestamp = iso_timestamp.strftime("%Y-%m-%d")
            is_older_than_week = last_week >= iso_timestamp

            kcal_value = meal["nutrition_facts"]["kcal"]

            if is_older_than_week:
                continue

            if timestamp not in meals_list:
                meals_list[timestamp] = {"kcal": 0, "difference": calories_goal}

            meals_list[timestamp]["kcal"] += kcal_value
            meals_list[timestamp]["difference"] -= kcal_value

        print(f"Cel: {calories_goal} kcal")
        for date, data in meals_list.items():
            is_calories_within_goal = "✓" if data["difference"] >= 0 else "x"

            print(
                f"{date}  {is_calories_within_goal}  {data['kcal']} kcal  ({data['difference']})"
            )

    def _handle_update_meal(self) -> None:
        while True:
            raw_meals_list = self._handle_get_meal_list()

            if not raw_meals_list:
                print("Brak posiłków do aktualizacji")
                return

            self._handle_show_meals()

            choice = input(
                '\nAby anulować naciśnij "Enter".'
                "\nWpisz numer porządkowy do aktualizacji: "
            ).strip()

            if not choice:
                print("Anulowano aktualizowanie posiłku")
                return

            try:
                idx = int(choice) - 1

                if 0 <= idx < len(raw_meals_list):
                    meal_to_update = self._run_meal_prompt_form()

                    if meal_to_update is None:
                        return

                    meal_id = raw_meals_list[idx].get("id")

                    res = requests.put(
                        f"{self.API_BASE_PATH}/meals/{meal_id}", json=meal_to_update
                    )

                    if res.status_code == status.HTTP_204_NO_CONTENT:
                        print(
                            f"\nPomyślnie zaktualizowano posiłek: {meal_to_update['name']}"
                        )
                        break
                    else:
                        print("Wystąpił błąd serwera podczas aktualizacji.")
                else:
                    print(f"Błąd: Wybierz numer z zakresu 1 - {len(raw_meals_list)}.")
            except ValueError:
                print("Błąd: To nie jest liczba. Podaj numer porządkowy (np. 1).")
