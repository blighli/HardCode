from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QTextEdit, QLineEdit, QPushButton, QLabel, QComboBox, QMessageBox, QCheckBox, QTableWidget, QTableWidgetItem, QFileDialog
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
import json

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.api_server = FastAPIServer()
        self.api_server.start()
        self.serialPort: QSerialPort | None = None
        self.graphicsWidget: GraphicsWidget = None
        self.initUI()
    
    def closeEvent(self, event):
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
        self.setCentralWidget(central_widget)
        # Create Main Layouts
        mainBox = QHBoxLayout(central_widget)
        leftBox = QVBoxLayout()
        rightBox = QVBoxLayout()
        mainBox.addLayout(leftBox)
        mainBox.addLayout(rightBox)

        # Select Serial Port
        serialPortWidget = SerialPortWidget()
        leftBox.addWidget(serialPortWidget)
        serialPortWidget.port_open.connect(self.portOpen)
        serialPortWidget.port_close.connect(self.portClose)
        
        self.messageDisplay = MessageDisplayWidget()
        leftBox.addWidget(self.messageDisplay)

        self.messageEditWidget = MessageEditWidget()
        self.messageEditWidget.message_send.connect(self.sendData)
        leftBox.addWidget(self.messageEditWidget)

        self.rangeWidget = RangeWidget(minValue=0, maxValue=100, value=50)
        self.rangeWidget.value_changed.connect(self.rangeValueChanged)
        leftBox.addWidget(self.rangeWidget)

        # Table View for Received Data
        self.readTable = MessageTableWidget()
        rightBox.addWidget(self.readTable)

        self.graphicsWidget = GraphicsWidget()
        #self.graphicsWidget.setFixedWidth(400)
        self.graphicsWidget.setMinimumHeight(200)
        rightBox.addWidget(self.graphicsWidget)

        self.sendTable = MessageTableWidget()
        rightBox.addWidget(self.sendTable)
        
        self.statusBar().showMessage("Ready!")

    def createMenuBar(self):
        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu("File")
        exitAction = fileMenu.addAction("Exit")
        exitAction.triggered.connect(self.close)

        toolsMenu = menuBar.addMenu("Tools")
        drawAction = toolsMenu.addAction("Draw")
        drawAction.triggered.connect(self.openDrawWindow)
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
            self.messageDisplay.appendMessage(" ".join(data) + "\n")  
        else:
            try:
                data = self.serialPort.readAll()
                data = str(data.data(), encoding='utf-8')
                self.messageDisplay.appendMessage(data)
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
            self.messageDisplay.appendMessage(data + "\n")
    

