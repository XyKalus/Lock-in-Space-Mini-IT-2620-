""" Student name : Haikal Areef Bin Reezal
ID : 253FC251BR

placeholder text here for me to use 
"""


import datetime as dt
from datetime import timedelta
import calendar
import sys, os
import PyQt6
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QGridLayout, QPushButton, QLineEdit, QComboBox, QDateEdit, QTimeEdit, QDateTimeEdit
from PyQt6.QtGui import QIcon, QFont, QFontDatabase
from PyQt6.QtCore import Qt, QDate, QTime, QDateTime #Qt is used for alignment

import json
import pathlib
from pathlib import Path

event_folder_checker = Path.cwd()/"events"
if (event_folder_checker.exists()): #check if the folder named "todolists" exist
# print('this file exists') << old code, used and being kept for trouble shooting
    pass
else : 
    os.mkdir('events')

event_folder = Path.cwd()/"events"
json_file = event_folder/"My events.json" #PATHLIB : finds (or the intended use for this, create) a file with the name
event_files = event_folder.iterdir() #PATHLIB : views the files in the directory
empty_chker = not any(event_files) #PATHLIB : checks if the directory has any files


if empty_chker :
        json_file.write_text(json.dumps(['test']), encoding="utf-8")
        print("File created using pathlib!") #Thank you Gemini for the help lol
else :
        print('has files')
        pass

    
class Events(QMainWindow): #self in the entire function refers to the "MainWindow" class (adding this here as a reminder to myself)
    def __init__(self, calendardate):
        super().__init__()
        self.setWindowTitle('Set an event date') # title of the window
        self.setGeometry(600,250,490,80) # (x,y,width,height)
        self.setWindowIcon(QIcon("cat.png")) #Window Icon (the thing you see on the top left)

        self.calendardate = calendardate

        # self.calendardate.calendar.selectionChanged.connect(self.on_calendar_date_changed)
        
        print(type(calendardate))
        
        self.initUI() #initialise the "layout" manager

    def initUI(self): #you can't normally make a layout manager inside of MainWindow, the method is : Create a main.central widget > Create the layout manager within the widget, the main widget is then added to the window (in this case (MainWindow class)), learning sources : Bro Code (YouTube)
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        
        font_id = QFontDatabase.addApplicationFont("Cave-Story.ttf")

        if font_id != -1:
            font_family = QFontDatabase.applicationFontFamilies(font_id)[0]


        "Input field"
        self.label = QLineEdit() #for my understanding > self means the Window
        self.label.setPlaceholderText('type your event here')
        self.label.setFont(QFont(font_family,30))
        self.label.setGeometry(0,0,90,90) #(x,y,width,height)
        self.label.setStyleSheet("color: black;"
                            "background-color: white;") # this code is only here for testing, will either keep or change
        # label.setAlignment(Qt.AlignHCenter | Qt.AlignTop) # controls the alignment of the label, the | is used to label 2 css properties at once

        "button that adds the input"
        self.event_button = QPushButton('Save Event', self)
        USEREVENT = self.event_button
        # self.event_button.setGeometry (150,200,400,200) #(x,y,width,height)
        self.event_button.setFont(QFont(font_family,25))
        self.event_button.clicked.connect(self.on_click)

        "button that makes a new list"
        self.newlist = QPushButton('New Event list')
        self.newlist.setFont(QFont(font_family,20))

        "button that deletes a list"
        self.byelist = QPushButton('Delete list')
        self.byelist.setFont(QFont(font_family,20))

        "MANUAL DATE SELECTOR >> this is for the date selector INSIDE this thing"
        self.manualdateselector = QDateEdit()
        self.manualdateselector.setCalendarPopup(True)
        self.manualdateselector.setDate(QDate.currentDate())
        self.manualdateselector.setDisplayFormat("dd/MM/yyyy")
        self.manualdateselector.setFont(QFont(font_family, 20))

        "MANUAL HOUR SELECTOR>> this is the thing lets you set the hour of the event"
        self.hourselector = QTimeEdit()
        self.hourselector.setTime(QTime.currentTime())
        self.hourselector.setDisplayFormat("HH:mm")
        self.hourselector.setFont(QFont(font_family, 20))

        "making....a dropdown for the events..."
        #THIS ONE IS FOR THE FILE/TYPE OF EVENTS
        eventsfolder = Path.cwd()/"events"
        jsononly = list(eventsfolder.glob("*json"))
        for file in eventsfolder.iterdir():
            print(file.name)
        print(jsononly)

        self.dropdownlabel = QLabel('Save to:')
        self.dropdownlabel.setFont(QFont(font_family,20))
        self.dropdown = QComboBox()
        self.dropdown.setEditable(True)
        self.dropdown.setInsertPolicy(QComboBox.InsertPolicy.NoInsert)
        # self.dropdown.lineEdit().editingFinished.connect.self(self.renamer)
        # self.dropdown.addItems(eventsfolder)

        
        # self.dropdown = 


        "This one here is for the recurrence"
        self.recurrencelabel =  QLabel('Repeats?')
        self.recurrencelabel.setFont(QFont(font_family,20))
        self.recurrencelabel.setGeometry(0,10,0,0)


        self.recurrence = QComboBox()
        self.recurrence.setFont(QFont(font_family, 20))
        pry = self.recurrence.addItems(['No','Weekly','Monthly', 'Yearly', 'Custom'])
        self.recurrence.currentTextChanged.connect(self.customEnable)


        self.customrecurrencelabel = QLabel('From:')
        self.customrecurrencelabel.setFont(QFont(font_family,20))
        self.customrecurrence = QDateTimeEdit()
        self.customrecurrence.setFont(QFont(font_family,20))
        self.customrecurrence.setEnabled(False)
        self.customrecurrence.setCalendarPopup(True)
        self.customrecurrence.setDate(QDate.currentDate())

        self.customrecurrenceEndlabel = QLabel('To:')
        self.customrecurrenceEndlabel.setFont(QFont(font_family,20))
        self.customrecurrenceEnd = QDateTimeEdit()
        self.customrecurrenceEnd.setFont(QFont(font_family,20))
        self.customrecurrenceEnd.setEnabled(False)
        self.customrecurrenceEnd.setCalendarPopup(True)
        self.customrecurrenceEnd.setDate(QDate.currentDate())


        # =======================================================
        # THIS ONE IS FOR FETCHING THE SELECTED DATE FROM CALENDAR
        # ========================================================
        self.tester = QLabel()
        self.button_test = QPushButton('get date')

        self.button_test.clicked.connect(self.date_fetcher)
        
        


        "All layouts  down here"

        layout = QVBoxLayout() #<<<< MAIN LAYOUT
        DateAndTime = QHBoxLayout() #<<<<< FOR THE EVENT AND TIME SELECTOR THINGY 
        RepeatOrNO = QFormLayout() # <<<< FOR THE RECURRENCE SETTER 
        horizontal = QHBoxLayout() #<<< FOR MAKING AND DELETING LISTS BUTTON

        horizontal.addWidget(self.newlist)
        horizontal.addWidget(self.byelist)

        DateAndTime.addWidget(self.manualdateselector)
        DateAndTime.addWidget(self.hourselector)

        RepeatOrNO.addRow(self.recurrencelabel, self.recurrence)

        RepeatOrNO.addRow(self.customrecurrencelabel, self.customrecurrence)
        RepeatOrNO.addRow(self.customrecurrenceEndlabel, self.customrecurrenceEnd)
        RepeatOrNO.addRow(self.dropdownlabel, self.dropdown)

        layout.addWidget(self.label)
        layout.addLayout(DateAndTime)
        layout.addLayout(RepeatOrNO)
        # layout.addWidget(self.tester)
        # layout.addWidget(self.button_test)
        layout.addLayout(horizontal)
        layout.addWidget(self.event_button)
        


        central_widget.setLayout(layout)

    def on_click(self): #<<< make this save the input 
        print('event added!')
        ayamgepuk = self.label.text()
        print(ayamgepuk)

        # file_path = Path.cwd()/"events"/"My events.json"

        # with open(file_path, 'r') as f:
        #         todo = json.load(f)

        # todo['test'].append({
        #         "task" : todo,
        #         "completed" : False,
        # })

        # with open(file_path,'w') as f:
        #         json.dump(todo, f, indent=4)

    def eventfilefinder(self):
        FolderWhereYouKeepTheEventFiles = Path.cwd()/"events"
        index = self.dropdown.currentText()
        pathtofile = self.dropdown.itemData(index)

        

        


    def renamer(self):
        pass

    def date_fetcher(self):
        datewanted = self.calendardate.datefetcher()
        print(datewanted)

    def on_calendar_date_changed(self):
        selected_qdate = self.calendardate.datefetcher()   # fetch current value, fresh
        current_time = self.hourselector.time()
        self.manualdateselector.setDate(QDate(selected_qdate))
        self.hourselector.setTime(QTime(current_time))

    def customEnable(self):
        textwanted = 'Custom'
        recurrentselection = self.recurrence.currentText(
        )
        self.customrecurrence.setEnabled(textwanted == recurrentselection)
        self.customrecurrenceEnd.setEnabled(textwanted == recurrentselection)

    def dateselectorgetter(self):
        return self.manualdateselector.date()

    def hourselectorgetting(self):
        return self.hourselector.time()





            
    

class FakeCalendar:
    def datefetcher(self):
        return QDate.currentDate()
   
            
        

def main():
    app = QApplication(sys.argv)
    window = Events(calendardate=FakeCalendar())
    window.setWindowFlags(window.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)
    window.show()
    sys.exit(app.exec())       

if __name__ == "__main__":
    main()
