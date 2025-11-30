from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QComboBox, QPushButton, QMessageBox
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtNetwork import QTcpSocket, QHostAddress

class SocketPortWidget(QWidget):

    port_open = pyqtSignal(QTcpSocket)
    port_close = pyqtSignal()

    def __init__(self, parent=None):
        super(SocketPortWidget, self).__init__(parent)

        self.socket: QTcpSocket | None = None

        LINE_HEIGHT = 30
        layout = QHBoxLayout()
        self.setLayout(layout)

        # IP Address Input
        ipLabel = QLabel("IP:")
        self.ipBox = QComboBox()
        self.ipBox.setEditable(True)
        self.ipBox.setCurrentText("127.0.0.1")
        self.ipBox.setFixedHeight(LINE_HEIGHT)
        self.ipBox.setMinimumWidth(200)
        layout.addWidget(ipLabel)
        layout.addWidget(self.ipBox, stretch=1)

        # Port Input
        portLabel = QLabel("Port:")
        self.portEdit = QLineEdit()
        self.portEdit.setText("8000")
        self.portEdit.setFixedHeight(LINE_HEIGHT)
        self.portEdit.setMinimumWidth(100)
        layout.addWidget(portLabel)
        layout.addWidget(self.portEdit)
        # Connect Button
        self.connectButton = QPushButton("连接")
        self.connectButton.setFixedWidth(100)
        self.connectButton.setFixedHeight(LINE_HEIGHT)
        self.connectButton.clicked.connect(self.connectButtonClicked)
        layout.addWidget(self.connectButton)

    def connectButtonClicked(self):
        # Implement connection logic here
        if self.socket and self.socket.state() == QTcpSocket.SocketState.ConnectedState:
            self.socket.disconnectFromHost()
            self.ipBox.setEnabled(True)
            self.portEdit.setEnabled(True)
            self.connectButton.setText("连接")
            self.socket = None
            self.port_close.emit()
            return
        elif not self.socket:
            self.socket = QTcpSocket(self)
            hostAddress = QHostAddress(self.ipAddress())
            if hostAddress.isNull():
                QMessageBox.warning(self, "输入错误", "无效的IP地址！")
                self.socket = None
                return
            else:
                try:
                    self.socket.connectToHost(hostAddress, self.portNumber())
                    if not self.socket.waitForConnected(3000):
                        QMessageBox.warning(self, "连接失败", f"无法连接到 {self.ipAddress()}:{self.portNumber()}")
                        self.socket = None
                        return
                    self.ipBox.setEnabled(False)
                    self.portEdit.setEnabled(False)
                    self.connectButton.setText("断开")
                    self.port_open.emit(self.socket)
                    self.socket.disconnected.connect(self.socketDisconnected)
                except Exception as e:
                    QMessageBox.warning(self, "连接异常", str(e))
                    self.socket = None
                    return
    
    def socketDisconnected(self):
        self.socket = None
        self.ipBox.setEnabled(True)
        self.portEdit.setEnabled(True)
        self.connectButton.setText("连接")
        self.port_close.emit()


    def ipAddress(self):
        return self.ipBox.currentText()

    def portNumber(self):
        port = 0
        try:
            port = int(self.portEdit.text())
        except ValueError:
            QMessageBox.warning(self, "输入错误", "端口号必须是整数！")
        return port

    def setIpAddress(self, ip):
        self.ipBox.setCurrentText(ip)

    def setPortNumber(self, port):
        self.portEdit.setText(str(port))

