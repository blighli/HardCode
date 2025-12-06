from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QGridLayout, QTableWidget,QHeaderView, QTableWidgetItem, QFileDialog, QMessageBox
from PyQt6.QtCore import Qt, pyqtSignal
from .MessageListTableWidget import MessageListTableWidget
import os
from .utils import assets_path


class CyberGearWidget(QWidget):
    
    send_message = pyqtSignal(str)
    
    DEFAULT_MESSAGE_LIST_FILE_PATH = 'config//default//CyberGearMessages.json'
    DEFAULT_MESSAGE_TEMPLATE_FILE_PATH = 'config//default//USBCAN_AT.json'

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

        self.messageListWidget = MessageListTableWidget(messageTemplateFilePath=assets_path.get(self.DEFAULT_MESSAGE_TEMPLATE_FILE_PATH))
        self.messageListWidget.send_message.connect(self.sendMessage)
        layout.addWidget(self.messageListWidget)

        self.setLayout(layout)

        filename = assets_path.get(self.DEFAULT_MESSAGE_LIST_FILE_PATH)
        if os.path.exists(filename):
            self.messageListWidget.loadMessagesFromFile(filename)

        QApplication.instance().aboutToQuit.connect(self.cleanUp)



    def cleanUp(self):
        self.messageListWidget.saveMessagesToFile(assets_path.get(self.DEFAULT_FILE_PATH))


    
    def sendMessage(self, message):
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
