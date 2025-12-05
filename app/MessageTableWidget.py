from PyQt6.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, QHeaderView, QComboBox, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFileDialog
from PyQt6.QtCore import Qt, pyqtSignal
import json

HEADERS = ["Length", "Type", "Name", "Value", "Format"]
TYPES = ["Byte","Bit"]
FORMATS = ["Int", "Float", "String","Hex", "Binary" ]
LINE_HEIGHT = 30

def createComboBox(items, currentText=""):
    comboBox = QComboBox()
    comboBox.addItems(items)
    index = comboBox.findText(currentText)
    if index >= 0:
        comboBox.setCurrentIndex(index)
    return comboBox

class MessageTableWidget(QWidget):

    send_message = pyqtSignal(str)

    def __init__(self, parent=None):
            super(MessageTableWidget, self).__init__(parent)

            layout = QVBoxLayout(self)
            self.table = QTableWidget()
            layout.addWidget(self.table)

            self.table.setColumnCount(len(HEADERS))
            self.table.setHorizontalHeaderLabels(HEADERS)
            self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
            self.table.setRowCount(0)

            self.statusLabel = QLabel("")
            layout.addWidget(self.statusLabel)

            self.encodeButton = QPushButton("encode")
            self.encodeButton.setMinimumWidth(100)
            self.encodeButton.setFixedHeight(LINE_HEIGHT)
            self.encodeButton.clicked.connect(self.encode)

            buttonBox = QHBoxLayout()
            buttonBox.addStretch()
            buttonBox.addWidget(self.encodeButton)
            buttonBox.addStretch()
            layout.addLayout(buttonBox)

            self.table.addAction("Add").triggered.connect(self.addRow)
            self.table.addAction("Del").triggered.connect(self.deleteRow)
            self.table.addAction("Load").triggered.connect(self.loadTable)
            self.table.addAction("Save").triggered.connect(self.saveTable)
            self.table.setContextMenuPolicy(Qt.ContextMenuPolicy.ActionsContextMenu)

    def setStatus(self, message):
        self.statusLabel.setText(message)

    def addRow(self):
        row = self.table.rowCount()
        self.table.insertRow(row)
        for col in range(self.table.columnCount()):
            if self.table.horizontalHeaderItem(col).text() == "Type":
                self.table.setCellWidget(row, col, createComboBox(TYPES))
            elif self.table.horizontalHeaderItem(col).text() == "Format":
                self.table.setCellWidget(row, col, createComboBox(FORMATS))
            else:
                self.table.setItem(row, col, QTableWidgetItem(""))

    def deleteRow(self):
        selectedRows = set()
        for item in self.table.selectedItems():
            selectedRows.add(item.row())
        for row in sorted(selectedRows, reverse=True):
            self.table.removeRow(row)

    def loadTableFromJson(self, data):
        self.table.setRowCount(0)
        for row in data:
            self.addRow()
            for col, value in enumerate(row):
                if self.table.horizontalHeaderItem(col).text() == "Type":
                    comboBox: QComboBox = self.table.cellWidget(self.table.rowCount()-1, col)
                    index = comboBox.findText(value)
                    if index >= 0:
                        comboBox.setCurrentIndex(index)
                elif self.table.horizontalHeaderItem(col).text() == "Format":
                    comboBox: QComboBox = self.table.cellWidget(self.table.rowCount()-1, col)
                    index = comboBox.findText(value)
                    if index >= 0:
                        comboBox.setCurrentIndex(index)
                else:
                    self.table.setItem(self.table.rowCount()-1, col, QTableWidgetItem(str(value)))

    
    def loadTableFromFile(self, filename):
        with open(filename, 'r') as f:
            data = json.load(f)
            self.loadTableFromJson(data)

    def loadTable(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open Table File", "", "JSON Files (*.json);;All Files (*)")
        if not filename:
            return
        self.loadTableFromFile(filename)
        
    def saveTableToJson(self):
        data = []
        for row in range(self.table.rowCount()):
            rowData = []
            for col in range(self.table.columnCount()):
                if self.table.horizontalHeaderItem(col).text() == "Type":
                    comboBox: QComboBox =  self.table.cellWidget(row, col)
                    itemText = comboBox.currentText()
                elif self.table.horizontalHeaderItem(col).text() == "Format":
                    comboBox: QComboBox = self.table.cellWidget(row, col)
                    itemText = comboBox.currentText()
                else:
                    itemText = self.table.item(row, col).text()
                rowData.append(itemText if itemText else "")
            data.append(rowData)
        return data

    def saveTableToFile(self, filename):
        data = self.saveTableToJson()
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)

    def saveTable(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Save Table File", "", "JSON Files (*.json);;All Files (*)")
        if not filename:
            return
        self.saveTableToFile(filename)


    def setButtonText(self, buttonText):
        self.encodeButton.setText(buttonText)

    def setButtonEnabled(self, enabled: bool):
        self.encodeButton.setEnabled(enabled)

    def setButtonVisible(self, visible: bool):
        self.encodeButton.setVisible(visible)
        

    def encode(self):
        data = []
        bitString = ""
        for row in range(self.table.rowCount()):
            fieldLength = 0
            fieldType = "Byte"
            fieldFormat = "Int"
            fieldName = ""
            fieldValue = ""
            for col in range(self.table.columnCount()):
                if self.table.horizontalHeaderItem(col).text() == "Length":
                    fieldLength = self.table.item(row, col).text()
                    fieldLength = int(fieldLength) if fieldLength.isdigit() else 0
                elif self.table.horizontalHeaderItem(col).text() == "Type":
                    fieldType =  self.table.cellWidget(row, col).currentText()
                elif self.table.horizontalHeaderItem(col).text() == "Format":
                    fieldFormat =  self.table.cellWidget(row, col).currentText()
                elif self.table.horizontalHeaderItem(col).text() == "Name":
                    fieldName = self.table.item(row, col).text()
                elif self.table.horizontalHeaderItem(col).text() == "Value":
                    fieldValue = self.table.item(row, col).text()
            # 处理这个字段的值，根据其表示格式把字段值从显示字符串转换成十六进制字符串，并且添加到data中，注意根据长度和类型进行处理
            if fieldType == "Byte":
                if fieldFormat == "Int":
                    try:
                        intValue = int(fieldValue)
                        bitLength = intValue.bit_length()
                        byteLength = (bitLength + 7) // 8
                        if byteLength > fieldLength:
                            error = f"Error: {fieldName}={fieldValue} exceeds the specified length of {fieldLength} bytes"
                            self.setStatus(error)
                            return None
                        hexValue = intValue.to_bytes(fieldLength, byteorder='big').hex()
                        data.append(hexValue)
                    except ValueError:
                        error = f"Error: {fieldName}={fieldValue} is not a valid integer"
                        self.setStatus(error)
                        return None
                    
                if fieldFormat == "Float":
                    try:
                        import struct
                        floatValue = float(fieldValue)
                        if fieldLength == 4:
                            hexValue = struct.pack('>f', floatValue).hex()
                        elif fieldLength == 8:
                            hexValue = struct.pack('>d', floatValue).hex()
                        else:
                            error = f"Error: {fieldName}={fieldValue} has unsupported length {fieldLength} for Float"
                            self.setStatus(error)
                            return None
                        data.append(hexValue)
                    except ValueError:
                        error = f"Error: {fieldName}={fieldValue} is not a valid float"
                        self.setStatus(error)
                        return None
                    except struct.error:
                        error = f"Error: {fieldName}={fieldValue} struct packing error"
                        self.setStatus(error)
                        return None

                elif fieldFormat == "Hex":
                    try:
                        if fieldValue.startswith("0x") or fieldValue.startswith("0X"):
                            fieldValue = fieldValue[2:]
                        hexValue = fieldValue.replace(" ", "")
                        # 判断fieldValue是否是合法的十六进制字符串
                        bytes.fromhex(hexValue)
                        if len(hexValue) != fieldLength * 2:
                            error = f"Error: {fieldName}={fieldValue} not the specified length of {fieldLength} bytes"
                            self.setStatus(error)
                            return None
                        data.append(hexValue)
                    except ValueError:
                        error = f"Error: {fieldName}={fieldValue} is not a valid hexadecimal string"
                        self.setStatus(error)
                        return None

                elif fieldFormat == "String":
                    byteValue = fieldValue.encode('utf-8')
                    if len(byteValue) > fieldLength:
                        error = f"Error: {fieldName}={fieldValue} exceeds the specified length of {fieldLength} bytes"
                        self.setStatus(error)
                        return None
                    # 如果不足长度，进行补0处理
                    byteValue = byteValue.ljust(fieldLength, b'\x00')
                    hexValue = byteValue.hex()
                    data.append(hexValue)
                elif fieldFormat == "Binary":
                    try:
                        intValue = int(fieldValue, 2)
                        bitLength = intValue.bit_length()
                        byteLength = (bitLength + 7) // 8
                        if byteLength != fieldLength:
                            error = f"Error: {fieldName}={fieldValue} not the specified length of {fieldLength} bytes"
                            self.setStatus(error)
                            return None
                        hexValue = intValue.to_bytes(fieldLength, byteorder='big').hex()
                        data.append(hexValue)                     
                    except ValueError:
                        error = f"Error: {fieldName}={fieldValue} is not a valid binary string"
                        self.setStatus(error)
                        return None

            elif fieldType == "Bit":
                if fieldFormat == "Int":
                    try:
                        intValue = int(fieldValue)
                        bitLength = intValue.bit_length()
                        if bitLength > fieldLength:
                            error = f"Error: {fieldName}={fieldValue} exceeds the specified length of {fieldLength} bits"
                            self.setStatus(error)
                            return None
                        bitString += f"{intValue:0{fieldLength}b}"
                        if len(bitString) >= 8:
                            byteCount = len(bitString) // 8
                            for i in range(byteCount):
                                byteBits = bitString[i*8:(i+1)*8]
                                byteValue = int(byteBits, 2)
                                hexValue = f"{byteValue:02x}"
                                data.append(hexValue)
                            bitString = bitString[byteCount*8:]
                    except ValueError:
                        error = f"Error: {fieldName}={fieldValue} is not a valid integer"
                        self.setStatus(error)
                        return None
                elif fieldFormat == "Binary":
                    try:
                        intValue = int(fieldValue, 2)
                        bitLength = intValue.bit_length()
                        if bitLength != fieldLength:
                            error = f"Error: {fieldName}={fieldValue} not the specified length of {fieldLength} bits"
                            self.setStatus(error)
                            return None
                        bitString += f"{intValue:0{fieldLength}b}"
                        if len(bitString) >= 8:
                            byteCount = len(bitString) // 8
                            for i in range(byteCount):
                                byteBits = bitString[i*8:(i+1)*8]
                                byteValue = int(byteBits, 2)
                                hexValue = f"{byteValue:02x}"
                                data.append(hexValue)
                            bitString = bitString[byteCount*8:]                                         
                    except ValueError:
                        error = f"Error: {fieldName}={fieldValue} is not a valid binary string"
                        self.setStatus(error)
                        return None
                else:
                    error = f"Error: Unsupported format {fieldFormat} for Bit type"
                    self.setStatus(error)
                    return None
        # 处理剩余的bitString
        if len(bitString) > 0:
            error = f"Error: Remaining bits {bitString} do not form a complete byte"
            self.setStatus(error)
            return None
        # 将十六进制字符串列表合并成一个完整的十六进制字符串，并且每隔两位添加一个空格
        hexString = "".join(data).upper()
        self.setStatus(f"Encoded Data {len(hexString) // 2} bytes: {hexString}")
        hexString = " ".join(hexString[i:i+2] for i in range(0, len(hexString), 2))

        if self.send_message:
            self.send_message.emit(hexString)
        return hexString