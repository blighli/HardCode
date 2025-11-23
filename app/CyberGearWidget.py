from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from app.MessageEditWidget import MessageEditWidget

class CyberGearWidget(QWidget):
    def __init__(self, parent=None, messenger : MessageEditWidget = None):
        super(CyberGearWidget, self).__init__(parent)
        self.messenger : MessageEditWidget = messenger
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        layout.addSpacing(100)

        buttonLayout = QHBoxLayout()

        startButton = QPushButton("开始控制")
        startButton.setFixedWidth(100)
        startButton.clicked.connect(self.startControl)
        buttonLayout.addWidget(startButton)

        cwButton = QPushButton("正向运行")
        cwButton.setFixedWidth(100)
        buttonLayout.addWidget(cwButton)
        cwButton.pressed.connect(self.runForward)
        cwButton.released.connect(self.stopRun)

        ccwButton = QPushButton("反向运行")
        ccwButton.setFixedWidth(100)
        buttonLayout.addWidget(ccwButton)
        ccwButton.pressed.connect(self.runBackward)
        ccwButton.released.connect(self.stopRun)

        layout.addLayout(buttonLayout)
        layout.addStretch()
        
        self.setLayout(layout)

    def startControl(self):
        print("开始控制小米电机")
        if self.messenger:
            self.messenger.sendMessage("41 54 2b 41 54 0d 0a")

    def runForward(self):
        print("小米电机正向运行")
        if self.messenger:
            self.messenger.sendMessage("41 54 90 07 eb fc 08 05 70 00 00 07 01 95 54 0d 0a")
    
    def runBackward(self):
        print("小米电机反向运行")
        if self.messenger:
            self.messenger.sendMessage("41 54 90 07 eb fc 08 05 70 00 00 07 01 6a aa 0d 0a")
    
    def stopRun(self):
        print("小米电机停止运行")
        if self.messenger:
            self.messenger.sendMessage("41 54 90 07 eb fc 08 05 70 00 00 07 00 7f ff 0d 0a")