import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QComboBox, QTableWidget, QTableWidgetItem, QHeaderView
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
        self.tool_combo.currentIndexChanged.connect(self.load_data)
        layout.addWidget(self.tool_combo)

        self.table = QTableWidget()
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.table)

        self.load_tools()

    def load_tools(self):
        tools = self.db.fetch_tools()
        for tool in tools:
            self.tool_combo.addItem(tool)

    def load_data(self):
        tool_name = self.tool_combo.currentText()
        if tool_name == "Select a tool":
            self.table.setRowCount(0)
            self.table.setColumnCount(0)
            return

        results = self.db.fetch_results(tool_name)
        if not results:
            self.table.setRowCount(0)
            self.table.setColumnCount(0)
            return

        sample_result = results[0].result
        columns = list(sample_result.keys())
        self.table.setColumnCount(len(columns))
        self.table.setHorizontalHeaderLabels(columns)

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