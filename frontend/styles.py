class Styles:
    @staticmethod
    def login_styles():
        """Login Page Styles with black text"""
        return """
            QWidget {
                background-color: #f4f4f9;
                font-size: 14px;
                font-family: 'Arial', sans-serif;
            }
            QLabel {
                color: black;  /* Set text color to black */
                margin-bottom: 10px;
            }
            QLineEdit {
                padding: 10px;
                border: 1px solid #ddd;
                border-radius: 5px;
                margin-bottom: 20px;
                font-size: 14px;
                color: black;  /* Set text color to black */
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 12px 20px;
                border-radius: 5px;
                border: none;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """

    @staticmethod
    def dashboard_styles():
        """Dashboard Page Styles with black text"""
        return """
            QWidget {
                background-color: #ffffff;
                font-family: 'Arial', sans-serif;
                color: black;  /* Set text color to black */
            }
            QComboBox {
                padding: 10px;
                border: 1px solid #ccc;
                border-radius: 8px;
                background-color: white;
                font-size: 14px;
                color: black;  /* Set text color to black */
            }
            QComboBox:editable {
                background-color: #e6f7ff;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: url(":/images/arrow_down.png");
            }
            QPushButton {
                background-color: #0099ff;
                color: white;
                padding: 10px 15px;
                border-radius: 5px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #007acc;
            }
        """

    @staticmethod
    def table_styles():
        """Table Styles with professional look"""
        return """
            QTableWidget {
                font-family: 'Arial', sans-serif;
                border: 2px solid #ddd;
                border-radius: 8px;
                background-color: #fafafa;
                color: black;  /* Set text color to black */
                gridline-color: #ddd;
                padding: 10px;
            }

            QTableWidget::item {
                padding: 10px;
                border-bottom: 1px solid #ddd;
            }

            QTableWidget::item:selected {
                background-color: #cce4ff;  /* Highlight selected row */
                color: black;
            }

            QTableWidget::horizontalHeader {
                background-color: #4CAF50;
                color: white;
                font-weight: bold;
                padding: 10px;
                border: 1px solid #ddd;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
            }

            QTableWidget::horizontalHeader::section {
                font-size: 16px;
                border: 1px solid #ddd;
                padding: 10px;
            }

            QTableWidget::verticalHeader {
                background-color: #f1f1f1;
                color: black;
                border-right: 1px solid #ddd;
                padding: 5px;
            }

            QTableWidget::verticalHeader::section {
                font-size: 16px;
                font-weight: bold;
                border: 1px solid #ddd;
                padding: 5px;
            }

            QTableWidget::item:hover {
                background-color: #e0f7fa;  /* Hover effect on items */
            }

            QTableWidget::horizontalHeader::section:hover {
                background-color: #45a049;
            }
        """

    @staticmethod
    def date_picker_styles():
        """Styles for Date Pickers"""
        return """
                QDateEdit {
                    font-size: 16px;
                    padding: 8px;
                    border: 2px solid #ccc;
                    border-radius: 8px;
                    background-color: #f9f9f9;
                }
                QDateEdit:focus {
                    border: 2px solid #007BFF;
                    background-color: #ffffff;
                }
            """

    @staticmethod
    def clear_button_styles():
        """Styles for the clear button"""
        return """
                QPushButton {
                    border: none; 
                    font-size: 22px; 
                    font-weight: bold;
                    color: red; 
                    background-color: transparent;
                    padding: 5px;
                }
                QPushButton:hover {
                    color: darkred;
                    background-color: rgba(255, 0, 0, 0.2);  /* Light red hover effect */
                }
            """

    @staticmethod
    def filter_input_styles():
        """Styles for the filter input field"""
        return """
                QLineEdit {
                    font-size: 16px;
                    padding: 5px;
                    border: 2px solid #ccc;
                    border-radius: 8px;
                    background-color: #f9f9f9;
                }
                QLineEdit:focus {
                    border: 2px solid #007BFF;  /* Blue highlight on focus */
                    background-color: #ffffff;
                }
            """

    @staticmethod
    def apply_styles(widget, style_name):
        """Applies the appropriate style to the given widget"""
        if style_name == "login":
            widget.setStyleSheet(Styles.login_styles())
        elif style_name == "dashboard":
            widget.setStyleSheet(Styles.dashboard_styles())
        elif style_name == "table":
            widget.setStyleSheet(Styles.table_styles())
        elif style_name == "date_picker":
            widget.setStyleSheet(Styles.date_picker_styles())
        elif style_name == "clear_button":
            widget.setStyleSheet(Styles.clear_button_styles())
        elif style_name == "filter_input":
            widget.setStyleSheet(Styles.filter_input_styles())