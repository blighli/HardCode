from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit
from .MessageTemplateTableWidget import MessageTemplateTableWidget

HEADERS = ["data", "json"]

class MessageEditDialog(QDialog):
    def __init__(self, parent=None):
        super(MessageEditDialog, self).__init__(parent)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Edit CAN Message")
        self.resize(800, 600)

        layout = QVBoxLayout()

        self.nameEdit = QLineEdit("")
        self.nameEdit.setPlaceholderText("Message Name")
        layout.addWidget(self.nameEdit)

        self.tableWidget: MessageTemplateTableWidget = MessageTemplateTableWidget()
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
        name = self.nameEdit.text().strip()
        if not name:
            name = "CAN_Message"
        encodedData = self.tableWidget.encode()
        jsonData = self.tableWidget.saveTableToJson()
        return (encodedData, jsonData, name)

    def setMessageData(self, messageData, name):
        self.nameEdit.setText(name)
        if messageData:
            self.tableWidget.loadTableFromJson(messageData)