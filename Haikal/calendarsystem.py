import datetime as dt
from datetime import timedelta
import calendar

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QCalendarWidget, QPushButton, QStackedWidget
)
from PyQt6.QtCore import QDate
from PyQt6.QtCore import QDate
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
        self.event_window = Events()
        self.event_window.show()

    def on_date_selected(self):
        """Triggered whenever the user clicks a date on the calendar."""
        selected_qdate = self.calendar.selectedDate()
        formatted_date = selected_qdate.toString("dddd, MMMM d, yyyy")
        self.info_label.setText(f"Selected Date: {formatted_date}")

    def go_to_today(self):
        """Resets the calendar view and selection to today's date."""
        today = QDate.currentDate()
        self.calendar.setSelectedDate(today)

    def open_music_settings(self):
        MusicDialog(self.music, parent=self).exec()
