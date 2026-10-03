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

event_folder_checker = Path.cwd()/"Events"
if (event_folder_checker.exists()): #check if the folder named "todolists" exist
# print('this file exists') << old code, used and being kept for trouble shooting
    pass
else : 
    os.mkdir('Events')

event_folder = Path.cwd()/"Events"
json_file = event_folder/"My events.json" #PATHLIB : finds (or the intended use for this, create) a file with the name
event_files = event_folder.iterdir() #PATHLIB : views the files in the directory
empty_chker = not any(event_files) #PATHLIB : checks if the directory has any files


if empty_chker :
        json_file.write_text(json.dumps([]), encoding="utf-8")
        
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
        self.newlist.clicked.connect(self.new_event_file)
        

        "button that deletes a list"
        self.byelist = QPushButton('Delete list')
        self.byelist.setFont(QFont(font_family,20))
        self.byelist.clicked.connect(self.delete_event_file)
        

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
        #THIS ONE IS FOR THE FILE/TYPE OF EVENTS\
        global eventsfolder
        eventsfolder = Path.cwd()/"Events"
        # print(f"eventsfolder is {eventsfolder}") << used for troubleshooting
        jsononly = list(eventsfolder.glob("*json"))
        for file in eventsfolder.iterdir():
            print(file.name)
        print(jsononly)

        
        names = [file.stem for file in eventsfolder.glob("*.json")]
        print(names)

        self.dropdownlabel = QLabel('Save to:')
        self.dropdownlabel.setFont(QFont(font_family,20))
        self.dropdown = QComboBox()
        self.dropdown.setFont(QFont(font_family, 20))
        self.dropdown.setEditable(True)
        self.dropdown.setInsertPolicy(QComboBox.InsertPolicy.NoInsert)
        self.dropdown.currentIndexChanged.connect(self.beforerename)
        self.dropdown.lineEdit().editingFinished.connect(self.renamer)
        self.dropdown.addItems(names)

        self.originalname = self.dropdown.currentText()

        
        # self.dropdown = 


        "This one here is for the recurrence"
        self.recurrencelabel =  QLabel('Repeats?')
        self.recurrencelabel.setFont(QFont(font_family,20))
        self.recurrencelabel.setGeometry(0,10,0,0)


        self.recurrence = QComboBox()
        self.recurrence.setFont(QFont(font_family, 20))
        pry = self.recurrence.addItems(['No','Weekly','Monthly', 'Yearly', 'Custom'])
        self.recurrence.currentTextChanged.connect(self.customEnable)


        self.recurrenceEndlabel = QLabel('Goes on:')
        self.recurrenceEndlabel.setFont(QFont(font_family, 20))
        self.recurrenceEndlabel.setVisible(False)
        self.recurrenceEnd = QComboBox()
        self.recurrenceEnd.setFont(QFont(font_family, 20))
        self.recurrenceEnd.addItems(["Forever", "Until a date"])
        self.recurrenceEnd.setVisible(False)
        self.recurrenceEnd.currentTextChanged.connect(self.toggleEndDateField)

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
        # ========================================================   why did i write it like this lmao?
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
        RepeatOrNO.addRow(self.recurrenceEndlabel, self.recurrenceEnd)

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

        event_name = self.label.text().strip()
        if not event_name:
            print("No event name entered — nothing saved.")
            return

        selected_file = self.dropdown.currentText()
        if not selected_file:
            print("No category selected — nothing saved.")
            return

        # event_start = self.date_picker.dateTime().toPyDateTime()   # ORIGINAL -- self.date_picker doesn't exist, left here commented out

        # self.customrecurrence.dateTime().toPyDateTime   # ORIGINAL -- left untouched, does nothing (no parentheses)

        # --- ADDED: pull recurrence choice, map it to a stored value ---
        recurrence_choice = self.recurrence.currentText()
        recurrence_map = {
            "No": "none",
            "Weekly": "weekly",
            "Monthly": "monthly",
            "Yearly": "yearly",
            "Custom": "daily",   # Custom = repeats daily, bounded by From/To
        }
        recurrence_value = recurrence_map.get(recurrence_choice, "none")

        # --- ADDED: decide where the date/recurrence_end come from, based on the choice above ---
        if recurrence_choice == "Custom":
            start_qdate = self.customrecurrence.date()
            end_qdate = self.customrecurrenceEnd.date()

            if start_qdate > end_qdate:   # ADDED: basic sanity check
                print("Custom 'From' date is after 'To' date — nothing saved.")
                return

            event_date_str = start_qdate.toString("ddMMyyyy")
            recurrence_end_str = end_qdate.toString("ddMMyyyy")
        else:
            event_date_str = self.manualdateselector.date().toString("ddMMyyyy")
            recurrence_end_str = None

        event_time_str = self.hourselector.time().toString("HH:mm")
        # --- END ADDED ---

        event_data = {
            "event_name": event_name,
            "event_date": event_date_str,          # CHANGED: built above, not from date_picker
            "event_time": event_time_str,          # CHANGED: built above, not from date_picker
            "duration_minutes": 0,       # TODO: pull from a duration input once one exists
            "recurrence": recurrence_value,        # CHANGED: now pulled from self.recurrence
            "recurrence_end": recurrence_end_str,  # CHANGED: now pulled from custom From/To when applicable
        }

        file_path = eventsfolder / f"{selected_file}.json"

        with open(file_path, 'r') as f:
            data = json.load(f)
        data.append(event_data)
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)

        print(f"Saved '{event_name}' to {selected_file}.json")
        self.label.clear()

        if hasattr(self, "load_events_into_list"):   # CHANGED: guarded -- this method isn't defined in your current file yet
            self.load_events_into_list()

    def eventfilefinder(self):
        FolderWhereYouKeepTheEventFiles = Path.cwd()/"events"
        index = self.dropdown.currentText()
        pathtofile = self.dropdown.itemData(index)

        

        


    def renamer(self):
        index = self.dropdown.currentIndex()
        new_name = self.dropdown.currentText().strip()

        if not new_name:
            return

        OldFileName = self.dropdown.itemData(index)
        NewFileName = self.dropdown.with_name(new_name + ".json")

        if OldFileName == NewFileName:
            return

        try:
            OldFileName.rename(NewFileName)
            self.dropdown.setItemData(index, NewFileName)
            self.dropdown.setItemText(index, new_name)

        except FileExistsError :
            print(f"the file named {new_name} already exists")

        except FileNotFoundError:
            print("can't find this file")

        pathtofile = self.dropdown.itemData(index)

        with open(pathtofile, 'r') as file:
            venter = json.load(file)
            

    def date_fetcher(self):
        datewanted = self.calendardate.datefetcher()
        print(datewanted)

    def on_calendar_date_changed(self):
        selected_qdate = self.calendardate.datefetcher()   # fetch current value, fresh
        current_time = self.hourselector.time()
        self.manualdateselector.setDate(QDate(selected_qdate))
        self.hourselector.setTime(QTime(current_time))

    def customEnable(self):
        # textwanted = 'Custom'
        # recurrentselection = self.recurrence.currentText(
        # )
        # self.customrecurrence.setEnabled(textwanted == recurrentselection)
        # self.customrecurrenceEnd.setEnabled(textwanted == recurrentselection)

        userchoice = self.recurrence.currentText()
        textwanted = (userchoice == "Custom")

        self.customrecurrence.setEnabled(textwanted)

        if textwanted:
            self.customrecurrenceEnd.setEnabled(True)
            self.recurrenceEnd.setVisible(False)
            self.recurrenceEndlabel.setVisible(False)
        elif userchoice == "No":
            self.customrecurrenceEnd.setEnabled(False)
            self.recurrenceEnd.setVisible(False)
            self.recurrenceEndlabel.setVisible(False)
        else:  # Weekly / Monthly / Yearly
            self.recurrenceEnd.setVisible(True)
            self.recurrenceEndlabel.setVisible(True)
            self.customrecurrenceEnd.setEnabled(self.recurrenceEnd.currentText() == "Until a date")

    def toggleEndDateField(self):
        choice = self.recurrence.currentText()
        if choice not in ("No", "Custom"):
            self.customrecurrenceEnd.setEnabled(self.recurrenceEnd.currentText() == "Until a date")


    def dateselectorgetter(self):
        return self.manualdateselector.date()

    def hourselectorgetting(self):
        return self.hourselector.time()

    def selected_event_file(self):
        currentfile = self.dropdown.currentText()
        PathToFile = Path.cwd()/"Events"/f"{currentfile}".json

        with open(PathToFile, 'r') as file:
            data = json.load(file)

        #data.append(event_date)

        with open(PathToFile, 'w') as file :
            json.dump(data, indent=4) #rewrite as (data, f, indent=4)

    def refreshdropdownlist(self):
        names = [file.stem for file in eventsfolder.glob("*.json")]

       # block currentindexchanged from returning anything during this process
        self.dropdown.clear()
        self.dropdown.addItems(names)
        
        

    def new_event_file(self, name: str):
        defaultname = "New Event file"
        name = defaultname
        counter = 1
        
        while (eventsfolder/f"{name}.json").exists():
            name = f"{defaultname} ({counter})"
            counter += 1

        the_path =  eventsfolder/f"{name}.json"
        the_path.write_text(json.dumps([]))

        self.dropdown.blockSignals(True)
        self.refreshdropdownlist()
        self.dropdown.setCurrentText(name)
        self.dropdown.blockSignals(False)

        self.oldname= name

    def delete_event_file(self):
        selectedfile = self.dropdown.currentText()
        pathtofile = eventsfolder/f"{selectedfile}.json"

        if pathtofile.exists():
            pathtofile.unlink() #UNLINK is pathlib's way to delete files
        self.refreshdropdownlist()

    def beforerename(self):
            self.originalname = self.dropdown.currentText()

    def renamer(self):
        new_name = self.dropdown.currentText()
        old_name = self.originalname

        if new_name == old_name or not new_name.strip(): return

        old_path = eventsfolder/f"{old_name}.json"
        new_path = eventsfolder/f"{new_name}.json"

        if not old_path.exists():
            return
        if new_path.exists():
            return

        old_path.rename(new_path)

        self.dropdown.blockSignals(True)
        self.refreshdropdownlist()
        self.dropdown.setCurrentText(new_name)
        self.dropdown.blockSignals(False)

        self.originalname = new_name


    


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
