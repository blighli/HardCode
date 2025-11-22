from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QTabWidget, QTextEdit, QLineEdit, QPushButton, QLabel, QComboBox, QMessageBox, QCheckBox, QTableWidget, QTableWidgetItem, QFileDialog
from PyQt6.QtGui import QIcon
from PyQt6.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt6.QtCore import QByteArray

from app.GraphicsWidget import GraphicsWidget
from .utils import assets_path, serial_port
from .RangeWidget import RangeWidget
from .WebService import FastAPIServer
from .MessageTableWidget import MessageTableWidget
from .SerialPortWidget import SerialPortWidget
from .MessageDisplayWidget import MessageDisplayWidget
from .MessageEditWidget import MessageEditWidget
import json,pickle

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.configFileName = "config/config.txt"
        self.api_server = FastAPIServer()
        self.api_server.start()
        self.serialPort: QSerialPort | None = None
        self.graphicsWidget: GraphicsWidget = None
        self.initUI()
        self.loadAppConfig()
    
    def closeEvent(self, event):
        self.saveAppConfig()
        self.api_server.stop()
        event.accept()

    def initUI(self):
        self.createMenuBar()
        LINE_HEIGHT = 30
        # Main Window Settings
        self.setWindowIcon(QIcon(assets_path.get('assets//app.ico')))
        self.setWindowTitle("Hello from HardCode!")
        self.setGeometry(100, 100, 1200, 800)

        # Central Widget and Layouts
        central_widget = QWidget()

        self.tabWidget = QTabWidget()
        self.tabWidget.addTab(central_widget, "Common")
        self.tabWidget.addTab(GraphicsWidget(), "Graphics")
        self.tabWidget.addTab(QWidget(), "CAN")

        self.setCentralWidget(self.tabWidget)
        # Create Main Layouts
        mainBox = QHBoxLayout(central_widget)
        leftBox = QVBoxLayout()
        rightBox = QVBoxLayout()
        mainBox.addLayout(leftBox)
        mainBox.addLayout(rightBox)

        # Select Serial Port
        self.serialPortWidget = SerialPortWidget()
        leftBox.addWidget(self.serialPortWidget)
        self.serialPortWidget.port_open.connect(self.portOpen)
        self.serialPortWidget.port_close.connect(self.portClose)
        
        # Message Display Widget
        self.messageDisplay = MessageDisplayWidget()
        leftBox.addWidget(self.messageDisplay)

        # Message Edit Widget
        self.messageEditWidget = MessageEditWidget()
        self.messageEditWidget.message_send.connect(self.sendData)
        leftBox.addWidget(self.messageEditWidget)

        self.rangeWidget = RangeWidget(minValue=0, maxValue=100, value=50)
        self.rangeWidget.value_changed.connect(self.rangeValueChanged)
        leftBox.addWidget(self.rangeWidget)

        # Table View for Received Data
        self.readTable = MessageTableWidget()
        rightBox.addWidget(self.readTable)

        # OpenGL Graphics Widget
        # self.graphicsWidget = GraphicsWidget()
        # self.graphicsWidget.setMinimumWidth(300)
        # self.graphicsWidget.setMinimumHeight(300)
        # rightBox.addWidget(self.graphicsWidget, 1)
        
         # Table View for Sent Data
        self.sendTable = MessageTableWidget()
        rightBox.addWidget(self.sendTable)
        
        self.statusBar().showMessage("Ready!")

    def createMenuBar(self):
        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu("File")
        exitAction = fileMenu.addAction("Exit")
        exitAction.triggered.connect(self.close)

        viewsMenu = menuBar.addMenu("Views")
        drawAction = viewsMenu.addAction("OpenGL Classic")
        drawAction.triggered.connect(self.openDrawWindow)

        toolsMenu = menuBar.addMenu("Tools")
        settingsAction = toolsMenu.addAction("Settings")

        helpMenu = menuBar.addMenu("Help")
        aboutAction = helpMenu.addAction("About")

    def openDrawWindow(self):
        if self.graphicsWidget is None:
            self.graphicsWidget = GraphicsWidget()
            self.graphicsWidget.setWindowTitle("OpenGL Draw Window")
            self.graphicsWidget.setGeometry(150, 150, 800, 600)
        self.graphicsWidget.show()

    def rangeValueChanged(self, name, value):
        self.statusBar().showMessage(f"{name}={value}")

    def portOpen(self, port):
        self.serialPort = port
        self.serialPort.readyRead.connect(self.readData)
        self.messageEditWidget.setButtonEnabled(True)
        self.statusBar().showMessage(f"Connected to {port.portName()} at {port.baudRate()} baud.")

    def portClose(self):
        self.serialPort = None
        self.statusBar().showMessage("Serial port closed.")
        self.messageEditWidget.setButtonEnabled(False)

    def readData(self):
        if self.messageEditWidget.isHexChecked():
            data = self.serialPort.readAll()
            data = [x.hex() for x in data]
            self.messageDisplay.recv(" ".join(data) + "\n")  
        else:
            try:
                data = self.serialPort.readAll()
                data = str(data.data(), encoding='utf-8')
                self.messageDisplay.recv( data)
            except:
                self.messageDisplay.appendMessage("error\n")

    def sendData(self, data):
        if data and self.serialPort.isOpen():
            if self.messageEditWidget.isHexChecked():
                try:
                    byteArray = QByteArray(bytes.fromhex(data.replace(" ","")))
                except:
                    QMessageBox.critical(self, "Send Data Error", f"Not hex format data {data}") 
                    return
            else:
                byteArray = QByteArray(data.encode('utf-8'))
            
            self.serialPort.write(byteArray)
            # Echo Sent Message
            self.messageDisplay.send(data + "\n")
    
    def saveAppConfig(self):
        self.appConfig["hexChecked"] = self.messageEditWidget.isHexChecked()
        self.appConfig["baudRate"] = self.serialPortWidget.baudRate()
        self.appConfig["msgHistory"] = self.messageEditWidget.history()
        self.appConfig["tabSelectedIndex"] = self.tabWidget.currentIndex()
        with open(self.configFileName, 'w') as f:
            json.dump(self.appConfig, f, indent=4)

    
    def loadAppConfig(self):
        self.appConfig = {
            "hexChecked" : False,
            "baudRate" : 115200,
            "msgHistory": []
        }
        try:
            with open(self.configFileName, 'r') as f:
                self.appConfig = json.load(f)
                self.messageEditWidget.setHexChecked(self.appConfig["hexChecked"])
                self.serialPortWidget.setBaudRate(self.appConfig["baudRate"])
                self.messageEditWidget.setHistory(self.appConfig["msgHistory"])
                self.tabWidget.setCurrentIndex(self.appConfig.get("tabSelectedIndex", 0))
        except Exception as e:
            print(e)
