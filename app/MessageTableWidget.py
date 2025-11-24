from PyQt6.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, QPushButton, QHBoxLayout, QVBoxLayout, QFileDialog, QComboBox, QHeaderView
import json

HEADERS = ["Length", "Type", "Name", "Value", "Format"]
TYPES = ["Byte","Bit"]
FORMATS = ["Dec","Char","Hex", "Bin" ]

def createComboBox(items, currentText=""):
    comboBox = QComboBox()
    comboBox.addItems(items)
    index = comboBox.findText(currentText)
    if index >= 0:
        comboBox.setCurrentIndex(index)
    return comboBox

class MessageTableWidget(QWidget):
    def __init__(self, parent=None):
        super(MessageTableWidget, self).__init__(parent)

        LINE_HEIGHT = 30
        
        layout = QVBoxLayout(self)

        self.table = QTableWidget()
        layout.addWidget(self.table)
        self.table.setColumnCount(len(HEADERS))
        self.table.setHorizontalHeaderLabels(HEADERS)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        self.table.setRowCount(0)

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

        self.encodeButton = QPushButton("encode")
        self.encodeButton.setFixedWidth(100)
        self.encodeButton.setFixedHeight(LINE_HEIGHT)
        self.encodeButton.clicked.connect(self.encode)

        self.decodeButton = QPushButton("decode")
        self.decodeButton.setFixedWidth(100)
        self.decodeButton.setFixedHeight(LINE_HEIGHT)
        self.decodeButton.clicked.connect(self.decode)
        
        buttonBox = QHBoxLayout()
        buttonBox.addStretch()
        buttonBox.addWidget(self.addButton)
        buttonBox.addWidget(self.delButton)
        buttonBox.addWidget(self.loadButton)
        buttonBox.addWidget(self.saveButton)
        buttonBox.addWidget(self.encodeButton)
        buttonBox.addWidget(self.decodeButton)
        buttonBox.addStretch()
        layout.addLayout(buttonBox)

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

    def loadTable(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open Table File", "", "JSON Files (*.json);;All Files (*)")
        if not filename:
            return
        
        with open(filename, 'r') as f:
            data = json.load(f)
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

    def saveTable(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Save Table File", "", "JSON Files (*.json);;All Files (*)")
        if not filename:
            return
        
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
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)

    
    def encode(self):
        data = []
        for row in range(self.table.rowCount()):
            fieldLength = 0
            fieldType = "Byte"
            fieldFormat = "Dec"
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
                if fieldFormat == "Dec":
                    try:
                        intValue = int(fieldValue)
                        bitLength = intValue.bit_length()
                        byteLength = (bitLength + 7) // 8
                        if byteLength > fieldLength:
                            error = f"Error: {fieldName}={fieldValue} exceeds the specified length of {fieldLength} bytes"
                            print(error)
                            return error
                        hexValue = intValue.to_bytes(fieldLength, byteorder='big').hex()
                        data.append(hexValue)
                    except ValueError:
                        error = f"Error: {fieldName}={fieldValue} is not a valid decimal number"
                        print(error)
                        return error

                elif fieldFormat == "Hex":
                    try:
                        if fieldValue.startswith("0x") or fieldValue.startswith("0X"):
                            fieldValue = fieldValue[2:]
                        hexValue = fieldValue.replace(" ", "")
                        # 判断fieldValue是否是合法的十六进制字符串
                        bytes.fromhex(hexValue)
                        if len(hexValue) != fieldLength * 2:
                            error = f"Error: {fieldName}={fieldValue} not the specified length of {fieldLength} bytes"
                            print(error)
                            return error
                        data.append(hexValue)
                    except ValueError:
                        error = f"Error: {fieldName}={fieldValue} is not a valid hexadecimal string"
                        print(error)
                        return error

                elif fieldFormat == "Char":
                    byteValue = fieldValue.encode('utf-8')
                    if len(byteValue) > fieldLength:
                        error = f"Error: {fieldName}={fieldValue} exceeds the specified length of {fieldLength} bytes"
                        print(error)
                        return error
                    # 如果不足长度，进行补0处理
                    byteValue = byteValue.ljust(fieldLength, b'\x00')
                    hexValue = byteValue.hex()
                    data.append(hexValue)
                elif fieldFormat == "Bin":
                    try:
                        intValue = int(fieldValue, 2)
                        bitLength = intValue.bit_length()
                        byteLength = (bitLength + 7) // 8
                        if byteLength != fieldLength:
                            error = f"Error: {fieldName}={fieldValue} not the specified length of {fieldLength} bytes"
                            print(error)
                            return error
                        hexValue = intValue.to_bytes(fieldLength, byteorder='big').hex()
                        data.append(hexValue)                     
                    except ValueError:
                        error = f"Error: {fieldName}={fieldValue} is not a valid binary string"
                        print(error)
                        return error

            elif fieldType == "Bit":
                # 位类型处理，可以根据需要进行扩展
                pass
        # 将十六进制字符串列表合并成一个完整的十六进制字符串，并且每隔两位添加一个空格
        hexString = "".join(data).upper()
        hexString = " ".join(hexString[i:i+2] for i in range(0, len(hexString), 2))
        print("Encoded Data: ", hexString)
        return hexString

   

    def decode(self, data):
        pass