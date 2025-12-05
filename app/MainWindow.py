from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QTabWidget, QTextEdit, QLineEdit, QPushButton, QLabel, QComboBox, QMessageBox, QCheckBox, QTableWidget, QTableWidgetItem, QFileDialog
from PyQt6.QtGui import QIcon
from PyQt6.QtSerialPort import QSerialPort
from PyQt6.QtNetwork import QTcpSocket

from PyQt6.QtCore import QByteArray

from .utils import assets_path
from .GraphicsWidget import GraphicsWidget
from .VisionWidget import VisionWidget

from .RangeWidget import RangeWidget
from .WebService import FastAPIServer
from .SerialPortWidget import SerialPortWidget
from .SocketPortWidget import SocketPortWidget
from .MessageDisplayWidget import MessageDisplayWidget
from .MessageEditWidget import MessageEditWidget
from .CommonWidget import CommonWidget
from .CANWidget import CANWidget
from .CyberGearWidget import CyberGearWidget

import json

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.configFileName = assets_path.get("config/config.txt")
        self.api_server = FastAPIServer()
        self.api_server.start()
        self.serialPort: QSerialPort | None = None
        self.socketPort: QTcpSocket | None = None
        self.initUI()
        self.loadAppConfig()
    
    def closeEvent(self, event):
        self.saveAppConfig()
        self.api_server.stop()
        event.accept()

    def initUI(self):
        self.graphicsWidget: GraphicsWidget = None
        self.visionWidget: VisionWidget = None
        self.createMenuBar()
        LINE_HEIGHT = 30
        # Main Window Settings
        self.setWindowIcon(QIcon(assets_path.get('assets//app.ico')))
        self.setWindowTitle("Hello from HardCode!")
        self.resize(1200, 800)

        # Central Widget and Layouts
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Create Main Layouts
        mainBox = QHBoxLayout(central_widget)
        leftBox = QVBoxLayout()
        rightBox = QVBoxLayout()
        mainBox.addLayout(leftBox)
        mainBox.addLayout(rightBox)

        self.portTabWidget = QTabWidget()
        # Select Serial Port
        self.serialPortWidget = SerialPortWidget()
        self.serialPortWidget.port_open.connect(self.portOpen)
        self.serialPortWidget.port_close.connect(self.portClose)
        self.portTabWidget.addTab(self.serialPortWidget, "串口")
        # Select Socket Port
        self.socketPortWidget = SocketPortWidget()
        self.portTabWidget.addTab(self.socketPortWidget, "网络")
        self.socketPortWidget.port_open.connect(self.socketOpen)
        self.socketPortWidget.port_close.connect(self.socketClose)
        leftBox.addWidget(self.portTabWidget)

        # Message Display Widget
        self.messageDisplay = MessageDisplayWidget()
        leftBox.addWidget(self.messageDisplay,stretch=1)

        # Message Edit Widget
        self.messageEditWidget = MessageEditWidget()
        self.messageEditWidget.message_send.connect(self.sendData)
        leftBox.addWidget(self.messageEditWidget)

        # self.rangeWidget = RangeWidget(minValue=0, maxValue=100, value=50)
        # self.rangeWidget.value_changed.connect(self.rangeValueChanged)
        # leftBox.addWidget(self.rangeWidget)

        # Create Tab Widget
        self.tabWidget = QTabWidget()
        rightBox.addWidget(self.tabWidget)
        
        self.commonWidget = CommonWidget()
        self.commonWidget.send_message.connect(self.messageEditWidget.sendMessage)
        self.tabWidget.addTab(self.commonWidget, "通用")

        self.cyberGearWidget = CyberGearWidget()
        self.cyberGearWidget.send_message.connect(self.messageEditWidget.sendMessage)
        self.tabWidget.addTab(self.cyberGearWidget, "小米电机")

        self.canWidget = CANWidget()
        self.serialPortWidget.port_select_changed.connect(self.canWidget.setChannel)
        self.canWidget.message_received.connect(self.messageDisplay.recv)
        self.tabWidget.addTab(self.canWidget, "CAN")

        self.graphicsWidget = GraphicsWidget()
        self.graphicsWidget.setMinimumWidth(800)
        self.tabWidget.addTab(self.graphicsWidget, "图形")

        self.visionWidget = VisionWidget()
        self.visionWidget.setMinimumWidth(800)
        self.tabWidget.addTab(self.visionWidget, "视觉")

        self.statusBar().showMessage("Ready!")


    def createMenuBar(self):
        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu("File")
        openSerialAction = fileMenu.addAction("Open Serial")
        openSerialAction.triggered.connect(self.openSerialPortDialog)
        openSocketAction = fileMenu.addAction("Open Socket")
        openSocketAction.triggered.connect(self.openSocketDialog)
        exitAction = fileMenu.addAction("Exit")
        exitAction.triggered.connect(self.close)

        viewsMenu = menuBar.addMenu("Views")
        drawAction = viewsMenu.addAction("OpenGL")
        drawAction.triggered.connect(self.openDrawWindow)
        visionAction = viewsMenu.addAction("Vision")
        visionAction.triggered.connect(self.openVisionWindow)

        toolsMenu = menuBar.addMenu("Tools")
        settingsAction = toolsMenu.addAction("Settings")

        helpMenu = menuBar.addMenu("Help")
        aboutAction = helpMenu.addAction("About")


    def openSerialPortDialog(self):
        pass


    def openSocketDialog(self):
        pass


    def openDrawWindow(self):
        self.graphicsWidget2 = GraphicsWidget()
        self.graphicsWidget2.setWindowTitle("OpenGL Draw Window")
        self.graphicsWidget2.setGeometry(150, 150, 800, 600)
        self.graphicsWidget2.show()

    def openVisionWindow(self):
        self.visionWidget2 = VisionWidget()
        self.visionWidget2.setWindowTitle("Vision Window")
        self.visionWidget2.setGeometry(200, 200, 800, 600)
        self.visionWidget2.show()

    def rangeValueChanged(self, name, value):
        self.statusBar().showMessage(f"{name}={value}")

    def socketOpen(self, socket: QTcpSocket):
        self.socketPort = socket
        self.socketPort.readyRead.connect(self.readData)
        self.messageEditWidget.setButtonEnabled(True)
        self.statusBar().showMessage(f"Connected to {socket.peerAddress().toString()}:{socket.peerPort()}.")
        self.portTabWidget.setTabEnabled(0, False)

    def socketClose(self):
        self.socketPort = None
        self.statusBar().showMessage("Socket closed.")
        self.messageEditWidget.setButtonEnabled(False)
        self.portTabWidget.setTabEnabled(0, True)

    def portOpen(self, port):
        self.serialPort = port
        self.serialPort.readyRead.connect(self.readData)
        self.messageEditWidget.setButtonEnabled(True)
        self.statusBar().showMessage(f"Connected to {port.portName()} at {port.baudRate()} baud.")
        self.portTabWidget.setTabEnabled(1, False)

    def portClose(self):
        self.serialPort = None
        self.statusBar().showMessage("Serial port closed.")
        self.messageEditWidget.setButtonEnabled(False)
        self.portTabWidget.setTabEnabled(1, True)

    def readData(self):
        data = self.serialPort.readAll() if self.serialPort and self.serialPort.isOpen() else self.socketPort.readAll()
        if self.messageDisplay.isHexMode():
            data = [x.hex() for x in data]
            self.messageDisplay.recv(" ".join(data) + "\n")  
        else:
            try:
                data = str(data.data(), encoding='utf-8')
                self.messageDisplay.recv( data)
            except:
                self.messageDisplay.appendMessage("error\n")

    def sendData(self, data):
        if data and (self.serialPort and self.serialPort.isOpen() or self.socketPort and self.socketPort.state() == QTcpSocket.SocketState.ConnectedState):
            if self.messageEditWidget.isHexChecked():
                try:
                    byteArray = QByteArray(bytes.fromhex(data.replace(" ","")))
                except:
                    QMessageBox.critical(self, "Send Data Error", f"Not hex format data {data}") 
                    return
            else:
                data = data.replace('<CR>', '\r').replace('<LF>', '\n')
                byteArray = QByteArray(data.encode('utf-8'))
                if self.messageEditWidget.isCarriageReturnChecked():
                    byteArray.append(b'\r')
                if self.messageEditWidget.isLineFeedChecked():
                    byteArray.append(b'\n')
            
            if self.socketPort and self.socketPort.state() == QTcpSocket.SocketState.ConnectedState:
                self.socketPort.write(byteArray)
            else:
                self.serialPort.write(byteArray)
            # Echo Sent Message
            self.messageDisplay.send(data + "\n")
    
    def saveAppConfig(self):
        self.appConfig["hexChecked"] = self.messageEditWidget.isHexChecked()
        self.appConfig["carriageReturnChecked"] = self.messageEditWidget.isCarriageReturnChecked()
        self.appConfig["lineFeedChecked"] = self.messageEditWidget.isLineFeedChecked()
        self.appConfig["baudRate"] = self.serialPortWidget.baudRate()
        self.appConfig["msgHistory"] = self.messageEditWidget.history()
        self.appConfig["tabSelectedIndex"] = self.tabWidget.currentIndex()
        with open(self.configFileName, 'w') as f:
            json.dump(self.appConfig, f, indent=4)

    
    def loadAppConfig(self):
        self.appConfig = {
            "hexChecked" : False,
            "carriageReturnChecked": False,
            "lineFeedChecked": False,
            "baudRate" : 115200,
            "msgHistory": []
        }
        try:
            with open(self.configFileName, 'r') as f:
                self.appConfig = json.load(f)
                self.messageEditWidget.setHexChecked(self.appConfig["hexChecked"])
                self.messageEditWidget.setCarriageReturnChecked(self.appConfig["carriageReturnChecked"])
                self.messageEditWidget.setLineFeedChecked(self.appConfig["lineFeedChecked"])
                self.serialPortWidget.setBaudRate(self.appConfig["baudRate"])
                self.messageEditWidget.setHistory(self.appConfig["msgHistory"])
                self.tabWidget.setCurrentIndex(self.appConfig.get("tabSelectedIndex", 0))
        except Exception as e:
            print(e)
