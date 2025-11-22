from PyQt6.QtWidgets import QWidget, QVBoxLayout
from .MessageTableWidget import MessageTableWidget

class CommonWidget(QWidget):
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.layout = QVBoxLayout(self)
        # Table View for Received Data
        self.readTable = MessageTableWidget()
        self.layout.addWidget(self.readTable)
        
         # Table View for Sent Data
        self.sendTable = MessageTableWidget()
        self.layout.addWidget(self.sendTable)
        
    def some_method(self):
        pass
