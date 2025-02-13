from PyQt6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QComboBox, QPushButton, QLineEdit,
    QHBoxLayout, QDateEdit, QMessageBox
)
from PyQt6.QtCore import QDate
from table_view import TableView
from data_handler import DataHandler
from styles import Styles

class Dashboard(QWidget):
    def __init__(self, login_page):
        super().__init__()
        self.login_page = login_page
        self.selected_column = None  # Track selected column
        self.init_ui()
        Styles.apply_styles(self, "dashboard")

    def configure_date_picker(self, date_picker):
        """Helper method to configure date pickers"""
        date_picker.setCalendarPopup(True)
        date_picker.setDate(QDate())  # Set the date as invalid (empty state)
        date_picker.setFixedHeight(40)
        date_picker.setMinimumWidth(200)

    def init_ui(self):
        self.setWindowTitle("Dashboard")
        self.setGeometry(100, 100, 800, 500)

        # Choose Tool
        self.label_tool = QLabel("Choose a Tool:")
        self.tool_select = QComboBox()
        self.tool_select.addItems(self.get_tools())  # Fetch tools dynamically

        # Choose Column
        self.column_select = QComboBox()
        self.column_select.addItem("Select a Column")  # Default placeholder
        self.column_select.addItems(self.get_columns())  # Add actual column names
        self.column_select.setCurrentIndex(0)  # Ensure the first item is selected initially
        self.column_select.currentIndexChanged.connect(self.column_selected)

        # Selected Column Display
        self.selected_column_label = QLabel("")
        self.clear_button = QPushButton("✖")
        self.clear_button.setFixedSize(25, 25)  # Adjust size for better visibility
        Styles.apply_styles(self.clear_button, "clear_button")
        self.clear_button.setVisible(False)
        self.clear_button.clicked.connect(self.clear_selected_column)

        column_layout = QHBoxLayout()
        column_layout.addWidget(self.selected_column_label)
        column_layout.addWidget(self.clear_button)
        column_layout.setSpacing(5)
        column_layout.setContentsMargins(0, 0, 0, 0)

        # Filter Input
        self.filter_input = QLineEdit()
        self.filter_input.setPlaceholderText("Enter value to filter...")
        self.filter_input.setEnabled(False)  # Disabled initially
        self.filter_input.setVisible(False)  # Hidden initially
        self.filter_input.setFixedHeight(35)  # Adjust height for better visibility
        Styles.apply_styles(self.filter_input, "filter_input")

        date_layout = QHBoxLayout()

        # Start Date Picker
        self.start_date_label = QLabel("Start Date:")
        self.start_date_picker = QDateEdit()
        self.configure_date_picker(self.start_date_picker)
        Styles.apply_styles(self.start_date_picker, "date_picker")

        # End Date Picker
        self.end_date_label = QLabel("End Date:")
        self.end_date_picker = QDateEdit()
        self.configure_date_picker(self.end_date_picker)
        Styles.apply_styles(self.end_date_picker, "date_picker")

        # Add widgets to horizontal layout
        date_layout.addWidget(self.start_date_label)
        date_layout.addWidget(self.start_date_picker)
        date_layout.addSpacing(10)
        date_layout.addWidget(self.end_date_label)
        date_layout.addWidget(self.end_date_picker)

        # Distribute space evenly between date pickers
        date_layout.setStretch(1, 1)
        date_layout.setStretch(3, 1)

        # Search Button
        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.search_data)

        # Small Logout Button
        self.logout_button = QPushButton("⏻")
        self.logout_button.setFixedSize(50, 30)
        self.logout_button.clicked.connect(self.go_to_login)

        # Table View
        self.table_view = TableView()

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.label_tool)
        layout.addWidget(self.tool_select)
        layout.addWidget(self.column_select)
        layout.addLayout(column_layout)
        layout.addWidget(self.filter_input)
        layout.addLayout(date_layout)
        layout.addWidget(self.search_button)
        layout.addWidget(self.logout_button)
        layout.addWidget(self.table_view)

        self.setLayout(layout)

    def get_tools(self):
        """Fetch tool names from backend"""
        return DataHandler.get_tools()

    def get_columns(self):
        """Fetch column names from backend"""
        return DataHandler.get_columns()

    def column_selected(self):
        """Handle column selection"""
        self.selected_column = self.column_select.currentText()

        if self.selected_column == "Select a Column":
            self.selected_column_label.setText("")
            self.clear_button.setVisible(False)  # Hide the button if no column is selected
        else:
            self.selected_column_label.setText(f"Selected: {self.selected_column}")
            self.clear_button.setVisible(True)  # Show the button when a column is selected

        # Enable filter input only if a valid column is selected
        self.filter_input.setEnabled(self.selected_column != "Select a Column")
        self.filter_input.setVisible(self.selected_column != "Select a Column")  # Show filter only if column is selected

    def clear_selected_column(self):
        """Clear selected column"""
        self.selected_column = None
        self.selected_column_label.setText("")
        self.filter_input.clear()
        self.filter_input.setVisible(False)  # Hide filter input when column is cleared
        self.filter_input.setEnabled(False)
        self.column_select.setCurrentIndex(0)  # Reset to "Select a Column"
        self.clear_button.setVisible(False)  # Hide the clear button after clearing the column

    def search_data(self):
        """Fetch filtered data"""
        selected_tool = self.tool_select.currentText()
        filter_value = self.filter_input.text()

        # Get the selected start and end date
        start_date = self.start_date_picker.date()
        end_date = self.end_date_picker.date()

        # Check if no date is selected, and set default value for dates
        start_date_str = start_date.toString("yyyy-MM-dd") if start_date != QDate() else ""
        end_date_str = end_date.toString("yyyy-MM-dd") if end_date != QDate() else ""

        # If no column is selected, allow fetching all data (no filter applied)
        if not self.selected_column:
            self.selected_column = None  # Set it to None or a suitable default value

        try:
            # Fetch filtered data or all data if no column or filter value is provided
            data = DataHandler.get_filtered_data(selected_tool, self.selected_column, filter_value, start_date_str,
                                                 end_date_str)
            self.table_view.update_table(data)
        except ValueError as e:
            # Show error message box if dates are invalid
            QMessageBox.critical(self, "Error", f"Invalid date range: {str(e)}")

    def go_to_login(self):
        """Switch back to the login page."""
        self.login_page.show()
        self.close()