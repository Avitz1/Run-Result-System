from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout
from dashboard import Dashboard
from styles import Styles

class Login(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        Styles.apply_styles(self, "login")  # Applying login styles

    def init_ui(self):
        self.setWindowTitle("Login")
        self.setGeometry(100, 100, 400, 250)

        self.label_user = QLabel("Username:")
        self.input_user = QLineEdit()
        self.input_user.returnPressed.connect(self.focus_password)

        self.label_pass = QLabel("Password:")
        self.input_pass = QLineEdit()
        self.input_pass.setEchoMode(QLineEdit.EchoMode.Password)
        self.input_pass.returnPressed.connect(self.check_login)

        self.btn_login = QPushButton("Login")
        self.btn_login.clicked.connect(self.check_login)

        layout = QVBoxLayout()
        layout.addWidget(self.label_user)
        layout.addWidget(self.input_user)
        layout.addWidget(self.label_pass)
        layout.addWidget(self.input_pass)
        layout.addWidget(self.btn_login)

        self.setLayout(layout)

    def focus_password(self):
        self.input_pass.setFocus()

    def check_login(self):
        username = self.input_user.text()
        password = self.input_pass.text()

        if username == "admin" and password == "password":
            self.open_dashboard()
        else:
            self.input_user.clear()
            self.input_pass.clear()

    def open_dashboard(self):
        self.dashboard = Dashboard()
        self.dashboard.show()
        self.close()
