from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QTextEdit, QLineEdit, QPushButton, QLabel, QComboBox, QMessageBox
from PyQt6.QtGui import QIcon
from PyQt6.QtSerialPort import QSerialPort, QSerialPortInfo
from .utils import assets_path, serial_port
from .RangeWidget import RangeWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.serialPort: QSerialPort | None = None
        self.initUI()


    def initUI(self):
        LINE_HEIGHT = 30
        # Main Window Settings
        self.setWindowIcon(QIcon(assets_path.get('assets//app.ico')))
        self.setWindowTitle("Hello from HardCode!")
        self.setGeometry(100, 100, 800, 600)

        # Central Widget and Layouts
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        # Create Main Layouts
        mainBox = QHBoxLayout(central_widget)
        leftBox = QVBoxLayout()
        rightBox = QVBoxLayout()
        mainBox.addLayout(leftBox)
        mainBox.addLayout(rightBox)


        # Serial Port Selection
        portBox = QHBoxLayout()
        leftBox.addLayout(portBox)
        # Serial Port ComboBox
        self.portComboBox = QComboBox()
        self.portComboBox.setMinimumWidth(200)
        self.portComboBox.setFixedHeight(LINE_HEIGHT)
        portList = serial_port.get_port_names()
        for port in portList:
            self.portComboBox.addItem(port)
        # Baud Rate ComboBox
        self.baudRateComboBox = QComboBox()
        self.baudRateComboBox.setMinimumWidth(200)
        self.baudRateComboBox.setFixedHeight(LINE_HEIGHT)
        self.baudRateComboBox.addItems(["9600", "19200", "38400", "57600", "115200", "230400", "460800", "921600"])
        self.baudRateComboBox.setCurrentIndex(4)  # Default to 115200
        # Connect Button
        self.portConnectButton = QPushButton("打开串口")
        self.portConnectButton.setFixedWidth(100)
        self.portConnectButton.setFixedHeight(LINE_HEIGHT)
        # Add widgets to portBox
        portBox.addWidget(self.portComboBox)
        portBox.addWidget(self.baudRateComboBox)
        portBox.addWidget(self.portConnectButton)
        
        self.messageDisplay = QTextEdit()
        leftBox.addWidget(self.messageDisplay)

        self.messageEdit = QLineEdit()
        self.messageEdit.setFixedHeight(LINE_HEIGHT)
        self.messageSendButton = QPushButton("发送")
        self.messageSendButton.setFixedWidth(100)
        self.messageSendButton.setFixedHeight(LINE_HEIGHT)
        self.messageSendButton.setEnabled(False)
        sendBox = QHBoxLayout()
        sendBox.addWidget(self.messageEdit)
        sendBox.addWidget(self.messageSendButton)
        leftBox.addLayout(sendBox)

        self.rangeWidget = RangeWidget(minValue=0, maxValue=100, value=50)
        self.rangeWidget.value_changed.connect(self.rangeValueChanged)
        leftBox.addWidget(self.rangeWidget)

        # Connect Button Signal
        self.portConnectButton.clicked.connect(self.connectPort)
        
        self.statusBar().showMessage("Ready!")

    def rangeValueChanged(self, name, value):
        self.statusBar().showMessage(f"{name}={value}")

    def connectPort(self):
        # Serial Port Connection Logic
        if self.serialPort is not None:
            self.serialPort.close()
            self.serialPort = None
            self.statusBar().showMessage("Serial port closed.")
            self.portComboBox.setEnabled(True)
            self.baudRateComboBox.setEnabled(True)
            self.portConnectButton.setText("打开串口")
            self.messageSendButton.setEnabled(False)
            return
        # Connect to Serial Port
        port = self.portComboBox.currentText()
        baud_rate = int(self.baudRateComboBox.currentText())
        self.serialPort = serial_port.connect(port, baud_rate)
        if self.serialPort is not None:
            self.serialPort.readyRead.connect(self.readData)
            self.statusBar().showMessage(f"Connected to {port} at {baud_rate} baud.")
            self.portComboBox.setEnabled(False)
            self.baudRateComboBox.setEnabled(False)
            self.portConnectButton.setText("关闭串口")
            self.messageSendButton.setEnabled(True)
        else:
            QMessageBox.critical(self, "Connection Error", f"Failed to connect to {port} at {baud_rate} baud.") 

    def readData(self):
        try:
            data = self.serialPort.readAll()
            data = str(data.data(), encoding='utf-8')
            self.messageDisplay.setPlainText(self.messageDisplay.toPlainText() + data)
            self.messageDisplay.verticalScrollBar().setValue(
                self.messageDisplay.verticalScrollBar().maximum()
            )
        except:
            self.messageDisplay.append("error\n")