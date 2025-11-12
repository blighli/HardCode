from PyQt6.QtWidgets import QWidget, QHBoxLayout, QComboBox, QPushButton, QCheckBox
from PyQt6.QtCore import pyqtSignal
import can

class MessageEditWidget(QWidget):

    message_send = pyqtSignal(str)

    def __init__(self, parent=None):
        super(MessageEditWidget, self).__init__(parent)

        LINE_HEIGHT = 30
        layout = QHBoxLayout()
        self.setLayout(layout)

        self.messageEdit = QComboBox()
        self.messageEdit.setEditable(True)
        self.messageEdit.setFixedHeight(LINE_HEIGHT)
        self.messageEdit.setStyleSheet("font-family: Consolas;")

        self.messageSendButton = QPushButton("发送")
        self.messageSendButton.setFixedWidth(100)
        self.messageSendButton.setFixedHeight(LINE_HEIGHT)
        self.messageSendButton.setEnabled(False)
        self.messageSendButton.clicked.connect(self.sendButtonClicked)

        self.clearButton = QPushButton("清空")
        self.clearButton.setFixedWidth(100)
        self.clearButton.setFixedHeight(LINE_HEIGHT)
        #self.messageSendButton.setEnabled(False)
        self.clearButton.clicked.connect(self.clearButtonClicked)
        
        self.hexCheckBox = QCheckBox()
        self.hexCheckBox.setText("Hex")

        layout.addWidget(self.messageEdit, 1)
        layout.addWidget(self.messageSendButton)
        layout.addWidget(self.clearButton)
        layout.addWidget(self.hexCheckBox)
    
    def setHistory(self, items):
        self.messageEdit.addItems(items)

    def history(self):
        return [self.messageEdit.itemText(i) for i in range(self.messageEdit.count())]

    def sendButtonClicked(self):
        message = self.messageEdit.currentText()
        found = False
        for i in range(self.messageEdit.count()):
            if self.messageEdit.itemText(i) == message:
                found = True
        if not found:
            self.messageEdit.addItem(message)

        #使用python-can发送报文
        if message == "can":
            can_msg = can.Message(
                arbitration_id=0x123,
                data=[0x01, 0x02, 0x03, 0x04],
                is_extended_id=False
            )
            message = str(can_msg)

        self.message_send.emit(message)

    def setButtonEnabled(self, enabled):
        self.messageSendButton.setEnabled(enabled)

    def isHexChecked(self):
        return self.hexCheckBox.isChecked()
    
    def setHexChecked(self, checked):
        self.hexCheckBox.setChecked(checked)

    def clearButtonClicked(self):
        self.messageEdit.clear()