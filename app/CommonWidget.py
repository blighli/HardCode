from PyQt6.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, QPushButton, QHBoxLayout, QVBoxLayout, QFileDialog, QComboBox, QHeaderView, QLabel
from PyQt6.QtCore import Qt, pyqtSignal
import json
from .MessageTableWidget import MessageTableWidget

class CommonWidget(QWidget):

    send_message = pyqtSignal(str)

    def __init__(self, parent=None):
        super(CommonWidget, self).__init__(parent)

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.msgTable = MessageTableWidget()
        layout.addWidget(self.msgTable)
        
        self.msgTable.send_message.connect(self.send_message)