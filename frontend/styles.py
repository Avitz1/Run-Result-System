from PyQt6.QtWidgets import QWidget, QPushButton, QLineEdit, QDateEdit

class Styles:
    @staticmethod
    def apply_styles(widget, style_type):
        if style_type == "dashboard":
            widget.setStyleSheet("background-color: #f0f0f0;")
        elif style_type == "clear_button":
            widget.setStyleSheet("color: red;")
        elif style_type == "filter_input":
            widget.setStyleSheet("border: 1px solid #ccc;")
        elif style_type == "date_picker":
            widget.setStyleSheet("border: 1px solid #ccc;")