from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget,QHeaderView, QTableWidgetItem, QFileDialog, QMessageBox
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QDialog
from PyQt6.QtCore import Qt, pyqtSignal
import json
from .MessageEditDialog import MessageEditDialog


class MessageListTableWidget(QWidget):

    send_message = pyqtSignal(str)
    HEADERS = ["Message", "Name"]

    def __init__(self, parent=None, messageTemplateFilePath=""):
        super(MessageListTableWidget, self).__init__(parent)
        self.messageEditDialog = None
        self.messageTemplateFilePath = messageTemplateFilePath
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(len(self.HEADERS))
        self.tableWidget.setHorizontalHeaderLabels(self.HEADERS)
        self.tableWidget.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.tableWidget.horizontalHeader().setMinimumSectionSize(200)
        self.tableWidget.setRowCount(0)
        
        layout.addWidget(self.tableWidget)
        self.tableWidget.addAction("Add Message", self.addMessage)
        self.tableWidget.addAction("Edit Message", self.editMessage)
        self.tableWidget.addAction("Send Message", self.sendMessage)
        
        seperator = QAction(self)
        seperator.setSeparator(True)
        self.tableWidget.addAction(seperator)
        self.tableWidget.addAction("Load", self.loadMessages)
        self.tableWidget.addAction("Save", self.saveMessages)
        
        seperator = QAction(self)
        seperator.setSeparator(True)
        self.tableWidget.addAction(seperator)
        self.tableWidget.addAction("Delete Message", self.deleteMessage)
        self.tableWidget.setContextMenuPolicy(Qt.ContextMenuPolicy.ActionsContextMenu)
        
        self.setLayout(layout)

    
    def deleteMessage(self):
        selectedItems = self.tableWidget.selectedItems()
        if not selectedItems:
            return
        row = selectedItems[0].row()
        if QMessageBox.question(self, "Delete Message", "Are you sure you want to delete the selected message?") == QMessageBox.StandardButton.Yes:
            self.tableWidget.removeRow(row)



    def showMessageDialog(self, row=-1, messageData=None, name=""):
        if not self.messageEditDialog:
            self.messageEditDialog = MessageEditDialog(messageTemplateFilePath=self.messageTemplateFilePath)
        if messageData:
            self.messageEditDialog.setMessageData(messageData, name)
        if self.messageEditDialog.exec() == QDialog.DialogCode.Accepted:
            messageData = self.messageEditDialog.getMessageData()
            item = QTableWidgetItem(messageData[0])
            item.setData(Qt.ItemDataRole.UserRole, messageData[1])
            if row == -1:
                row = self.tableWidget.rowCount()
                self.tableWidget.insertRow(row)
            self.tableWidget.setItem(row , 0, item)
            self.tableWidget.setItem(row , 1, QTableWidgetItem(messageData[2]))



    def addMessage(self):
        self.showMessageDialog()



    def editMessage(self):
        selectedItems = self.tableWidget.selectedItems()
        if not selectedItems:
            return
        row = selectedItems[0].row()
        currentData = self.tableWidget.item(row, 0).data(Qt.ItemDataRole.UserRole)
        name = self.tableWidget.item(row, 1).text() if self.tableWidget.item(row, 1) else ""
        self.showMessageDialog(row, currentData, name)



    def loadMessages(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open Table File", "", "Message List Files (*.list);;All Files (*)")
        if not filename:
            return
        self.loadMessagesFromFile(filename)



    def loadMessagesFromFile(self, filename):
        self.tableWidget.setRowCount(0)
        with open(filename, 'r') as f:
            data = json.load(f)
            for messageData in data:
                row = self.tableWidget.rowCount()
                self.tableWidget.insertRow(row)
                item = QTableWidgetItem(messageData[0])
                item.setData(Qt.ItemDataRole.UserRole, messageData[1])
                self.tableWidget.setItem(row , 0, item)
                if len(messageData) > 2:
                    self.tableWidget.setItem(row , 1, QTableWidgetItem(messageData[2]))



    def saveMessages(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Save Table File", "", "Message List Files (*.list);;All Files (*)")
        if not filename:
            return
        self.saveMessagesToFile(filename)



    def saveMessagesToFile(self, filename):
        data = []
        for row in range(self.tableWidget.rowCount()):
            item = self.tableWidget.item(row, 0)
            name = self.tableWidget.item(row, 1).text()
            messageData = item.data(Qt.ItemDataRole.UserRole)
            data.append((item.text(), messageData, name))
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)


    
    def sendMessage(self):
        selectedItems = self.tableWidget.selectedItems()
        if not selectedItems:
            return
        row = selectedItems[0].row()
        message = self.tableWidget.item(row, 0).text()
        self.send_message.emit(message)