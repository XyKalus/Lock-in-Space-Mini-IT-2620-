# """
# # Core event model for a calendar app.

# # Design idea:
# # - An Event has a start (datetime) and a duration (timedelta).
# #   Duration naturally lets an event cross midnight -- you don't need
# #   any special "spans two days" flag, a timedelta of e.g. 5 hours
# #   starting at 22:00 just ends at 03:00 the next day.
# # - Recurrence is a separate concern layered on top: given a base event,
# #   "does this event occur on day X?" expands the recurrence rule and
# #   checks each candidate occurrence.

# # Next steps once this feels right:
# #   - persist events (JSON to start, SQLite later)
# #   - hook get_events_on_day() into your existing `calendar` module output
# #   - eventually swap print statements for a real UI
# #

# # from dataclasses import dataclass, field
# # from datetime import datetime, timedelta, date
# # from enum import Enum
# # from typing import Optional, List, Tuple
# # import itertools


# # class Recurrence(Enum):
# #     NONE = "none"
# #     DAILY = "daily"
# #     WEEKLY = "weekly"
# #     MONTHLY = "monthly"
# #     YEARLY = "yearly"
# """


# import datetime as dt
# from datetime import timedelta
# import calendar

# """ target_datetime = dt.datetime(2030,1,2,12,30,1)
# # current = dt.datetime.now()

# # if target_datetime < current :
# #     print('passed')
# # else : 
# #     print('it is yet to come') """

# """I have to have 2 DIFFERENT DATES THEN USE TIMEDELTA
# HOLY CRAP"""


# import sys
# import datetime
# from PyQt6.QtWidgets import (
#     QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
#     QLabel, QCalendarWidget, QPushButton, QStackedWidget
# )
# from PyQt6.QtCore import QDate
# from PyQt6.QtGui import QFont, QFontDatabase


# class CalendarMainWindow(QWidget):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self.initUI()

#     def initUI(self):

#         self.setWindowTitle("Your Calendar")
#         # self.setGeometry(300, 150, 450, 400)

#         self.innerwidgetlol = QStackedWidget()
        
#         font_id = QFontDatabase.addApplicationFont("Cave-Story.ttf")

#         if font_id != -1:
#             font_family = QFontDatabase.applicationFontFamilies(font_id)[0]

#         # label = QLabel("title", self) #for my understanding > self means the Window
#         # label.setFont(QFont(font_family,60))

#         main_layout = QVBoxLayout(self)

#         """Calendar Widget"""
        
#         self.calendar_system = QWidget()
#         calendar_layout = QVBoxLayout(self.calendar_system)

        
#         self.btn = QPushButton("Go to Events")
#         self.btn.setGeometry(0,0,20,30)
#         self.btn.clicked.connect(self.SwitchToEventView)
#         self.btn.setFont((QFont(font_family, 20, QFont.Weight.Bold)))
#         # layout.addWidget(self.btn)

#         # Label to display the selected date
#         self.info_label = QLabel("Selected Date: None")
#         self.info_label.setFont(QFont(font_family, 20, QFont.Weight.Bold))
#         # layout.addWidget(self.info_label)

#         # Interactive QCalendarWidget
#         self.calendar = QCalendarWidget(self)
#         self.calendar.setGridVisible(True)  # Shows grid lines between days

        
#         # Connect date selection signal to slot function
#         self.calendar.selectionChanged.connect(self.on_date_selected)
#         self.calendar.setFont(QFont(font_family,25))
#         # layout.addWidget(self.calendar)

#         # Bottom Controls: Quick reset button
#         bottom_layout = QHBoxLayout()
#         today_btn = QPushButton("Go to Today")
#         today_btn.clicked.connect(self.go_to_today)
#         bottom_layout.addWidget(today_btn)
#         today_btn.setFont(QFont(font_family,25))

#         """Event System pop up down here"""

#         # from EventSystem import Events

#         self.event_button = QPushButton('Event adder', self)
#         # self.event_button.setGeometry (150,200,400,200) #(x,y,width,height)
#         self.event_button.setFont(QFont(font_family,25))
#         self.event_button.clicked.connect(self.on_click)

#         self.close_button = QPushButton('X', self)
#         self.close_button.setFont(QFont(font_family,25))
#         # self.close_button.clicked.connect(self.homepage)

#         "Calendar Widget stuff here"
#         calendar_layout.addWidget(self.close_button)
#         calendar_layout.addWidget(self.btn)
#         calendar_layout.addWidget(self.info_label)
#         calendar_layout.addWidget(self.calendar)
#         calendar_layout.addLayout(bottom_layout)
#         calendar_layout.addWidget(self.event_button)
        

        
        
#         # Display current date on startup
#         self.on_date_selected()

#         # layout.addLayout(bottom_layout)
#         # layout.addWidget(self.event_button)

#         "Events Viewer"

#         self.myevents = QWidget()
#         myevents_layout = QVBoxLayout(self.myevents)
        

#         self.eventsbtn = QPushButton('Go to Calendar')
#         self.eventsbtn.setGeometry(0,0,20,30)
#         self.eventsbtn.clicked.connect(self.SwitchToCalendarView)
#         self.eventsbtn.setFont((QFont(font_family, 20, QFont.Weight.Bold)))
#         # myevents_layout.addWidget(self.eventsbtn)

#         myevents_layout.addWidget(self.eventsbtn)
#         myevents_layout.addWidget(QLabel('I exist for the sake of testing'))

#         "Layout down here"
        
#         main_layout.addWidget(self.innerwidgetlol)
#         # layout.addWidget(self.innerwidgetlol)
        

#         # self.setLayout(layout)

#         # main_layout.addWidget(self.calendar_system)
#         # main_layout.addWidget(self.myevents)

#         # self.setLayout(main_layout)
#         # main_layout.addLayout(calendar_layout)
#         # main_layout.addLayout(myevents_layout)
#         # main_layout.addWidget(self.innerwidgetlol)
#         # self.setLayout(main_layout)

#         self.innerwidgetlol.addWidget(self.calendar_system)
#         self.innerwidgetlol.addWidget(self.myevents)

#         main_layout.addWidget(self.innerwidgetlol)

#         "Layout code ends here - Haikal"

        

#     def SwitchToEventView(self):
#         self.innerwidgetlol.setCurrentWidget(self.myevents)

#     def SwitchToCalendarView(self):
#         self.innerwidgetlol.setCurrentWidget(self.calendar_system)

#     # def homepage(self, controller):
#     #     self.innerwidgetlol.setCurrentWidget(lambda: controller.setCurrentIndex(0))

#     def on_click(self):
#             self.window = Events()
#             self.window.show()

#     def on_date_selected(self):
#         """Triggered whenever the user clicks a date on the calendar."""
#         selected_qdate = self.calendar.selectedDate()
#         # Format QDate into a readable string (e.g., 'Tuesday, August 18, 2026')
#         formatted_date = selected_qdate.toString("dddd, MMMM d, yyyy")
#         self.info_label.setText(f"Selected Date: {formatted_date}")
#         # self.open_main_window(QDate)

#     def go_to_today(self):
#         """Resets the calendar view and selection to today's date."""
#         today = QDate.currentDate()
#         self.calendar.setSelectedDate(today)

#     def show_calendar(self):
#         CalendarMainWindow.show()

#     # def on_date_double_click(self):
#     #     selected_qdate = self.calendar.selectedDate()
        
#     # def open_main_window(self, date):
#         # print("Double clicked date:", self)
#         # self.popup_window = MainWindow()
#         # self.popup_window.show()

# # if __name__ == "__main__":
# #     app = QApplication(sys.argv)
# #     window = CalendarMainWindow()
# #     window.show()
# #     sys.exit(app.exec())

import datetime as dt
from datetime import timedelta
import calendar

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QCalendarWidget, QPushButton, QStackedWidget
)
from PyQt6.QtCore import QDate, pyqtSignal
from PyQt6.QtGui import QFont, QFontDatabase
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput

from Haikal.MusicPlayer import *


class CalendarMainWindow(QWidget):
    """
    A page meant to be added to the main window's QStackedWidget.

    - close_button is exposed but NOT connected here. The main window
      connects it to switch back to the home page.
    - Nothing runs on import (no QApplication, no .show()).
    """

    def __init__(self, parent=None, controller=None):
        super().__init__(parent)
        self.initUI()
        self.controller = controller
        self.music = MusicController()

    def initUI(self):

        

        self.setWindowTitle("Your Calendar")

        # Inner stack: calendar view <-> events view
        self.innerwidgetlol = QStackedWidget()

        # Fallback family so font_family always exists, even if the .ttf isn't found
        font_family = "Cave Story"
        font_id = QFontDatabase.addApplicationFont("Cave-Story.ttf")
        if font_id != -1:
            font_family = QFontDatabase.applicationFontFamilies(font_id)[0]

        main_layout = QVBoxLayout(self)

        """Calendar Widget"""

        self.calendar_system = QWidget()
        calendar_layout = QVBoxLayout(self.calendar_system)

        self.btn = QPushButton("Go to Events")
        self.btn.clicked.connect(self.SwitchToEventView)
        self.btn.setFont(QFont(font_family, 20, QFont.Weight.Bold))

        self.musicbtn = QPushButton('set background music')
        self.musicbtn.clicked.connect(self.open_music_settings)

        # Label to display the selected date
        self.info_label = QLabel("Selected Date: None")
        self.info_label.setFont(QFont(font_family, 20, QFont.Weight.Bold))

        # Interactive QCalendarWidget
        self.calendar = QCalendarWidget()
        self.calendar.setGridVisible(True)
        self.calendar.selectionChanged.connect(self.on_date_selected)
        self.calendar.setFont(QFont(font_family, 25))

        # Bottom Controls: Quick reset button
        bottom_layout = QHBoxLayout()
        today_btn = QPushButton("Go to Today")
        today_btn.clicked.connect(self.go_to_today)
        bottom_layout.addWidget(today_btn)
        today_btn.setFont(QFont(font_family, 25))

        """Event System pop up down here"""

        self.event_button = QPushButton("Event adder")
        self.event_button.setFont(QFont(font_family, 25))
        self.event_button.clicked.connect(self.on_click)

        # Main window connects this to go back to the home page
        self.close_button = QPushButton("X")
        self.close_button.setFont(QFont(font_family, 25))

        "Calendar Widget stuff here"
        horizontally = QHBoxLayout()
        horizontally.addWidget(self.musicbtn)
        horizontally.addWidget(self.close_button)

        calendar_layout.addLayout(horizontally)
        calendar_layout.addWidget(self.btn)
        calendar_layout.addWidget(self.info_label)
        calendar_layout.addWidget(self.calendar)
        calendar_layout.addLayout(bottom_layout)
        calendar_layout.addWidget(self.event_button)

        # Display current date on startup
        self.on_date_selected()

        "Events Viewer"

        self.myevents = QWidget()
        myevents_layout = QVBoxLayout(self.myevents)

        self.eventsbtn = QPushButton("Go to Calendar")
        self.eventsbtn.clicked.connect(self.SwitchToCalendarView)
        self.eventsbtn.setFont(QFont(font_family, 20, QFont.Weight.Bold))

        myevents_layout.addWidget(self.eventsbtn)
        myevents_layout.addWidget(QLabel("I exist for the sake of testing"))

        "Layout down here"

        self.innerwidgetlol.addWidget(self.calendar_system)
        self.innerwidgetlol.addWidget(self.myevents)

        # Added once, as the single root widget of this page
        main_layout.addWidget(self.innerwidgetlol)

        "Layout code ends here - Haikal"

    def SwitchToEventView(self):
        self.innerwidgetlol.setCurrentWidget(self.myevents)

    def SwitchToCalendarView(self):
        self.innerwidgetlol.setCurrentWidget(self.calendar_system)

    def on_click(self):
        # Imported here (not at the top) to avoid circular imports.
        # Adjust the module name to wherever your Events class lives.
        from Haikal.EventSystem import Events

        # NOT self.window: that name is a built-in QWidget method
        self.event_window = Events(calendardate=self)
        # self.event_window.windowFlags(Qt.WindowType.WindowStaysOnTopHint)

        self.event_window.show()

    def on_date_selected(self):
        """Triggered whenever the user clicks a date on the calendar."""
        selected_qdate = self.calendar.selectedDate()
        formatted_date = selected_qdate.toString("dddd, MMMM d, yyyy")
        self.info_label.setText(f"Selected Date: {formatted_date}")

    def datefetcher(self):
        return self.calendar.selectedDate()

    def go_to_today(self):
        """Resets the calendar view and selection to today's date."""
        today = QDate.currentDate()
        self.calendar.setSelectedDate(today)

    def open_music_settings(self):
        MusicDialog(self.music, parent=self).exec()

    def get_selected_date(self):
        return self.on_date_selected


# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = CalendarMainWindow()
#     window.show()
#     sys.exit(app.exec())