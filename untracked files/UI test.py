import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, 
    QLabel, QLineEdit, QPushButton
)

class BasicApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Configure Main Window
        self.setWindowTitle("PyQt5 Quickstart")
        self.setGeometry(100, 100, 300, 150)

        # Create Layout & Widgets
        layout = QVBoxLayout()

        self.label = QLabel("Enter your name:", self)
        layout.addWidget(self.label)

        self.input_field = QLineEdit(self)
        layout.addWidget(self.input_field)

        self.btn = QPushButton("Submit", self)
        layout.addWidget(self.btn)

        # Signals & Slots: Connect button click to function
        self.btn.clicked.connect(self.on_click)

        self.setLayout(layout)

    def on_click(self):
        user_text = self.input_field.text()
        if user_text.strip():
            self.label.setText(f"Hello, {user_text}!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BasicApp()
    window.show()
    sys.exit(app.exec_())