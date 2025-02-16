import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QComboBox, QTableWidget, QTableWidgetItem, QHeaderView, QLineEdit, QPushButton, QLabel, QFormLayout
from database.database_client import Database


class Dashboard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = Database()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Run Results Dashboard')
        self.setGeometry(100, 100, 800, 600)

        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)

        self.tool_combo = QComboBox()
        self.tool_combo.addItem("Select a tool")
        self.tool_combo.currentIndexChanged.connect(self.load_schema)
        layout.addWidget(self.tool_combo)

        self.filter_layout = QFormLayout()
        self.filters = {}
        layout.addLayout(self.filter_layout)

        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.load_data)
        layout.addWidget(self.search_button)

        self.table = QTableWidget()
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setSortingEnabled(True)
        layout.addWidget(self.table)

        self.load_tools()

    def load_tools(self):
        tools = self.db.fetch_tools()
        for tool in tools:
            self.tool_combo.addItem(tool)

    def load_schema(self):
        self.clear_table()
        self.clear_filters()
        tool_name = self.tool_combo.currentText()
        if tool_name == "Select a tool":
            return

        schema = self.db.fetch_schema(tool_name)

        for field, value in schema.items():
            if isinstance(value, str):
                line_edit = QLineEdit()
                self.filters[field] = line_edit
                self.filter_layout.addRow(QLabel(field), line_edit)

        self.centralWidget().layout().insertLayout(1, self.filter_layout)

    def clear_filters(self):
        for i in reversed(range(self.filter_layout.count())):
            widget = self.filter_layout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)
        self.filters = {}

    def clear_table(self):
        self.table.setRowCount(0)
        self.table.setColumnCount(0)

    def load_data(self):
        tool_name = self.tool_combo.currentText()
        if tool_name == "Select a tool":
            self.clear_table()
            return

        filters = {field: edit.text() for field, edit in self.filters.items() if edit.text()}
        results = self.db.fetch_results(tool_name, filters)
        if not results:
            self.clear_table()
            return

        sample_result = results[0].result
        columns = list(sample_result.keys())
        self.table.setColumnCount(len(columns) + 1)
        self.table.setHorizontalHeaderLabels(["ID"] + columns)

        self.table.setRowCount(len(results))
        for row_idx, result in enumerate(results):
            self.table.setItem(row_idx, 0, QTableWidgetItem(str(result.id)))
            for col_idx, key in enumerate(columns, start=1):
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(result.result[key])))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    dashboard = Dashboard()
    dashboard.show()
    sys.exit(app.exec_())