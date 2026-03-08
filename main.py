from app.services import FileManager, SettingsManager
from cli import CLI

if __name__ == "__main__":
    file_manager = FileManager()
    settings_manager = SettingsManager(file_manager)

    CLI(settings_manager).run()
