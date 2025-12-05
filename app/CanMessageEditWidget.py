from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QTableWidget, QPushButton
from .MessageTableWidget import MessageTableWidget

HEADERS = ["data", "json"]

class CanMessageEditWidget(QDialog):
    def __init__(self, parent=None):
        super(CanMessageEditWidget, self).__init__(parent)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Edit CAN Message")
        self.resize(600, 400)

        layout = QVBoxLayout()

        self.tableWidget: MessageTableWidget = MessageTableWidget()
        self.tableWidget.setButtonVisible(False)
        layout.addWidget(self.tableWidget)

        buttonLayout = QHBoxLayout()
        buttonLayout.addStretch()
        okButton = QPushButton("OK")
        okButton.clicked.connect(self.accept)
        cancelButton = QPushButton("Cancel")
        cancelButton.clicked.connect(self.reject)
        buttonLayout.addWidget(okButton)
        buttonLayout.addWidget(cancelButton)
        
        layout.addLayout(buttonLayout)
        self.setLayout(layout)

    def getMessageData(self):
        encodedData = self.tableWidget.encode()
        jsonData = self.tableWidget.saveTableToJson()
        return (encodedData, jsonData)

    def setMessageData(self, messageData):
        if messageData:
            self.tableWidget.loadTableFromJson(messageData)