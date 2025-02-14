from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from ui_components import ToolSelector, TableView, SearchButton, FilterSelector, PaginationControls
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
        self.setGeometry(100, 100, 800, 600)

        # Initialize UI components
        self.tool_selector = ToolSelector(self)
        self.filter_selector = FilterSelector(self)
        self.search_button = SearchButton(self)
        self.table_view = TableView(self)
        self.pagination_controls = PaginationControls(self)

        layout = QVBoxLayout()
        layout.addWidget(self.tool_selector.label)
        layout.addWidget(self.tool_selector.combo_box)
        layout.addWidget(self.filter_selector.label)
        layout.addLayout(self.filter_selector.layout)
        layout.addWidget(self.search_button.button)
        layout.addWidget(self.table_view.table)
        layout.addLayout(self.pagination_controls.layout)
        self.setLayout(layout)

    def update_table(self, data, columns):
        self.table_view.update_table(data, columns)

    def update_filters(self, fields):
        self.filter_selector.update_filters(fields)

    def update_pagination(self, total_pages):
        self.pagination_controls.update_total_pages(total_pages)

    def set_pagination_buttons_enabled(self, next_enabled, prev_enabled):
        self.pagination_controls.set_buttons_enabled(next_enabled, prev_enabled)

    def sort_table(self, column_index):
        self.table_view.sort_table(column_index)