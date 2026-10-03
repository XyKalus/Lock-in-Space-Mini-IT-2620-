import PyQt6
import pathlib 
import sys
import os
from pathlib import Path
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *


class EventList(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("My Events")
        self.setGeometry(300, 150, 450, 400)

        font_id = QFontDatabase.addApplicationFont("Cave-Story.ttf")
        
        if font_id != -1:
            font_family = QFontDatabase.applicationFontFamilies(font_id)[0]

        self.List = QListWidget()
        my_event_lists = Path.cwd()/"events"
        said_event_lists = my_event_lists.iterdir()
        print(said_event_lists)
        location_of_lists = os.chdir(my_event_lists)
        print([location_of_lists])

        self.btn = QPushButton("Calendar")
        self.btn.setFont(QFont(font_family, 50))
        self.btn.clicked.connect(self.SwitchToCalendar)

        layout = QFormLayout()
        layout.addWidget(self.btn)

        self.setLayout(layout)

    def SwitchToCalendar(self):
        if self.main_window:
            self.main_window.show.SwitchToCalendar()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EventList()
    window.show()
    sys.exit(app.exec())