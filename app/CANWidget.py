from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,QComboBox, QTableWidget, QTableWidgetItem, QMessageBox, QLabel, QCheckBox, QLineEdit, QGroupBox
from PyQt6.QtCore import Qt, pyqtSignal
import can
from threading import Thread
from .MessageTemplateTableWidget import MessageTemplateTableWidget
from .utils import assets_path

class CANWidget(QWidget):
    
    message_received = pyqtSignal(str)

    def __init__(self, parent=None):
        super(CANWidget, self).__init__(parent)
        self.channel: str = None
        self.canBus: can.BusABC = None
        self.reader: can.BufferedReader = None
        self.notifier: can.Notifier = None
        self.thread: Thread = None
        self.initUI()

    def initUI(self):
        LINE_HEIGHT = 30
        layout = QVBoxLayout()
        self.setLayout(layout)

        configLayout = QHBoxLayout()
        layout.addLayout(configLayout)

        self.channelLabel = QLabel("Channel: Not Set")
        configLayout.addWidget(self.channelLabel)

        # Bus Type ComboBox
        configLayout.addWidget(QLabel("Bus Type:"), 1, Qt.AlignmentFlag.AlignRight)
        self.busTypeComboBox = QComboBox()
        self.busTypeComboBox.setMinimumWidth(200)
        self.busTypeComboBox.setFixedHeight(LINE_HEIGHT)
        self.busTypeComboBox.addItems(["slcan", "socketcan", "pcan", "zlgcan"])
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


        # Edit arbitration ID table
        arbitationIdLayout = QVBoxLayout()
        arbitationIdLayout.addWidget(QLabel("Arbitration IDs:"))
        self.arbitationIdTable = MessageTemplateTableWidget()
        self.arbitationIdTable.setButtonVisible(False)
        self.arbitationIdTable.setMinimumHeight(250)
        arbitationIdLayout.addWidget(self.arbitationIdTable)
        layout.addLayout(arbitationIdLayout)


        # Edit message data table
        dataLayout = QVBoxLayout()
        dataLayout.addWidget(QLabel("Message Data:"))
        self.msgDataTable = MessageTemplateTableWidget()
        self.msgDataTable.setButtonVisible(False)
        self.msgDataTable.setMinimumHeight(350)
        dataLayout.addWidget(self.msgDataTable)
        layout.addLayout(dataLayout)


        layout.addSpacing(10)
        arbitationLayout = QHBoxLayout()
        arbitationLayout.addWidget(QLabel("Arbitration ID:"))
        self.arbitrationIdEdit = QLineEdit()
        self.arbitrationIdEdit.setPlaceholderText("Enter Arbitration ID (e.g., '0xc0ffee')")
        self.arbitrationIdEdit.setFixedHeight(LINE_HEIGHT)
        arbitationLayout.addWidget(self.arbitrationIdEdit,2)
        arbitationLayout.addSpacing(100)

        self.extendedIdCheckBox = QCheckBox()
        self.extendedIdCheckBox.setChecked(True)
        self.extendedIdCheckBox.setText("Extended ID")
        arbitationLayout.addWidget(self.extendedIdCheckBox, 1)

        self.canFDCheckBox = QCheckBox()
        self.canFDCheckBox.setText("CAN FD")
        arbitationLayout.addWidget(self.canFDCheckBox, 1)

        layout.addLayout(arbitationLayout)

        layout.addSpacing(10)
        dataLayout = QHBoxLayout()
        dataLayout.addWidget(QLabel("Message Data:"))
        self.dataEdit = QLineEdit()
        self.dataEdit.setPlaceholderText("Enter data bytes separated by spaces (e.g., '0 25 0 1 3 1 4 1')")
        self.dataEdit.setFixedHeight(LINE_HEIGHT)
        dataLayout.addWidget(self.dataEdit)
        layout.addLayout(dataLayout)

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
        self.arbitationIdTable.loadTableFromFile(assets_path.get('config//default//CAN_Ext_ArbitationId.template'))
        self.msgDataTable.loadTableFromFile(assets_path.get('config//default//CAN_Ext_MsgData.template'))


         

    def setChannel(self, channel: str):
        if self.busTypeComboBox.isEnabled():
            self.channel = channel
            self.channelLabel.setText(f"Channel: <b>{channel}</b>")


    def cleanUp(self):
        if self.canBus is not None:
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
        self.msgDataTable.setButtonEnabled(True)

    def closedStatus(self):
        self.busTypeComboBox.setEnabled(True)
        self.bitrateComboBox.setEnabled(True)
        self.arbitrationIdEdit.setEnabled(False)
        self.dataEdit.setEnabled(False)
        self.extendedIdCheckBox.setEnabled(False)
        self.canFDCheckBox.setEnabled(False)
        self.openCanPushButton.setText("打开")
        self.sendButton.setEnabled(False)
        self.msgDataTable.setButtonEnabled(False)

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
            open_can_bus = Thread(target=self.open_can_bus, args=(interface, bitrate))
            open_can_bus.start()
            open_can_bus.join()

            self.reader = can.BufferedReader()
            self.notifier = can.Notifier(self.canBus, [self.reader])
            self.thread = Thread(target=self.receive_messages, daemon=True)
            self.thread.start()
            self.message_received.connect(self.display_message)
            
        except can.CanError as e:
            QMessageBox.critical(self, "Error", f"CAN bus open error: {e}")
            return
        self.openedStatus()
    
    def open_can_bus(self, interface: str, bitrate: int):
        self.canBus = can.interface.Bus(bustype=interface, channel=self.channel, bitrate=bitrate)
    
    def receive_messages(self):
        while self.canBus is not None:
            msg = self.reader.get_message(timeout=1.0)
            if msg is not None:
                self.message_received.emit(str(msg) + "\n")
    
    def display_message(self, msg: str):
        print(f"Received message: {msg}")


    def sendCANMessage(self):
        if self.canBus is None:
            QMessageBox.critical(self, "Error", "CAN bus not opened")
            return
        
        arbitration_id_hexStr: str = self.arbitationIdTable.encode().replace(" ", "")
        #print("arbitration_id:", arbitration_id_hexStr)
        arbitration_id = int(arbitration_id_hexStr, 16)
        self.arbitrationIdEdit.setText(hex(arbitration_id))

        message_data_hexStr: str = self.msgDataTable.encode().replace(" ", "")
        #print("message_data:", message_data_hexStr)
        try:
            data = bytes.fromhex(message_data_hexStr)
            self.dataEdit.setText(" ".join([str(b) for b in data]))
        except:
            QMessageBox.critical(self, "Error", f"Message data({message_data_hexStr}) not in bytes format")
            return
        msg = can.Message(arbitration_id=arbitration_id,
                        data=data,
                        is_extended_id=self.extendedIdCheckBox.isChecked())
        try:
            self.canBus.send(msg)
        except can.CanError:
            QMessageBox.critical(self, "Error", "Message NOT sent")
