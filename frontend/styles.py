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
                color: black;
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
    def apply_styles(widget, style_name):
        """Applies the appropriate style to the given widget"""
        if style_name == "login":
            widget.setStyleSheet(Styles.login_styles())
        elif style_name == "dashboard":
            widget.setStyleSheet(Styles.dashboard_styles())
        elif style_name == "table":
            widget.setStyleSheet(Styles.table_styles())
