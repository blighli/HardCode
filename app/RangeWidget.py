from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QLineEdit, QSlider, QSpinBox
from PyQt6.QtCore import Qt, pyqtSignal

class RangeWidget(QWidget):

    value_changed = pyqtSignal(str, int)

    def __init__(self, minValue=0, maxValue=100, value=0, parent=None):
        super(RangeWidget, self).__init__(parent)
        self.minValue = minValue
        self.maxValue = maxValue
        self.value = value
        self.initUI()

    def initUI(self):
        LINE_HEIGHT = 30

        layout = QHBoxLayout()

        self.nameEdit = QLineEdit()
        self.nameEdit.setPlaceholderText("参数名称")
        self.nameEdit.setFixedWidth(100)
        self.nameEdit.setFixedHeight(LINE_HEIGHT)
        layout.addWidget(self.nameEdit)

        layout.addWidget(QLabel("="))

        self.spin = QSpinBox()
        self.spin.setFixedWidth(80)
        self.spin.setFixedHeight(LINE_HEIGHT)
        self.spin.setRange(self.minValue, self.maxValue)
        self.spin.setValue(self.value)
        self.spin.setSingleStep(1)
        self.spin.valueChanged.connect(self.spinUpdate)
        layout.addWidget(self.spin)

        layout.addWidget(QLabel("("))
        self.minEdit = QLineEdit(str(self.minValue))
        self.minEdit.setFixedWidth(50)
        self.minEdit.setFixedHeight(LINE_HEIGHT)
        self.minEdit.textChanged.connect(self.rangeUpdate)
        layout.addWidget(self.minEdit)
        layout.addWidget(QLabel("-"))
        self.maxEdit = QLineEdit(str(self.maxValue))
        self.maxEdit.setFixedWidth(50)
        self.maxEdit.setFixedHeight(LINE_HEIGHT)
        self.maxEdit.textChanged.connect(self.rangeUpdate)
        layout.addWidget(self.maxEdit)
        layout.addWidget(QLabel(")"))


        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setFixedHeight(LINE_HEIGHT)
        self.slider.setRange(self.minValue, self.maxValue)
        self.slider.setTickInterval(int((self.maxValue - self.minValue)/10))
        self.slider.setValue(self.value)
        self.slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.slider.setSingleStep(1)
        self.slider.valueChanged.connect(self.sliderUpdate)
        layout.addWidget(self.slider)

        self.setLayout(layout)

    def name(self):
        return self.nameEdit.text()

    def updateValue(self):
        self.value = self.slider.value()
        self.value_changed.emit(self.nameEdit.text(), self.value)

    def sliderUpdate(self):
        self.spin.setValue(self.slider.value())
        self.updateValue()

    def spinUpdate(self):
        self.slider.setValue(self.spin.value())
        self.updateValue()

    def rangeUpdate(self):
        try:
            self.minValue = int(self.minEdit.text())
            self.maxValue = int(self.maxEdit.text())
            self.spin.setRange(self.minValue, self.maxValue)
            self.slider.setRange(self.minValue, self.maxValue)
            self.slider.setTickInterval(int((self.maxValue - self.minValue)/10))
            self.updateValue()
        except:
            self.minEdit.setText(str(self.minValue))
            self.maxEdit.setText(str(self.maxValue))