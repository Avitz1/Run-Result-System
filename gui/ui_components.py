from PyQt5.QtWidgets import QComboBox, QFormLayout, QLineEdit, QLabel, QTableWidget, QHeaderView, QTableWidgetItem

from gui.constants import TABLE_VIEW_TIP, ID_COLUMN_NAME, SELECT_TOOL_TEXT


class ToolComboBox(QComboBox):
    def __init__(self, db, parent=None):
        super().__init__(parent)
        self.db = db
        self.addItem(SELECT_TOOL_TEXT)
        self.load_tools()

    def load_tools(self):
        tools = self.db.fetch_tools()
        for tool in tools:
            self.addItem(tool)


class FilterForm(QFormLayout):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.filters = {}

    def load_schema(self, schema):
        self.clear_filters()
        for field, value in schema.items():
            if isinstance(value, str):
                line_edit = QLineEdit()
                self.filters[field] = line_edit
                self.addRow(QLabel(field), line_edit)

    def clear_filters(self):
        while self.count():
            child = self.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        self.filters = {}


class ResultsTable(QTableWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.setSortingEnabled(True)
        self.setToolTip(TABLE_VIEW_TIP)

    def clear_table(self):
        self.setRowCount(0)
        self.setColumnCount(0)

    def load_data(self, results):
        self.clear_table()
        if not results:
            return

        sample_result = results[0].result
        columns = list(sample_result.keys())
        self.setColumnCount(len(columns) + 1)
        self.setHorizontalHeaderLabels([ID_COLUMN_NAME] + columns)

        self.setRowCount(len(results))
        for row_idx, result in enumerate(results):
            self.setItem(row_idx, 0, QTableWidgetItem(str(result.id)))
            for col_idx, key in enumerate(columns, start=1):
                self.setItem(row_idx, col_idx, QTableWidgetItem(str(result.result[key])))
