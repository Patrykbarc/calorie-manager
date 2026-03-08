import sys
from dataclasses import asdict, dataclass

from app.core import USER_SETTINGS_FILE_NAME

from .file_manager import FileManager


@dataclass
class UserSettings:
    calories_daily: int = 2200
    name: str = ""


class SettingsManager:
    def __init__(self, file_manager: FileManager) -> None:
        self.file_manager = file_manager

    def get_user_settings(self) -> UserSettings | None:
        data = self.file_manager.read_file(USER_SETTINGS_FILE_NAME)

        if not data:
            return None

        return UserSettings(**data)

    def run_user_settings_form(self):
        settings_prompts = {
            "name": {"prompt": "Jak masz na imię?\n", "type": "str"},
            "kcal": {
                "prompt": "Ile kalorii dziennie chcesz spożywać?\n",
                "type": "int",
            },
        }

        results = {}

        try:
            idx = 0
            keys = list(settings_prompts.keys())

            while idx < len(settings_prompts):
                key = keys[idx]
                prompt_data = settings_prompts[key]
                user_input = input(prompt_data["prompt"]).strip()

                if not user_input:
                    print("⚠️ To pole nie może być puste. Spróbuj ponownie.")
                    continue

                try:
                    expected_type = prompt_data["type"]

                    if expected_type == "int":
                        res = int(user_input)

                        if res <= 0:
                            print("⚠️ Wartość nie może być ujemna.")
                            continue

                        results[key] = res
                    else:
                        results[key] = str(user_input)

                    idx += 1

                except ValueError:
                    print(
                        f"⚠️ Nieprawidłowy format! Oczekiwano wartości typu: {expected_type}."
                    )
        except KeyboardInterrupt:
            print("\n🛑 Przerwano wprowadzanie danych.")
            print("\n🛑 Zamykanie programu...")
            sys.exit(0)
        except Exception as e:
            print(f"❌ Wystąpił błąd krytyczny: {e}")
            sys.exit(0)

        response: UserSettings = UserSettings(
            name=results["name"], calories_daily=results["kcal"]
        )
        self._set_user_settings(response)

    def _set_user_settings(self, settings: UserSettings):
        return self.file_manager.save_to_file(USER_SETTINGS_FILE_NAME, asdict(settings))
