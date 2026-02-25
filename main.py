from cli import CLI
from file_manager import FileManager
from manager import CalorieManager

if __name__ == "__main__":
    manager = CalorieManager()
    file_manager = FileManager()

    CLI(manager, file_manager).run()
