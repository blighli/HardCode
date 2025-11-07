from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QLineEdit, QPushButton, QLabel, QComboBox, QMessageBox
from PyQt6.QtGui import QIcon
from PyQt6.QtSerialPort import QSerialPort, QSerialPortInfo
from .utils import assets_path, serial_port

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.port: QSerialPort | None = None
        self.initUI()


    def initUI(self):

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
        leftBox.addStretch()
        # Serial Port ComboBox
        self.portComboBox = QComboBox()
        self.portComboBox.setFixedWidth(200)
        portList = serial_port.get_port_names()
        for port in portList:
            self.portComboBox.addItem(port)
        # Baud Rate ComboBox
        self.baudRateComboBox = QComboBox()
        self.baudRateComboBox.setFixedWidth(100)
        self.baudRateComboBox.addItems(["9600", "19200", "38400", "57600", "115200", "230400", "460800", "921600"])
        self.baudRateComboBox.setCurrentIndex(4)  # Default to 115200
        # Connect Button
        self.portConnectButton = QPushButton("打开串口")
        self.portConnectButton.setFixedWidth(100)
        # Add widgets to portBox
        portBox.addWidget(self.portComboBox)
        portBox.addWidget(self.baudRateComboBox)
        portBox.addWidget(self.portConnectButton)

        # Connect Button Signal
        self.portConnectButton.clicked.connect(self.connectPort)

    def connectPort(self):
        # Serial Port Connection Logic
        if self.port is not None:
            self.port.close()
            self.port = None
            self.statusBar().showMessage("Serial port closed.")
            self.portComboBox.setEnabled(True)
            self.baudRateComboBox.setEnabled(True)
            self.portConnectButton.setText("打开串口")
            return
        # Connect to Serial Port
        port = self.portComboBox.currentText()
        baud_rate = int(self.baudRateComboBox.currentText())
        self.port = serial_port.connect(port, baud_rate)
        if self.port is not None:
            self.statusBar().showMessage(f"Connected to {port} at {baud_rate} baud.")
            self.portComboBox.setEnabled(False)
            self.baudRateComboBox.setEnabled(False)
            self.portConnectButton.setText("关闭串口")
        else:
            QMessageBox.critical(self, "Connection Error", f"Failed to connect to {port} at {baud_rate} baud.") 
