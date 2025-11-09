from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLineEdit, QPushButton, QCheckBox
from PyQt6.QtCore import pyqtSignal

class MessageEditWidget(QWidget):

    message_send = pyqtSignal(str)

    def __init__(self, parent=None):
        super(MessageEditWidget, self).__init__(parent)

        LINE_HEIGHT = 30
        layout = QHBoxLayout()
        self.setLayout(layout)

        self.messageEdit = QLineEdit()
        self.messageEdit.setFixedHeight(LINE_HEIGHT)
        self.messageSendButton = QPushButton("发送")
        self.messageSendButton.setFixedWidth(100)
        self.messageSendButton.setFixedHeight(LINE_HEIGHT)
        self.messageSendButton.setEnabled(False)
        self.messageSendButton.clicked.connect(self.sendButtonClicked)
        
        self.hexCheckBox = QCheckBox()
        self.hexCheckBox.setText("Hex")

        layout.addWidget(self.messageEdit)
        layout.addWidget(self.messageSendButton)
        layout.addWidget(self.hexCheckBox)

    def sendButtonClicked(self):
        self.message_send.emit(self.messageEdit.text())

    def setButtonEnabled(self, enabled):
        self.messageSendButton.setEnabled(enabled)

    def isHexChecked(self):
        return self.hexCheckBox.isChecked()