from PyQt6.QtWidgets import (
    QTableWidget, QTableWidgetItem, QVBoxLayout, QPushButton,
    QHBoxLayout, QWidget, QDateEdit, QLabel
)
from pagination import Pagination
from PyQt6.QtCore import QDate


class TableView(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout()
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Column 1", "Column 2", "Column 3", "Date"])
        self.table.setSortingEnabled(True)

        self.pagination = None

        # 🔹 Date Filter UI Elements
        self.date_layout = QHBoxLayout()
        self.start_date_label = QLabel("Start Date:")
        self.start_date = QDateEdit()
        self.start_date.setCalendarPopup(True)
        self.start_date.setDate(QDate.currentDate().addDays(-30))  # Default: 30 days ago

        self.end_date_label = QLabel("End Date:")
        self.end_date = QDateEdit()
        self.end_date.setCalendarPopup(True)
        self.end_date.setDate(QDate.currentDate())  # Default: Today

        self.filter_button = QPushButton("Filter Data")
        self.filter_button.clicked.connect(self.filter_data)

        self.date_layout.addWidget(self.start_date_label)
        self.date_layout.addWidget(self.start_date)
        self.date_layout.addWidget(self.end_date_label)
        self.date_layout.addWidget(self.end_date)
        self.date_layout.addWidget(self.filter_button)

        # Pagination Buttons
        self.pagination_layout = QHBoxLayout()
        self.first_button = QPushButton("1")
        self.first_button.clicked.connect(lambda: self.go_to_page(1))

        self.prev_button = QPushButton("Previous")
        self.prev_button.clicked.connect(self.previous_page)

        self.next_button = QPushButton("Next")
        self.next_button.clicked.connect(self.next_page)

        self.last_button = QPushButton("Last")
        self.last_button.clicked.connect(self.go_to_last_page)

        # Layout setup
        self.pagination_layout.addWidget(self.prev_button)
        self.pagination_layout.addWidget(self.first_button)
        self.pagination_layout.addWidget(self.next_button)
        self.pagination_layout.addWidget(self.last_button)

        self.layout.addLayout(self.date_layout)
        self.layout.addWidget(self.table)
        self.layout.addLayout(self.pagination_layout)
        self.setLayout(self.layout)

    def update_table(self, data):
        self.original_data = data
        self.pagination = Pagination(data)
        self.display_page()

    def filter_data(self):
        """Filters data based on the selected date range."""
        if not self.pagination:
            return  # No data loaded

        start_date = self.start_date.date().toString("yyyy-MM-dd")
        end_date = self.end_date.date().toString("yyyy-MM-dd")

        # Convert date string to QDate for filtering
        filtered_data = []
        for row in self.original_data:
            row_date = QDate.fromString(row[3], "yyyy-MM-dd")  # Assuming Date is in 4th column
            if row_date.isValid() and self.start_date.date() <= row_date <= self.end_date.date():
                filtered_data.append(row)

        # Update pagination with filtered data
        self.pagination = Pagination(filtered_data)
        self.display_page()

    def display_page(self):
        """Displays the current page data."""
        if not self.pagination:
            return

        page_data = self.pagination.get_page_data()
        self.table.setRowCount(len(page_data))

        for row_idx, row_data in enumerate(page_data):
            for col_idx, value in enumerate(row_data):
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))

        self.update_pagination_buttons()

    def update_pagination_buttons(self):
        for i in reversed(range(1, self.pagination_layout.count() - 2)):
            button = self.pagination_layout.itemAt(i).widget()
            if button:
                self.pagination_layout.removeWidget(button)
                button.deleteLater()

        page_buttons = self.pagination.get_pagination_buttons()
        for page_num in page_buttons:
            if page_num == "...":
                button = QPushButton("...")
                button.setEnabled(False)
            else:
                button = QPushButton(str(page_num))
                button.clicked.connect(lambda _, p=page_num: self.go_to_page(p))
                if page_num == self.pagination.current_page:
                    button.setStyleSheet("font-weight: bold; border: 2px solid black;")

            self.pagination_layout.insertWidget(self.pagination_layout.count() - 2, button)

    def go_to_page(self, page_number):
        self.pagination.go_to_page(page_number)
        self.display_page()

    def go_to_last_page(self):
        self.go_to_page(self.pagination.total_pages())

    def next_page(self):
        self.pagination.next_page()
        self.display_page()

    def previous_page(self):
        self.pagination.previous_page()
        self.display_page()

