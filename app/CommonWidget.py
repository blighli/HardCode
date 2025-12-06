from PyQt6.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, QPushButton, QHBoxLayout, QVBoxLayout, QFileDialog, QComboBox, QHeaderView, QLabel
from PyQt6.QtCore import Qt, pyqtSignal
from .MessageTemplateTableWidget import MessageTemplateTableWidget
from .MessageListTableWidget import MessageListTableWidget
from .utils import assets_path

class CommonWidget(QWidget):

    send_message = pyqtSignal(str)
    DEFAULT_MESSAGE_TEMPLATE_FILE_PATH = 'config//default//USBCAN_AT.template'

    def __init__(self, parent=None):
        super(CommonWidget, self).__init__(parent)

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.msgTable = MessageTemplateTableWidget()
        layout.addWidget(self.msgTable)
        
        self.msgTable.send_message.connect(self.send_message)
        self.msgTable.loadTableFromFile(assets_path.get(self.DEFAULT_MESSAGE_TEMPLATE_FILE_PATH))
        self.msgTable.setButtonText("发送")

        self.msgListTable = MessageListTableWidget(messageTemplateFilePath=assets_path.get(self.DEFAULT_MESSAGE_TEMPLATE_FILE_PATH))
        self.msgListTable.send_message.connect(self.send_message)
        layout.addWidget(self.msgListTable)