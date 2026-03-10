import json
from typing import Any, Final


class FileManager:
    ENCODING_METHOD: Final = "utf-8"

    def save_to_file(self, filename: str, data) -> None:
        try:
            with open(filename, "w", encoding=self.ENCODING_METHOD) as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Wystąpił nieoczekiwany błąd: {e}")

    def read_file(self, filename: str) -> Any | None:
        try:
            with open(filename, "r", encoding=self.ENCODING_METHOD) as f:
                return json.load(f)
        except FileNotFoundError:
            return None
        except Exception as e:
            raise Exception(f"Wystąpił nieoczekiwany błąd: {e}")
