from PyQt6.QtWidgets import QApplication
from app.MainWindow import MainWindow

import sys, os

def main():
    # Create the application
    app = QApplication([])
    app.setStyle("Fusion")
    window = MainWindow()
    window.show()
    # Move window to center of screen
    screen = app.primaryScreen()
    screen_geometry = screen.availableGeometry()
    window_geometry = window.frameGeometry()
    x = (screen_geometry.width() - window_geometry.width()) // 2
    y = (screen_geometry.height() - window_geometry.height()) // 2
    window.move(x, y)
    # Start the event loop
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
