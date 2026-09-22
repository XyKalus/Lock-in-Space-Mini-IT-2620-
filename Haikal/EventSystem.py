""" Student name : Haikal Areef Bin Reezal
ID : 253FC251BR

placeholder text here for me to use 
"""


import datetime as dt
from datetime import timedelta
import calendar
import sys, os
import PyQt6
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QGridLayout, QPushButton, QLineEdit
from PyQt6.QtGui import QIcon, QFont, QFontDatabase
from PyQt6.QtCore import Qt #Qt is used for alignment

import json
import pathlib
from pathlib import Path

class Events(QMainWindow): #self in the entire function refers to the "MainWindow" class (adding this here as a reminder to myself)
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Set an event date') # title of the window
        self.setGeometry(600,250,400,80) # (x,y,width,height)
        self.setWindowIcon(QIcon("cat.png")) #Window Icon (the thing you see on the top left)
        self.initUI() #initialise the "layout" manager

    def initUI(self): #you can't normally make a layout manager inside of MainWindow, the method is : Create a main.central widget > Create the layout manager within the widget, the main widget is then added to the window (in this case (MainWindow class)), learning sources : Bro Code (YouTube)
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        
        font_id = QFontDatabase.addApplicationFont("Cave-Story.ttf")

        if font_id != -1:
            font_family = QFontDatabase.applicationFontFamilies(font_id)[0]

        label = QLineEdit() #for my understanding > self means the Window
        label.setPlaceholderText('type your event here')
        label.setFont(QFont(font_family,30))
        label.setGeometry(0,0,90,90) #(x,y,width,height)
        label.setStyleSheet("color: black;"
                            "background-color: white;") # this code is only here for testing, will either keep or change
        # label.setAlignment(Qt.AlignHCenter | Qt.AlignTop) # controls the alignment of the label, the | is used to label 2 css properties at once

        self.event_button = QPushButton('Add event', self)
        USEREVENT = self.event_button
        # self.event_button.setGeometry (150,200,400,200) #(x,y,width,height)
        self.event_button.setFont(QFont(font_family,25))
        self.event_button.clicked.connect(self.on_click)

    
        layout = QFormLayout()

        layout.addWidget(label)
        layout.addWidget(self.event_button)

        central_widget.setLayout(layout)

    def on_click(self):
        print('event added!')
        self.event_button.setText(f"{input} added to events!")  #FIGURE OUT HOW THIS WORKS
        event_folder_checker = Path.cwd()/"events"
        if (event_folder_checker.exists()): #check if the folder named "todolists" exist
# print('this file exists') << old code, used and being kept for trouble shooting
            pass
        else : 
            os.mkdir('events')
            todo = Path.cwd()/"events"

            json_file = todo/"My events.json" #PATHLIB : finds (or the intended use for this, create) a file with the name
            todo_files = todo.iterdir() #PATHLIB : views the files in the directory
            empty_chker = not any(todo_files) #PATHLIB : checks if the directory has any files

            if empty_chker :
                    json_file.write_text(json.dumps([]), encoding="utf-8")
                    print("File created using pathlib!") #Thank you Gemini for the help lol
            else :
                    print('has files')
                    pass
            
    

   
            
        

def main():
    app = QApplication(sys.argv)
    window = Events()
    window.show()
    sys.exit(app.exec())       

if __name__ == "__main__":
    main()


def eventsystem():
    today = dt.datetime.today() 
    print(today)

    #this entire section is for the user to input their event times, the E in each variable represents "Event"
    Eyear = (int(input('enter your event year: ')))
    Emonth = (int(input('enter your event month: ')))
    Eday = (int(input('enter your event day: ')))
    Ehour = (int(input('input the starting hour: ')))
    Eminute = (int(input('input the starting minute: ')))


    #checks if months goes beyond 12 and add year value by 1 for every 12 months it goes over
    if Emonth > 12:  
        extra_years = (Emonth - 1) // 12
        Eyear += extra_years
        Emonth = ((Emonth - 1) % 12) + 1

    empty, DaysInMonth = calendar.monthrange(Eyear,Emonth) 
    #checks how many days are in the month selected, this is used to determine at what value (28,30 or 31) to change Emonth to the following the month
    print(DaysInMonth) 
    #"empty" is ignored because we only want to know the amount of days in EventMonth (Emonth), not EventYear (Eyear), its only purpose is so Eyear is never defined because it is not needed

    if Eday > DaysInMonth:
        extra_days = (Eday - 1)// dt.datetime.month(Emonth)

    date2 = dt.datetime(Eyear,Emonth,Eday,Ehour,Eminute)
    print(date2)

    calc = date2 - today

    print(calc)

