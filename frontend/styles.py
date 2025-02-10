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
                color: black;
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
    def apply_styles(widget, style_name):
        """Applies the appropriate style to the given widget"""
        if style_name == "login":
            widget.setStyleSheet(Styles.login_styles())
