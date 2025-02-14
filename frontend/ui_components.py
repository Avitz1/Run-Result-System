from PyQt6.QtWidgets import QLabel, QComboBox, QTableWidget, QTableWidgetItem, QPushButton, QLineEdit, QVBoxLayout, QHBoxLayout

class ToolSelector:
    def __init__(self, parent):
        self.label = QLabel("Choose a Tool:")
        self.combo_box = QComboBox()
        self.combo_box.addItem("Select a Tool")
        self.combo_box.addItems(parent.event_handlers.get_tools())
        self.combo_box.setCurrentIndex(0)
        self.combo_box.currentIndexChanged.connect(parent.event_handlers.tool_selected)

class FilterSelector:
    def __init__(self, parent):
        self.label = QLabel("Select Fields to Filter On:")
        self.layout = QVBoxLayout()

    def update_filters(self, fields):
        # Clear existing filters
        self.clear_layout(self.layout)

        for field, field_type in fields.items():
            if field_type == "string":
                field_label = QLabel(f"{field}:")
                field_input = QLineEdit()
                field_input.setPlaceholderText(f"Enter regex pattern for {field}...")
                filter_layout = QHBoxLayout()
                filter_layout.addWidget(field_label)
                filter_layout.addWidget(field_input)
                self.layout.addLayout(filter_layout)

    def clear_layout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
            elif child.layout():
                self.clear_layout(child.layout())

class TableView:
    def __init__(self, parent):
        self.table = QTableWidget()
        self.table.horizontalHeader().sectionClicked.connect(parent.event_handlers.sort_data)
        self.data = []
        self.columns = []

    def update_table(self, data, columns):
        self.data = data
        self.columns = columns
        self.table.setRowCount(len(data))
        self.table.setColumnCount(len(columns))
        self.table.setHorizontalHeaderLabels(columns)

        for row_idx, row_data in enumerate(data):
            for col_idx, item in enumerate(row_data):
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(item)))

    def sort_table(self, column_index):
        self.data.sort(key=lambda x: x[column_index])
        self.update_table(self.data, self.columns)

class SearchButton:
    def __init__(self, parent):
        self.button = QPushButton("Search")
        self.button.clicked.connect(parent.event_handlers.search_data)

class PaginationControls:
    def __init__(self, parent):
        self.layout = QHBoxLayout()
        self.prev_button = QPushButton("Previous")
        self.next_button = QPushButton("Next")
        self.page_input = QLineEdit()
        self.page_input.setPlaceholderText("Page")
        self.page_input.setFixedWidth(50)
        self.page_input.returnPressed.connect(parent.event_handlers.go_to_page)
        self.total_pages_label = QLabel("of 0")
        self.prev_button.clicked.connect(parent.event_handlers.prev_page)
        self.next_button.clicked.connect(parent.event_handlers.next_page)
        self.layout.addWidget(self.prev_button)
        self.layout.addWidget(self.page_input)
        self.layout.addWidget(self.total_pages_label)
        self.layout.addWidget(self.next_button)
        self.set_buttons_enabled(False, False)

    def set_buttons_enabled(self, next_enabled, prev_enabled):
        self.next_button.setEnabled(next_enabled)
        self.prev_button.setEnabled(prev_enabled)

    def update_total_pages(self, total_pages):
        self.total_pages_label.setText(f"of {total_pages}")