from dataclasses import asdict, dataclass

from constants.constants import USER_SETTINGS_FILE_NAME
from file_manager import FileManager


@dataclass
class UserSettings:
    calories_daily: int = 2200
    name: str = ""


class SettingsManager:
    def __init__(self, file_manager: FileManager) -> None:
        self.file_manager = file_manager

    def get_user_settings(self) -> UserSettings:
        data = self.file_manager.read_file(USER_SETTINGS_FILE_NAME)

        if not data:
            default_settings = UserSettings()
            self.set_user_settings(default_settings)

            return default_settings

        return UserSettings(**data)

    def set_user_settings(self, settings: UserSettings):
        return self.file_manager.save_to_file(USER_SETTINGS_FILE_NAME, asdict(settings))
