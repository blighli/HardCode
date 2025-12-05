from PyQt6.QtWidgets import QWidget, QTextEdit, QHBoxLayout, QLineEdit, QPushButton, QCheckBox
from PyQt6.QtCore import Qt, pyqtSignal

class MessageDisplayWidget(QWidget):

    def __init__(self, parent=None):
        super(MessageDisplayWidget, self).__init__(parent)

        self.hexMode = False

        layout = QHBoxLayout()
        self.setLayout(layout)

        self.messageDisplay = QTextEdit()
        self.messageDisplay.setReadOnly(True)
        self.messageDisplay.setStyleSheet("font-family: Consolas;")
        layout.addWidget(self.messageDisplay)
        
        self.messageDisplay.addAction("Hex Mode", self.toggleHexMode).setCheckable(True)
        self.messageDisplay.setContextMenuPolicy(Qt.ContextMenuPolicy.ActionsContextMenu)

        self.messageDisplay.addAction("Clear", self.clearMessages)

    def isHexMode(self):
        return self.hexMode

    def clearMessages(self):
        self.messageDisplay.clear()

    def toggleHexMode(self):
        self.hexMode = not self.hexMode
        print(f"Hex Mode {'Enabled' if self.hexMode else 'Disabled'}")

    def appendMessage(self, message):
        self.messageDisplay.setPlainText(self.messageDisplay.toPlainText() + message)
        self.messageDisplay.verticalScrollBar().setValue(
            self.messageDisplay.verticalScrollBar().maximum()
        )

    def send(self, message):
        self.appendMessage("Send -> " + message)

    def recv(self, message):
        self.appendMessage("Recv <- " + message)