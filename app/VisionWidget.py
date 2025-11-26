from PyQt6.QtWidgets import QWidget, QMessageBox, QLabel, QVBoxLayout,QHBoxLayout, QPushButton, QTimer
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtCore import Qt
import cv2
import numpy as np

class VisionWidget(QWidget):
    def __init__(self):
        super().__init__()
        
        LINE_HEIGHT = 30
        BUTTON_WIDTH = 100
        
        self.videoCapture: cv2.VideoCapture = None
        self.timer = 0

        self.setWindowTitle("Vision Widget")

        layout = QVBoxLayout(self)
        self.setLayout(layout)

        self.imageDiplay = QLabel()
        self.imageDiplay.setGeometry(10, 10, 640, 480)
        self.imageDiplay.setText("No image captured")
        self.imageDiplay.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.imageDiplay.setStyleSheet("background-color: black; color: white;")
        layout.addWidget(self.imageDiplay)

        buttonLayout = QHBoxLayout()
        self.captureButton = QPushButton("打开摄像头")
        self.captureButton.setFixedHeight(LINE_HEIGHT)
        self.captureButton.setFixedWidth(BUTTON_WIDTH)
        self.captureButton.clicked.connect(self.capture_image)
        buttonLayout.addStretch(1)
        buttonLayout.addWidget(self.captureButton)
        buttonLayout.addStretch(1)
        layout.addLayout(buttonLayout)


    def capture_image(self):
        self.videoCapture = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # 打开摄像头
        if not self.videoCapture.isOpened():
            QMessageBox.critical(self, "错误", "无法打开摄像头！", QMessageBox.StandardButton.Ok)
            return
        self.timer = self.startTimer(100)  # 每100毫秒捕获一次图像

    def timerEvent(self, event):
        ret, frame = self.videoCapture.read()
        if ret:
            # 处理图像数据
            rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # 将图像转换为QImage格式
            h, w, ch = rgb_image.shape
            bytes_per_line = ch * w
            qtImage = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
            self.imageDiplay.setPixmap(QPixmap.fromImage(qtImage))

        else:
            QMessageBox.warning(self, "警告", "无法读取摄像头数据！", QMessageBox.StandardButton.Ok)
            self.killTimer(self.timer)
            self.videoCapture.release()