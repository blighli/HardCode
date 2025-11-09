from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QTextEdit, QLineEdit, QPushButton, QLabel, QComboBox, QMessageBox, QCheckBox, QTableWidget, QTableWidgetItem, QFileDialog
from PyQt6.QtGui import QIcon
from PyQt6.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt6.QtCore import QByteArray
from .utils import assets_path, serial_port
from .RangeWidget import RangeWidget
from .WebService import FastAPIServer
import json

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.api_server = FastAPIServer()
        self.api_server.start()

        # f = open(assets_path.get("assets/web/index.html"), 'r')
        # self.html_content = f.read()
        # f.close()
        # print("Loaded HTML content length:", len(self.html_content))

        self.serialPort: QSerialPort | None = None
        self.initUI()
    
    def closeEvent(self, event):
        self.api_server.stop()
        event.accept()

    def initUI(self):
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


        # Serial Port Selection
        portBox = QHBoxLayout()
        leftBox.addLayout(portBox)
        # Serial Port ComboBox
        self.portComboBox = QComboBox()
        self.portComboBox.setMinimumWidth(200)
        self.portComboBox.setFixedHeight(LINE_HEIGHT)
        portList = serial_port.get_serial_ports()
        for port in portList:
            self.portComboBox.addItem(f"{port.portName()} - [ {port.description()} , {port.manufacturer()} ]", port)
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
        self.hexCheckBox = QCheckBox()
        self.hexCheckBox.setText("Hex")

        sendBox = QHBoxLayout()
        sendBox.addWidget(self.messageEdit)
        sendBox.addWidget(self.messageSendButton)
        sendBox.addWidget(self.hexCheckBox)
        leftBox.addLayout(sendBox)

        self.rangeWidget = RangeWidget(minValue=0, maxValue=100, value=50)
        self.rangeWidget.value_changed.connect(self.rangeValueChanged)
        leftBox.addWidget(self.rangeWidget)

        tableHeaders = ["pos", "len", "type", "name", "value"]
        self.readTableView = QTableWidget()
        rightBox.addWidget(self.readTableView)
        self.readTableView.setColumnCount(len(tableHeaders))
        self.readTableView.setHorizontalHeaderLabels(tableHeaders)
        self.readTableView.horizontalHeader().setStretchLastSection(True)   
        
        self.addButton = QPushButton("add")
        self.addButton.setFixedWidth(100)
        self.addButton.setFixedHeight(LINE_HEIGHT)
        self.addButton.clicked.connect(self.addRow)

        self.delButton = QPushButton("del")
        self.delButton.setFixedWidth(100)
        self.delButton.setFixedHeight(LINE_HEIGHT)
        self.delButton.clicked.connect(self.deleteRow)

        self.loadButton = QPushButton("load")
        self.loadButton.setFixedWidth(100)
        self.loadButton.setFixedHeight(LINE_HEIGHT)
        self.loadButton.clicked.connect(self.loadTable)

        self.saveButton = QPushButton("save")
        self.saveButton.setFixedWidth(100)
        self.saveButton.setFixedHeight(LINE_HEIGHT)
        self.saveButton.clicked.connect(self.saveTable)

        buttonBox = QHBoxLayout()
        buttonBox.addStretch()
        buttonBox.addWidget(self.addButton)
        buttonBox.addWidget(self.delButton)
        buttonBox.addWidget(self.loadButton)
        buttonBox.addWidget(self.saveButton)
        buttonBox.addStretch()
        rightBox.addLayout(buttonBox)



        self.sendTableView = QTableWidget()
        rightBox.addWidget(self.sendTableView)
        self.sendTableView.setColumnCount(len(tableHeaders))
        self.sendTableView.setHorizontalHeaderLabels(tableHeaders)


        # Connect Button Signal
        self.portConnectButton.clicked.connect(self.connectPort)
        self.messageSendButton.clicked.connect(self.sendData)
        
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
        port = self.portComboBox.currentData()
        baud_rate = int(self.baudRateComboBox.currentText())
        self.serialPort = serial_port.connect(port, baud_rate)
        if self.serialPort is not None:
            self.serialPort.readyRead.connect(self.readData)
            self.statusBar().showMessage(f"Connected to {port.portName()} at {baud_rate} baud.")
            self.portComboBox.setEnabled(False)
            self.baudRateComboBox.setEnabled(False)
            self.portConnectButton.setText("关闭串口")
            self.messageSendButton.setEnabled(True)
        else:
            QMessageBox.critical(self, "Connection Error", f"Failed to connect to {port} at {baud_rate} baud.") 

    def readData(self):
        if self.hexCheckBox.isChecked():
            data = self.serialPort.readAll()
            
            data = [ x.hex() for x in data]
            
            self.messageDisplay.setPlainText(self.messageDisplay.toPlainText() + " ".join(data) + "\n")
            self.messageDisplay.verticalScrollBar().setValue(
                self.messageDisplay.verticalScrollBar().maximum()
            )
            
        else:
            try:
                data = self.serialPort.readAll()
                data = str(data.data(), encoding='utf-8')
                self.messageDisplay.setPlainText(self.messageDisplay.toPlainText() + data)
                self.messageDisplay.verticalScrollBar().setValue(
                    self.messageDisplay.verticalScrollBar().maximum()
                )
            except:
                self.messageDisplay.append("error\n")

    def sendData(self):
        
        data = self.messageEdit.text()
        if data and self.serialPort.isOpen():
            if self.hexCheckBox.isChecked():
                try:
                    byteArray = QByteArray(bytes.fromhex(data.replace(" ","")))
                except:
                    QMessageBox.critical(self, "Send Data Error", f"Not hex format data {data}") 
                    return
            else:
                byteArray = QByteArray(data.encode('utf-8'))
            
            self.serialPort.write(byteArray)
            # Echo Sent Message
            self.messageDisplay.setPlainText(self.messageDisplay.toPlainText() + data + "\n")
            self.messageDisplay.verticalScrollBar().setValue(
                self.messageDisplay.verticalScrollBar().maximum()
            )

    def addRow(self):
        rowPosition = self.readTableView.rowCount()
        self.readTableView.insertRow(rowPosition)
        for col in range(self.readTableView.columnCount()):
            self.readTableView.setItem(rowPosition, col, QTableWidgetItem(""))
    
    def deleteRow(self):
        selectedRows = set()
        for item in self.readTableView.selectedItems():
            selectedRows.add(item.row())
        for row in sorted(selectedRows, reverse=True):
            self.readTableView.removeRow(row)
    
    def loadTable(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open Table File", "", "JSON Files (*.json);;All Files (*)")
        if not filename:
            return
        
        with open(filename, 'r') as f:
            data = json.load(f)
        self.readTableView.setRowCount(0)
        for row in data:
            self.addRow()
            for col, value in enumerate(row):
                self.readTableView.setItem(self.readTableView.rowCount()-1, col, QTableWidgetItem(str(value)))
    
    def saveTable(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Save Table File", "", "JSON Files (*.json);;All Files (*)")
        if not filename:
            return
        
        data = []
        for row in range(self.readTableView.rowCount()):
            rowData = []
            for col in range(self.readTableView.columnCount()):
                item = self.readTableView.item(row, col)
                rowData.append(item.text() if item else "")
            data.append(rowData)
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
    
    def refreshSerialPorts(self):
        self.portComboBox.clear()
        portList = serial_port.get_serial_ports()
        for port in portList:
            self.portComboBox.addItem(f"{port.portName()} - [ {port.description()} , {port.manufacturer()} ]", port)
