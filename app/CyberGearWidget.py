from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QGridLayout, QTableWidget,QHeaderView, QTableWidgetItem, QFileDialog, QMessageBox
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QDialog
from PyQt6.QtCore import Qt, pyqtSignal
from .CanMessageEditWidget import CanMessageEditWidget
import json
import os
from .utils import assets_path

HEADERS = ["data", "name"]

class CyberGearWidget(QWidget):
    
    send_message = pyqtSignal(str)
    DEFAULT_FILE_PATH = 'config//default//CyberGearMessages.json'

    def __init__(self, parent=None):
        super(CyberGearWidget, self).__init__(parent)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        controlLayout = QHBoxLayout()
        startButton = QPushButton("开始控制")   
        startButton.setFixedWidth(100)
        startButton.clicked.connect(self.startControl)
        controlLayout.addWidget(startButton)

        cwButton = QPushButton("正向运行")
        cwButton.setFixedWidth(100)
        controlLayout.addWidget(cwButton)
        cwButton.pressed.connect(self.runForward)
        cwButton.released.connect(self.stopRun)

        ccwButton = QPushButton("反向运行")
        ccwButton.setFixedWidth(100)
        controlLayout.addWidget(ccwButton)
        ccwButton.pressed.connect(self.runBackward)
        ccwButton.released.connect(self.stopRun)
        
        layout.addLayout(controlLayout)

        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(len(HEADERS))
        self.tableWidget.setHorizontalHeaderLabels(HEADERS)
        self.tableWidget.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.tableWidget.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.tableWidget.setRowCount(0)
        
        layout.addWidget(self.tableWidget)
        self.tableWidget.addAction("Add Message", self.addMessage)
        self.tableWidget.addAction("Edit Message", self.editMessage)
        self.tableWidget.addAction("Delete Message", self.deleteMessage)
        self.tableWidget.addAction("Send Message", self.sendMessage)
        seperator = QAction(self)
        seperator.setSeparator(True)
        self.tableWidget.addAction(seperator)
        self.tableWidget.addAction("Load", self.loadMessages)
        self.tableWidget.addAction("Save", self.saveMessages)
        self.tableWidget.setContextMenuPolicy(Qt.ContextMenuPolicy.ActionsContextMenu)
        
        self.setLayout(layout)

        filename = assets_path.get(self.DEFAULT_FILE_PATH)
        if os.path.exists(filename):
            self.loadMessagesFromFile(filename)

        QApplication.instance().aboutToQuit.connect(self.cleanUp)

    def cleanUp(self):
        self.saveMessagesToFile(assets_path.get(self.DEFAULT_FILE_PATH))
    
    def deleteMessage(self):
        selectedItems = self.tableWidget.selectedItems()
        if not selectedItems:
            return
        row = selectedItems[0].row()
        if QMessageBox.question(self, "Delete Message", "Are you sure you want to delete the selected message?") == QMessageBox.StandardButton.Yes:
            self.tableWidget.removeRow(row)

    def showMessageDialog(self, row=-1, messageData=None, name=""):
        canMessageEditWidget = CanMessageEditWidget()
        if messageData:
            canMessageEditWidget.setMessageData(messageData, name)
        if canMessageEditWidget.exec() == QDialog.DialogCode.Accepted:
            messageData = canMessageEditWidget.getMessageData()
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
        filename, _ = QFileDialog.getOpenFileName(self, "Open Table File", "", "JSON Files (*.json);;All Files (*)")
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
        filename, _ = QFileDialog.getSaveFileName(self, "Save Table File", "", "JSON Files (*.json);;All Files (*)")
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
    
    def sendMessage(self, message = None):
        if not message:
            selectedItems = self.tableWidget.selectedItems()
            if not selectedItems:
                return
            row = selectedItems[0].row()
            message = self.tableWidget.item(row, 0).text()
        self.send_message.emit(message)


    def startControl(self):
        print("开始控制小米电机")
        self.sendMessage("41 54 2b 41 54 0d 0a")

    def runForward(self):
        print("小米电机正向运行")
        self.sendMessage("41 54 90 07 eb fc 08 05 70 00 00 07 01 95 54 0d 0a")
    
    def runBackward(self):
        print("小米电机反向运行")
        self.sendMessage("41 54 90 07 eb fc 08 05 70 00 00 07 01 6a aa 0d 0a")
    
    def stopRun(self):
        print("小米电机停止运行")
        self.sendMessage("41 54 90 07 eb fc 08 05 70 00 00 07 00 7f ff 0d 0a")
