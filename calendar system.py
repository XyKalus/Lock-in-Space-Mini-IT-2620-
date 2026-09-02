"""
Student name :
ID :
Email : 
"""


import sys
import datetime
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QCalendarWidget, QPushButton
)
from PyQt5.QtCore import QDate
from PyQt5.QtGui import QFont

class InteractiveCalendarApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Calendar (W.I.P)")
        self.setGeometry(300, 150, 450, 400)

        layout = QVBoxLayout()

        # Label to display the selected date
        self.info_label = QLabel("Selected Date: None")
        self.info_label.setFont(QFont("Arial", 11, QFont.Bold))
        layout.addWidget(self.info_label)

        # Interactive QCalendarWidget
        self.calendar = QCalendarWidget(self)
        self.calendar.setGridVisible(True)  # Shows grid lines between days
        
        # Connect date selection signal to slot function
        self.calendar.selectionChanged.connect(self.on_date_selected)
        layout.addWidget(self.calendar)

        # Bottom Controls: Quick reset button
        bottom_layout = QHBoxLayout()
        today_btn = QPushButton("Go to Today")
        today_btn.clicked.connect(self.go_to_today)
        bottom_layout.addWidget(today_btn)

        layout.addLayout(bottom_layout)

        self.setLayout(layout)

        # Display current date on startup
        self.on_date_selected()

    def on_date_selected(self):
        """Triggered whenever the user clicks a date on the calendar."""
        selected_qdate = self.calendar.selectedDate()
        # Format QDate into a readable string (e.g., 'Tuesday, August 18, 2026')
        formatted_date = selected_qdate.toString("dddd, MMMM d, yyyy")
        self.info_label.setText(f"Selected Date: {formatted_date}")

    def go_to_today(self):
        """Resets the calendar view and selection to today's date."""
        today = QDate.currentDate()
        self.calendar.setSelectedDate(today)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = InteractiveCalendarApp()
    window.show()
    sys.exit(app.exec_())
