from PyQt6.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, QPushButton, QHBoxLayout, QVBoxLayout, QFileDialog, QComboBox, QHeaderView, QLabel
from PyQt6.QtCore import Qt, pyqtSignal
import json
from .MessageTableWidget import MessageTableWidget
from .utils import assets_path

class CommonWidget(QWidget):

    send_message = pyqtSignal(str)

    def __init__(self, parent=None):
        super(CommonWidget, self).__init__(parent)

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.msgTable = MessageTableWidget()
        layout.addWidget(self.msgTable)
        
        self.msgTable.send_message.connect(self.send_message)
        self.msgTable.loadTableFromFile(assets_path.get('config//default//USBCAN_AT.json'))
        self.msgTable.setButtonText("发送")