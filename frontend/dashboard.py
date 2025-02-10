from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QComboBox, QPushButton
from table_view import TableView
from data_handler import DataHandler
from styles import Styles

class Dashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        Styles.apply_styles(self, "dashboard")

    def init_ui(self):
        self.setWindowTitle("Dashboard")
        self.setGeometry(100, 100, 800, 500)

        self.label = QLabel("Select a Tool:")
        self.tool_select = QComboBox()
        self.tool_select.addItems(["Tool A", "Tool B", "Tool C"])

        self.fetch_button = QPushButton("Fetch Data")
        self.fetch_button.clicked.connect(self.fetch_data)

        self.table_view = TableView()

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.tool_select)
        layout.addWidget(self.fetch_button)
        layout.addWidget(self.table_view)
        self.setLayout(layout)

    def fetch_data(self):
        selected_tool = self.tool_select.currentText()
        data = DataHandler.get_data(selected_tool)
        self.table_view.update_table(data)


