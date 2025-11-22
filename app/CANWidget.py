from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton,QComboBox, QTableWidget, QTableWidgetItem, QFrame
from PyQt6.QtCore import Qt
import can  # Assuming a CAN library is available

class CANWidget(QWidget):
    def __init__(self, parent=None):
        super(CANWidget, self).__init__(parent)
        self.initUI()

    def initUI(self):
        LINE_HEIGHT = 30
        layout = QVBoxLayout()

        configLayout = QHBoxLayout()
        layout.addLayout(configLayout)

        # Bus Type ComboBox
        self.busTypeComboBox = QComboBox()
        self.busTypeComboBox.setMinimumWidth(200)
        self.busTypeComboBox.setFixedHeight(LINE_HEIGHT)
        self.busTypeComboBox.addItems(["slcan", "socketcan", "pcan"])
        self.busTypeComboBox.setCurrentIndex(0)  # Default to slcan
        configLayout.addWidget(self.busTypeComboBox)

        # Bitrate ComboBox
        self.bitrateComboBox = QComboBox()
        self.bitrateComboBox.setMinimumWidth(200)
        self.bitrateComboBox.setFixedHeight(LINE_HEIGHT)
        self.bitrateComboBox.addItems(["125000", "250000", "500000", "1000000"])
        self.bitrateComboBox.setCurrentIndex(2)  # Default to 500000
        configLayout.addWidget(self.bitrateComboBox)

        sendTable = QTableWidget()

        sendTable.setColumnCount(1)
        sendTable.setRowCount(9)
        item = QTableWidgetItem("Arbitration ID")
        item.setTextAlignment(Qt.AlignmentFlag.AlignRight)
        sendTable.setVerticalHeaderItem(0,item)
        for i in range(8):
            item = QTableWidgetItem(f"Data Byte {i+1}")
            item.setTextAlignment(Qt.AlignmentFlag.AlignRight)
            sendTable.setVerticalHeaderItem(i + 1, item)
        
        sendTable.verticalHeader().setFixedWidth(100)
        sendTable.setHorizontalHeaderItem(0, QTableWidgetItem("Value"))
        sendTable.horizontalHeader().setStretchLastSection(True)
        

        layout.addWidget(sendTable)

        self.sendButton = QPushButton("Send CAN Message")
        self.sendButton.clicked.connect(self.sendCANMessage)

        layout.addWidget(self.sendButton)

        self.setLayout(layout)

    def sendCANMessage(self):
        print("Initializing CAN bus...")
        bus = can.interface.Bus(bustype='slcan', channel='COM3', bitrate=500000)
        print("Sending CAN message...")
        msg = can.Message(arbitration_id=0xc0ffee,
                        data=[0, 25, 0, 1, 3, 1, 4, 1],
                        is_extended_id=True)
        print("Prepared CAN message.")
        try:
            bus.send(msg)
            print("Message sent on {}".format(bus.channel_info))
        except can.CanError:
            print("Message NOT sent")