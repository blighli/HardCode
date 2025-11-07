from PyQt6.QtWidgets import QApplication
from app.MainWindow import MainWindow

def main():
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()

if __name__ == "__main__":
    main()
