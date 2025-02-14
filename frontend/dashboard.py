from PyQt6.QtWidgets import QWidget, QVBoxLayout
from ui_components import ToolSelector, TableView
from event_handlers import EventHandlers
from styles import Styles

class Dashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.selected_tool = None
        self.event_handlers = EventHandlers(self)  # Initialize event handlers here
        self.init_ui()
        Styles.apply_styles(self, "dashboard")

    def init_ui(self):
        self.setWindowTitle("Run Results Dashboard")
        self.setGeometry(100, 100, 800, 500)

        # Initialize UI components
        self.tool_selector = ToolSelector(self)
        self.table_view = TableView()

        layout = QVBoxLayout()
        layout.addWidget(self.tool_selector.label)
        layout.addWidget(self.tool_selector.combo_box)
        layout.addWidget(self.table_view.table)
        self.setLayout(layout)

    def update_table(self, data, columns):
        self.table_view.update_table(data, columns)