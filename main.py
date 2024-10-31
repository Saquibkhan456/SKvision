from gui.main_window import MainWindow
from config.settings import APP_CONFIG

if __name__ == "__main__":
    app = MainWindow(APP_CONFIG)
    app.run()
   