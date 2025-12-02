from PyQt6.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, QPushButton, QHBoxLayout, QVBoxLayout, QFileDialog, QComboBox, QHeaderView, QLabel
from PyQt6.QtCore import Qt
import json
from .MessageEditWidget import MessageEditWidget
from .MessageTableWidget import MessageTableWidget

class CommonWidget(QWidget):
    def __init__(self, parent=None, messenger : MessageEditWidget = None):
        super(CommonWidget, self).__init__(parent)
        self.messenger : MessageEditWidget = messenger

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.msgTable = MessageTableWidget()
        layout.addWidget(self.msgTable)
        
        self.msgTable.send_message.connect(self.messenger.sendMessage)