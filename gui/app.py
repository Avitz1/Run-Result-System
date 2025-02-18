import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QMessageBox

from database.database_client import Database, DatabaseConnectionError
from gui.constants import SELECT_TOOL_TEXT, SEARCH_BUTTON_TEXT, DASHBOARD_TITLE
from gui.ui_components import ToolComboBox, FilterForm, ResultsTable


class Dashboard(QMainWindow):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(DASHBOARD_TITLE)
        self.setGeometry(100, 100, 800, 600)

        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)

        self.tool_combo = ToolComboBox(self.db)
        self.tool_combo.currentIndexChanged.connect(self.load_schema)
        layout.addWidget(self.tool_combo)

        self.filter_form = FilterForm()
        layout.addLayout(self.filter_form)

        self.search_button = QPushButton(SEARCH_BUTTON_TEXT)
        self.search_button.clicked.connect(self.load_data)
        layout.addWidget(self.search_button)

        self.results_table = ResultsTable()
        layout.addWidget(self.results_table)

    def load_schema(self):
        tool_name = self.tool_combo.currentText()
        if tool_name == SELECT_TOOL_TEXT:
            self.filter_form.clear_filters()
            self.results_table.clear_table()
            return
        try:
            schema = self.db.fetch_schema(tool_name)
            self.filter_form.load_schema(schema)
            self.results_table.clear_table()
        except DatabaseConnectionError as err:
            self.show_error_message(str(err))

    def load_data(self):
        tool_name = self.tool_combo.currentText()
        if tool_name == SELECT_TOOL_TEXT:
            self.results_table.clear_table()
            return

        filters = {field: edit.text() for field, edit in self.filter_form.filters.items() if edit.text()}
        try:
            results = self.db.fetch_results(tool_name, filters)
            self.results_table.load_data(results)
        except DatabaseConnectionError as err:
            self.show_error_message(str(err))

    def show_error_message(self, message):
        QMessageBox.critical(self, "Database Error", message)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    try:
        db = Database()
        dashboard = Dashboard(db)
        dashboard.show()
        sys.exit(app.exec_())
    except DatabaseConnectionError as e:
        QMessageBox.critical(None, "Database Error", str(e))
        sys.exit(1)
