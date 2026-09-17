"""
# Core event model for a calendar app.

# Design idea:
# - An Event has a start (datetime) and a duration (timedelta).
#   Duration naturally lets an event cross midnight -- you don't need
#   any special "spans two days" flag, a timedelta of e.g. 5 hours
#   starting at 22:00 just ends at 03:00 the next day.
# - Recurrence is a separate concern layered on top: given a base event,
#   "does this event occur on day X?" expands the recurrence rule and
#   checks each candidate occurrence.

# Next steps once this feels right:
#   - persist events (JSON to start, SQLite later)
#   - hook get_events_on_day() into your existing `calendar` module output
#   - eventually swap print statements for a real UI
#

# from dataclasses import dataclass, field
# from datetime import datetime, timedelta, date
# from enum import Enum
# from typing import Optional, List, Tuple
# import itertools


# class Recurrence(Enum):
#     NONE = "none"
#     DAILY = "daily"
#     WEEKLY = "weekly"
#     MONTHLY = "monthly"
#     YEARLY = "yearly"
"""


import datetime as dt
from datetime import timedelta
import calendar

""" target_datetime = dt.datetime(2030,1,2,12,30,1)
# current = dt.datetime.now()

# if target_datetime < current :
#     print('passed')
# else : 
#     print('it is yet to come') """

"""I have to have 2 DIFFERENT DATES THEN USE TIMEDELTA
HOLY CRAP"""


import sys
import datetime
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QCalendarWidget, QPushButton, QMainWindow
)
from PyQt6.QtCore import QDate
from PyQt6.QtGui import QFont, QFontDatabase

from EventSystem import Events, eventsystem

class Calendar(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Interactive PyQt5 Calendar")
        self.setGeometry(300, 150, 450, 400)

         
        font_id = QFontDatabase.addApplicationFont("Cave-Story.ttf")

        if font_id != -1:
            font_family = QFontDatabase.applicationFontFamilies(font_id)[0]

        # label = QLabel("title", self) #for my understanding > self means the Window
        # label.setFont(QFont(font_family,60))

        layout = QVBoxLayout()

        # Label to display the selected date
        self.info_label = QLabel("Selected Date: None")
        self.info_label.setFont(QFont(font_family, 20, QFont.Weight.Bold))
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
        today_btn.setFont(QFont(font_family,25))

        from EventSystem import Events

        self.event_button = QPushButton('Event adder', self)
        # self.event_button.setGeometry (150,200,400,200) #(x,y,width,height)
        self.event_button.setFont(QFont(font_family,25))
        self.event_button.clicked.connect(self.on_click)
        


        layout.addLayout(bottom_layout)
        layout.addWidget(self.event_button)

        self.setLayout(layout)

        # Display current date on startup
        self.on_date_selected()

    def on_click(self):
            self.window = Events()
            self.window.show()

    def on_date_selected(self):
        """Triggered whenever the user clicks a date on the calendar."""
        selected_qdate = self.calendar.selectedDate()
        # Format QDate into a readable string (e.g., 'Tuesday, August 18, 2026')
        formatted_date = selected_qdate.toString("dddd, MMMM d, yyyy")
        self.info_label.setText(f"Selected Date: {formatted_date}")
        # self.open_main_window(QDate)

    def go_to_today(self):
        """Resets the calendar view and selection to today's date."""
        today = QDate.currentDate()
        self.calendar.setSelectedDate(today)

    # def on_date_double_click(self):
    #     selected_qdate = self.calendar.selectedDate()
        
    # def open_main_window(self, date):
        # print("Double clicked date:", self)
        # self.popup_window = MainWindow()
        # self.popup_window.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Calendar()
    window.show()
    sys.exit(app.exec())

