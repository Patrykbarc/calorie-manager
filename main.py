from cli import CLI
from manager import CalorieManager

if __name__ == "__main__":
    manager = CalorieManager()
    CLI(manager).run()
