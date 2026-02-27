from calorie_manager import CalorieManager
from cli import CLI
from file_manager import FileManager
from settings_manager import SettingsManager

if __name__ == "__main__":
    file_manager = FileManager()
    settings_manager = SettingsManager(file_manager)
    manager = CalorieManager(file_manager)

    CLI(manager, file_manager, settings_manager).run()
