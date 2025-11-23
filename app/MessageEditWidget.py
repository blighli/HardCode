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
        self.clearButton.clicked.connect(self.clearButtonClicked)
        
        self.hexCheckBox = QCheckBox()
        self.hexCheckBox.setText("Hex")

        self.crCheckBox = QCheckBox()
        self.crCheckBox.setText("CR")

        self.lfCheckBox = QCheckBox()
        self.lfCheckBox.setText("LF")

        layout.addWidget(self.messageEdit, 1)
        layout.addWidget(self.messageSendButton)
        layout.addWidget(self.clearButton)
        layout.addWidget(self.hexCheckBox)
        layout.addWidget(self.crCheckBox)
        layout.addWidget(self.lfCheckBox)
    
    def setHistory(self, items):
        self.messageEdit.addItems(items)

    def history(self):
        return [self.messageEdit.itemText(i) for i in range(self.messageEdit.count())]
    
    def sendMessage(self, data, isHex=True, hasCR=True, hasLF=True):
        if self.messageSendButton.isEnabled():
            self.messageEdit.setCurrentText(data)
            self.hexCheckBox.setChecked(isHex)
            self.crCheckBox.setChecked(hasCR)
            self.lfCheckBox.setChecked(hasLF)
            self.sendButtonClicked()


    def sendButtonClicked(self):
        message = self.messageEdit.currentText()
        found = False
        for i in range(self.messageEdit.count()):
            if self.messageEdit.itemText(i) == message:
                found = True
        if not found:
            self.messageEdit.addItem(message)
            
        self.message_send.emit(message)

    def setButtonEnabled(self, enabled):
        self.messageSendButton.setEnabled(enabled)

    def isHexChecked(self):
        return self.hexCheckBox.isChecked()
    
    def setHexChecked(self, checked):
        self.hexCheckBox.setChecked(checked)

    def isCarriageReturnChecked(self):
        return self.crCheckBox.isChecked()
    
    def setCarriageReturnChecked(self, checked):
        self.crCheckBox.setChecked(checked)

    def isLineFeedChecked(self):
        return self.lfCheckBox.isChecked()
    
    def setLineFeedChecked(self, checked):
        self.lfCheckBox.setChecked(checked)

    def clearButtonClicked(self):
        self.messageEdit.clear()