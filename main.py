from PyQt6.QtWidgets import QApplication
from app.MainWindow import MainWindow

import sys, os

def main():
    app = QApplication([])
    app.setStyle("Fusion")
    window = MainWindow()
    window.show()
    app.exec()

if __name__ == "__main__":

    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
      # Running in a PyInstaller bundle
      class DummyFile:
          def write(self, x): pass
          def flush(self): pass
          def isatty(self): return False # Indicate not a TTY

      sys.stdout = DummyFile()
      sys.stderr = DummyFile()
    
    main()
