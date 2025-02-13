import random
import faker
from datetime import datetime, timedelta
from PyQt6.QtWidgets import (QMessageBox)

class DataHandler:
    @staticmethod
    def get_tools():
        """Fetch available tools."""
        return ["Tool A", "Tool B", "Tool C"]

    @staticmethod
    def get_columns():
        """Fetch column names dynamically."""
        return ["Name", "Age", "Job", "Date"]

    def get_filtered_data(tool_name, column_name, filter_value, start_date, end_date):
        """Simulates fetching filtered data with type checking"""
        fake = faker.Faker()
        dummy_data = []

        # Define expected types for each column
        expected_types = {
            "Name": str,
            "Age": int,
            "Job": str,
            "Date": str
        }

        # Check if start_date and end_date are empty (meaning no date filter applied)
        if start_date and end_date:
            # Convert string dates to datetime.date objects only if dates are provided
            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
        else:
            # If no dates are provided, don't filter by date
            start_date = None
            end_date = None

        # Validate the filter_value data type based on selected column
        if column_name in expected_types:
            expected_type = expected_types[column_name]
            try:
                # Try to cast the filter_value to the expected type
                if expected_type == int:
                    filter_value = int(filter_value)
                elif expected_type == str:
                    filter_value = str(filter_value)
                # For other types, you can add more checks if needed (e.g., float, bool)
            except ValueError:
                # If the casting fails, show an error message box
                QMessageBox.warning(None, "Invalid Input",
                                    f"Please enter a valid {expected_type.__name__} for the column '{column_name}'.")
                return []

        for _ in range(50):
            row = [
                fake.name(),  # Name
                random.randint(20, 60),  # Age
                fake.job(),  # Job
            ]

            # If dates are provided, generate date within the range, else use a random date
            if start_date and end_date:
                row.append(fake.date_between(start_date=start_date, end_date=end_date).strftime("%Y-%m-%d"))  # Date
            else:
                row.append(fake.date_this_century().strftime("%Y-%m-%d"))  # Random date from this century

            # If no column is selected, return all data without filtering by column value
            if not column_name:
                dummy_data.append(row)
            elif str(row[DataHandler.get_columns().index(column_name)]) == str(filter_value):
                dummy_data.append(row)

        return dummy_data if dummy_data else [["No Data", "", "", ""]]