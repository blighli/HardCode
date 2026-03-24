from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt


class AboutDialog(QDialog):
    def __init__(self, version, icon_path, parent=None):
        super().__init__(parent)
        self.setWindowTitle("About HardCode")
        self.setFixedSize(400, 300)

        layout = QVBoxLayout(self)

        # Logo
        logo_label = QLabel()
        pixmap = QPixmap(icon_path).scaled(80, 80)
        logo_label.setPixmap(pixmap)
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Title
        title_label = QLabel("HardCode")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Version
        version_label = QLabel(f"Version: {version}")
        version_label.setStyleSheet("font-size: 14px; color: gray;")
        version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Description
        desc_label = QLabel("A powerful serial port and network debugging tool")
        desc_label.setWordWrap(True)
        desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Close button
        close_btn = QPushButton("OK")
        close_btn.setFixedWidth(100)
        close_btn.clicked.connect(self.close)

        layout.addWidget(logo_label)
        layout.addWidget(title_label)
        layout.addWidget(version_label)
        layout.addWidget(desc_label)
        layout.addWidget(close_btn, alignment=Qt.AlignmentFlag.AlignCenter)