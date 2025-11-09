from PyQt6.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, QPushButton, QHBoxLayout, QVBoxLayout, QFileDialog
import json

class MessageTableWidget(QWidget):
    def __init__(self, parent=None):
        super(MessageTableWidget, self).__init__(parent)

        LINE_HEIGHT = 30
        tableHeaders = ["pos", "len", "type", "name", "value"]

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