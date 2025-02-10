from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem, QVBoxLayout, QPushButton, QHBoxLayout, QWidget
from pagination import Pagination


class TableView(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout()
        self.table = QTableWidget()
        self.table.setColumnCount(3)  # Adjustable columns
        self.table.setHorizontalHeaderLabels(["Column 1", "Column 2", "Column 3"])
        self.table.setSortingEnabled(True)  # Enables sorting

        self.pagination = None  # Will hold the pagination instance

        # Buttons for pagination
        self.pagination_layout = QHBoxLayout()
        self.prev_button = QPushButton("Previous")
        self.prev_button.clicked.connect(self.previous_page)
        self.next_button = QPushButton("Next")
        self.next_button.clicked.connect(self.next_page)

        self.pagination_layout.addWidget(self.prev_button)
        self.pagination_layout.addWidget(self.next_button)

        self.layout.addWidget(self.table)
        self.layout.addLayout(self.pagination_layout)
        self.setLayout(self.layout)

    def update_table(self, data):
        """Updates table content dynamically without refreshing."""
        # Initialize pagination
        self.pagination = Pagination(data)
        self.display_page()

    def display_page(self):
        """Displays the current page data."""
        page_data = self.pagination.get_page_data()
        self.table.setRowCount(len(page_data))
        for row_idx, row_data in enumerate(page_data):
            for col_idx, value in enumerate(row_data):
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))

    def next_page(self):
        """Move to the next page and update table."""
        page_data = self.pagination.next_page()
        self.display_page()

    def previous_page(self):
        """Move to the previous page and update table."""
        page_data = self.pagination.previous_page()
        self.display_page()


