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

        file_path = Path.cwd()/"events"/"My events.json"

        with open(file_path, 'r') as f:
                todo = json.load(f)

        todo['test'].append({
                "task" : todo,
                "completed" : False,
        })

        with open(file_path,'w') as f:
                json.dump(todo, f, indent=4)

            
    

   
            
        

def main():
    app = QApplication(sys.argv)
    window = Events()
    window.show()
    sys.exit(app.exec())       

if __name__ == "__main__":
    main()
