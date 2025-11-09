from PyQt6.QtWidgets import QWidget, QTextEdit, QHBoxLayout, QLineEdit, QPushButton, QCheckBox
from PyQt6.QtCore import pyqtSignal

class MessageDisplayWidget(QWidget):

    def __init__(self, parent=None):
        super(MessageDisplayWidget, self).__init__(parent)

        layout = QHBoxLayout()
        self.setLayout(layout)

        self.messageDisplay = QTextEdit()
        self.messageDisplay.setReadOnly(True)
        layout.addWidget(self.messageDisplay)

    def appendMessage(self, message):
        self.messageDisplay.setPlainText(self.messageDisplay.toPlainText() + message)
        self.messageDisplay.verticalScrollBar().setValue(
            self.messageDisplay.verticalScrollBar().maximum()
        )
