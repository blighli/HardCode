from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,QComboBox, QTableWidget, QTableWidgetItem, QMessageBox, QLabel, QCheckBox, QLineEdit
from PyQt6.QtCore import Qt

import can  # Assuming a CAN library is available

class CANWidget(QWidget):
    def __init__(self, parent=None):
        super(CANWidget, self).__init__(parent)
        self.channel: str = None
        self.canBus: can.BusABC = None
        self.initUI()

    def initUI(self):
        LINE_HEIGHT = 30
        layout = QVBoxLayout()
        self.setLayout(layout)

        layout.addSpacing(20)
        configLayout = QHBoxLayout()
        layout.addLayout(configLayout)

        # Bus Type ComboBox
        configLayout.addWidget(QLabel("Bus Type:"), 1, Qt.AlignmentFlag.AlignRight)
        self.busTypeComboBox = QComboBox()
        self.busTypeComboBox.setMinimumWidth(200)
        self.busTypeComboBox.setFixedHeight(LINE_HEIGHT)
        self.busTypeComboBox.addItems(["slcan", "socketcan", "pcan"])
        self.busTypeComboBox.setCurrentIndex(0)  # Default to slcan
        configLayout.addWidget(self.busTypeComboBox, 3)

        # Bitrate ComboBox
        configLayout.addWidget(QLabel("Bitrate:"), 1, Qt.AlignmentFlag.AlignRight)
        self.bitrateComboBox = QComboBox()
        self.bitrateComboBox.setMinimumWidth(200)
        self.bitrateComboBox.setFixedHeight(LINE_HEIGHT)
        self.bitrateComboBox.addItems(["125000", "250000", "500000", "1000000"])
        self.bitrateComboBox.setCurrentIndex(2)  # Default to 500000
        configLayout.addWidget(self.bitrateComboBox, 3)

        self.openCanPushButton = QPushButton("打开")
        self.openCanPushButton.setFixedWidth(100)
        self.openCanPushButton.setFixedHeight(LINE_HEIGHT)
        self.openCanPushButton.clicked.connect(self.openCan)
        configLayout.addWidget(self.openCanPushButton)

        layout.addSpacing(20)
        arbitationLayout = QHBoxLayout()
        arbitationLayout.addWidget(QLabel("Arbitration ID:"))
        self.arbitrationIdEdit = QLineEdit()
        self.arbitrationIdEdit.setPlaceholderText("Enter Arbitration ID (e.g., '0x1AB')")
        self.arbitrationIdEdit.setFixedHeight(LINE_HEIGHT)
        arbitationLayout.addWidget(self.arbitrationIdEdit,2)

        arbitationLayout.addSpacing(100)

        self.extendedIdCheckBox = QCheckBox()
        self.extendedIdCheckBox.setText("Extended ID")
        arbitationLayout.addWidget(self.extendedIdCheckBox, 1)

        self.canFDCheckBox = QCheckBox()
        self.canFDCheckBox.setText("CAN FD")
        arbitationLayout.addWidget(self.canFDCheckBox, 1)

        layout.addLayout(arbitationLayout)

        layout.addSpacing(20)
        dataLayout = QHBoxLayout()
        dataLayout.addWidget(QLabel("Data:"))
        self.dataEdit = QLineEdit()
        self.dataEdit.setPlaceholderText("Enter data bytes separated by spaces (e.g., '0 25 0 1 3 1 4 1')")
        self.dataEdit.setFixedHeight(LINE_HEIGHT)
        dataLayout.addWidget(self.dataEdit)
        layout.addLayout(dataLayout)

        # sendTable = QTableWidget()

        # sendTable.setColumnCount(1)
        # sendTable.setRowCount(9)
        # item = QTableWidgetItem("Arbitration ID")
        # item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        # sendTable.setVerticalHeaderItem(0,item)
        # for i in range(8):
        #     item = QTableWidgetItem(f"Data Byte {i+1}")
        #     item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        #     sendTable.setVerticalHeaderItem(i + 1, item)
        
        # sendTable.verticalHeader().setFixedWidth(100)
        # sendTable.setHorizontalHeaderItem(0, QTableWidgetItem("Value"))
        # sendTable.horizontalHeader().setStretchLastSection(True)
        

        # layout.addWidget(sendTable)

        layout.addSpacing(20)
        self.sendButton = QPushButton("Send CAN Message")
        self.sendButton.setFixedHeight(LINE_HEIGHT)
        self.sendButton.setFixedWidth(150)
        self.sendButton.clicked.connect(self.sendCANMessage)

        layout.addWidget(self.sendButton)
        layout.setAlignment(self.sendButton, Qt.AlignmentFlag.AlignCenter)

        layout.addStretch()
        self.closedStatus()

        QApplication.instance().aboutToQuit.connect(self.cleanUp)

    def cleanUp(self):
        if self.canBus is not None:
            print("Shutdown canbus")
            self.canBus.shutdown()
            self.canBus = None

    def openedStatus(self):
        self.busTypeComboBox.setEnabled(False)
        self.bitrateComboBox.setEnabled(False)
        self.arbitrationIdEdit.setEnabled(True)
        self.dataEdit.setEnabled(True)
        self.extendedIdCheckBox.setEnabled(True)
        self.canFDCheckBox.setEnabled(True)
        self.openCanPushButton.setText("关闭")
        self.sendButton.setEnabled(True)

    def closedStatus(self):
        self.busTypeComboBox.setEnabled(True)
        self.bitrateComboBox.setEnabled(True)
        self.arbitrationIdEdit.setEnabled(False)
        self.dataEdit.setEnabled(False)
        self.extendedIdCheckBox.setEnabled(False)
        self.canFDCheckBox.setEnabled(False)
        self.openCanPushButton.setText("打开")
        self.sendButton.setEnabled(False)

    def openCan(self):
        if self.canBus is not None:
            self.canBus.shutdown()
            self.canBus = None
            self.closedStatus()
            return
        interface = self.busTypeComboBox.currentText()
        bitrate = int(self.bitrateComboBox.currentText())
        if not self.channel:
            QMessageBox.warning(self, "Warning", "CAN channel not set.")
            return
        try:
            self.canBus = can.interface.Bus(bustype=interface, channel=self.channel, bitrate=bitrate)
        except:
            QMessageBox.critical(self, "Error", "CAN bus open error")
            return
        self.openedStatus()


    def sendCANMessage(self):
        if self.canBus == None:
            QMessageBox.critical(self, "Error", "CAN bus not opened")
            return
        
        try:
            arbitration_id = int(self.arbitrationIdEdit.text(), 16)
        except:
            QMessageBox.critical(self, "Error", f"Message arbitration_id({self.arbitrationIdEdit.text()}) not in hex format")
            return
        
        try:
            data = [int(item) for item in self.dataEdit.text().split(" ")]
        except:
            QMessageBox.critical(self, "Error", f"Message data({self.dataEdit.text()}) not in bytes format")
            return

        msg = can.Message(arbitration_id=arbitration_id,
                        data=data,
                        is_extended_id=self.extendedIdCheckBox.isChecked())
        print("Message: {}".format(msg))
        try:
            self.canBus.send(msg)
        except can.CanError:
            QMessageBox.critical(self, "Error", "Message NOT sent")

    def setChannel(self, channel: str):
        self.channel = channel