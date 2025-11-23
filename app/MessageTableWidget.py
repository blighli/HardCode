from PyQt6.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, QPushButton, QHBoxLayout, QVBoxLayout, QFileDialog
import json

class MessageTableWidget(QWidget):
    def __init__(self, parent=None):
        super(MessageTableWidget, self).__init__(parent)

        LINE_HEIGHT = 30

        # type = bit int2 int4 int8 byte char
        tableHeaders = ["len", "type", "name", "value"]

        layout = QVBoxLayout(self)

        self.table = QTableWidget()
        layout.addWidget(self.table)
        self.table.setColumnCount(len(tableHeaders))
        self.table.setHorizontalHeaderLabels(tableHeaders)
        self.table.horizontalHeader().setStretchLastSection(True)
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
        
        buttonBox = QHBoxLayout()
        buttonBox.addStretch()
        buttonBox.addWidget(self.addButton)
        buttonBox.addWidget(self.delButton)
        buttonBox.addWidget(self.loadButton)
        buttonBox.addWidget(self.saveButton)
        buttonBox.addStretch()
        layout.addLayout(buttonBox)

    def addRow(self):
        rowPosition = self.table.rowCount()
        self.table.insertRow(rowPosition)
        for col in range(self.table.columnCount()):
            self.table.setItem(rowPosition, col, QTableWidgetItem(""))

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
                self.table.setItem(self.table.rowCount()-1, col, QTableWidgetItem(str(value)))

    def saveTable(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Save Table File", "", "JSON Files (*.json);;All Files (*)")
        if not filename:
            return
        
        data = []
        for row in range(self.table.rowCount()):
            rowData = []
            for col in range(self.table.columnCount()):
                item = self.table.item(row, col)
                rowData.append(item.text() if item else "")
            data.append(rowData)
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)

    
    def encode(self):
        data = []
        for row in range(self.table.rowCount()):

            item = self.table.item(row, 0)
            itemText = item.text() if item else ""
            len = int(itemText) if itemText.isdigit() else 0

            item = self.table.item(row, 1)
            type = item.text() if item else ""
            if type == "bit":
                len = (len + 7) // 8  # Convert bits to bytes
            elif type == "int2":
                len = 2
            elif type == "int4":
                len = 4
            elif type == "int8":
                len = 8
            elif type == "byte":
                len = 1
            elif type == "char":
                pass
            
            item = self.table.item(row, 3)
            itemText = item.text() if item else ""
            value = b""
            
            data.append({
                "len": len,
                "type": type,
                "value": value
            })
        return data

    def getFieldType(self, row):
        item = self.table.item(row, 2)
        text =  item.text() if item else ""
        return text
    
    def getFieldLen(self, row):
        item = self.table.item(row, 1)
        text =  item.text() if item else ""
        len = 0
        if text.isdigit():
            len = int(text)
        return len
    
    def getFieldCharValue(self, row):
        item = self.table.item(row, 4)
        text =  item.text() if item else ""
        value = b""
        if self.getFieldType(row) == "char":
            value = text.encode('utf-8')
        return value
        
    def getFieldInt8Value(self, row):
        item = self.table.item(row, 4)
        text =  item.text() if item else ""
        value = 0
        if text.isdigit() or (text.startswith('-') and text[1:].isdigit()):
            value = int(text).to_bytes(1, byteorder='big', signed=True)
        return value
    
    def getFieldBitValue(self, row):
        item = self.table.item(row, 4)
        text =  item.text() if item else ""
        value = b""
        if all(c in '01' for c in text):
            bits = text
            while len(bits) % 8 != 0:
                bits = '0' + bits
            byteArray = bytearray()
            for i in range(0, len(bits), 8):
                byte = bits[i:i+8]
                byteArray.append(int(byte, 2))
            value = bytes(byteArray)
        return value

    def decode(self, data):
        pass