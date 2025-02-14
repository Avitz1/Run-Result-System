from PyQt6.QtWidgets import QLabel, QComboBox, QTableWidget, QTableWidgetItem
from data_handler import DataHandler

class ToolSelector:
    def __init__(self, parent):
        self.label = QLabel("Choose a Tool:")
        self.combo_box = QComboBox()
        self.combo_box.addItem("Select a Tool")
        self.combo_box.addItems(DataHandler.get_tools())
        self.combo_box.setCurrentIndex(0)
        self.combo_box.currentIndexChanged.connect(parent.event_handlers.tool_selected)

class TableView:
    def __init__(self):
        self.table = QTableWidget()

    def update_table(self, data, columns):
        self.table.setRowCount(len(data))
        self.table.setColumnCount(len(columns))
        self.table.setHorizontalHeaderLabels(columns)

        for row_idx, row_data in enumerate(data):
            for col_idx, item in enumerate(row_data):
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(item)))