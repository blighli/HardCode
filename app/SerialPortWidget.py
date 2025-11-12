from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QPushButton, QMessageBox
from PyQt6.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt6.QtCore import Qt, pyqtSignal
from .utils import serial_port

class SerialPortWidget(QWidget):

    port_open = pyqtSignal(QSerialPort)
    port_close = pyqtSignal()

    def __init__(self, parent=None):
        super(SerialPortWidget, self).__init__(parent)

        self.serialPort: QSerialPort | None = None

        LINE_HEIGHT = 30

        layout = QHBoxLayout()
        self.setLayout(layout)
        # Serial Port ComboBox
        self.portComboBox = QComboBox()
        self.portComboBox.setMinimumWidth(200)
        self.portComboBox.setFixedHeight(LINE_HEIGHT)
        self.refreshSerialPorts()
        # Baud Rate ComboBox
        self.baudRateComboBox = QComboBox()
        self.baudRateComboBox.setMinimumWidth(200)
        self.baudRateComboBox.setFixedHeight(LINE_HEIGHT)
        self.baudRateComboBox.addItems(["9600", "19200", "38400", "57600", "115200", "230400", "460800", "500000", "921600"])
        self.baudRateComboBox.setCurrentIndex(4)  # Default to 115200
        # Connect Button
        self.portConnectButton = QPushButton("打开串口")
        self.portConnectButton.setFixedWidth(100)
        self.portConnectButton.setFixedHeight(LINE_HEIGHT)
        # Refresh Button
        self.portRefreshButton = QPushButton("刷新串口")
        self.portRefreshButton.setFixedWidth(100)
        self.portRefreshButton.setFixedHeight(LINE_HEIGHT)
        # Add widgets to layout
        layout.addWidget(self.portComboBox)
        layout.addWidget(self.baudRateComboBox)
        layout.addWidget(self.portConnectButton)
        layout.addWidget(self.portRefreshButton)

        self.portConnectButton.clicked.connect(self.connectPort)
        self.portRefreshButton.clicked.connect(self.refreshSerialPorts)

    def baudRate(self):
        return int(self.baudRateComboBox.currentText())
    
    def setBaudRate(self, baudRate):
        self.baudRateComboBox.setCurrentText(str(baudRate))

    def refreshSerialPorts(self):
        self.portComboBox.clear()
        portList = serial_port.get_serial_ports()
        for port in portList:
            self.portComboBox.addItem(f"{port.portName()} - [ {port.description()} , {port.manufacturer()} ]", port)

    def connectPort(self):
        # Serial Port Connection Logic
        if self.serialPort is not None:
            self.serialPort.close()
            self.serialPort = None
            self.portComboBox.setEnabled(True)
            self.baudRateComboBox.setEnabled(True)
            self.portConnectButton.setText("打开串口")
            self.port_close.emit()
            return
        # Connect to Serial Port
        port = self.portComboBox.currentData()
        baud_rate = int(self.baudRateComboBox.currentText())
        self.serialPort = serial_port.connect(port, baud_rate)
        if self.serialPort is not None:
            self.portComboBox.setEnabled(False)
            self.baudRateComboBox.setEnabled(False)
            self.portConnectButton.setText("关闭串口")
            self.port_open.emit(self.serialPort)
        else:
            QMessageBox.critical(self, "Connection Error", f"Failed to connect to {port.portName()} at {baud_rate} baud.")