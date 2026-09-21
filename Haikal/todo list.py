"""
REWORK THIS ENTIRE THING IN PYQT6 

To-do list
Basic features :
- a checkbox
- saving the made lists
- ability to make multiple lists
- list of completed and uncompleted tasks
 """

""" Videos I owe my code to 
saving JSON : https://www.youtube.com/watch?v=4rmBOxn0PdI

"""

import shutil

import sys
import json

from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QGridLayout,
    QStackedWidget,
    QVBoxLayout,
    QHBoxLayout,
    QListWidget,
    QListWidgetItem,
    QFormLayout,
    QPushButton,
    QLineEdit,
    QLabel,
    QComboBox,
    QCheckBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon

tasks = []

# app = QApplication([])

class TodoList(QMainWindow):
    def __init__(self):
            super().__init__()
            self.setWindowTitle('To-do list') # title of the window
            self.setGeometry(600,250,300,500) # (x,y,width,height)
            self.initUI() #initialise the "layout" manager

    def initUI(self): #you can't normally make a layout manager inside of MainWindow, the method is : Create a main.central widget > Create the layout manager within the widget, the main widget is then added to the window (in this case (MainWindow class)), learning sources : Bro Code (YouTube)
            central_widget = QWidget()
            self.setCentralWidget(central_widget)


            """BUS LABEL"""
            self.text = QLabel("---Tasks---", self) #for my understanding > self means the Window
            # button.setFont(QFont(font_family,60))
            # self.text.setFont()
            self.text.setGeometry(0,0,90,90) #(x,y,width,height)
            self.text.setStyleSheet("color: white;"
                                "background-color: black; font-size: 20px;") # this code is only here for testing, will either keep or change
            self.text.setAlignment(Qt.AlignmentFlag.AlignCenter) # controls the alignment of the label, the | is used to label 2 css properties at once

            
            """Button that adds a new task"""
            self.NewTask = QPushButton('click me to add a task!', self)
            self.NewTask.setGeometry (0,0,80,40) #(x,y,width,height)
            # self.event_button.setFont(QFont(font_family,60))
            self.NewTask.clicked.connect(self.on_click)

            """drop down menu (previously just a button) that show the list of existing tasks"""
            # self.TaskList = QPushButton('list', self)
            # self.TaskList.setGeometry (0,0,80,40) #(x,y,width,height)
            # # self.event_button.setFont(QFont(font_family,60))
            # self.TaskList.clicked.connect(self.on_click)
            self.ListOfTasks= QComboBox()
            
             
            
            """Where you type in the task"""
            self.TaskName = QLineEdit()
            self.TaskName.setPlaceholderText('Type in your task')
            # self.layout.addRow("Task name:", self.name_input)

            
            "Checkbox stuff here"
            self.TaskList = QListWidget()
            self.TaskList.addItem('tester')
            with open('todolisttest.json','r') as file:
                todo = json.load(file)
                for Tasks in todo["Tasks"]:
                        taskfunction = Tasks.get("task")
                        # print(taskfunction) #used for trouble-shooting 
                        self.TaskList.addItem(taskfunction)
            
            """Clear button here"""
            self.ClearTask = QPushButton('Mark all as complete', self)
            self.ClearTask.setGeometry (0,0,40,40)
            self.ClearTask.clicked.connect(self.on_click_clear)

            """Delete Task"""
            self.DeleteTask = QPushButton('Delete task', self)
            self.DeleteTask.setGeometry(0,0,40,40)


            Vlayout = QVBoxLayout()
            Glayout = QGridLayout()
            Hlayout = QHBoxLayout()
            Formlayout = QFormLayout()

            # """Glayout spacing"""
            # Glayout.setVerticalSpacing(0)
        

            Formlayout.addWidget(self.TaskName) 
            Formlayout.addWidget(self.NewTask)
            Formlayout.addWidget(self.TaskList)
            # Hlayout.addWidget(self.TaskList)


            # Vlayout.addWidget(self.TaskList)

            # central_layout = QVBoxLayout()
            # central_layout.addLayout(Hlayout)

            # central_widget.setLayout(central_layout)
            Hlayout.setSpacing(0)
            Hlayout.setContentsMargins(0,0,0,0)

            Vlayout.setSpacing(0)
            Vlayout.setContentsMargins(0,0,0,0)

            # Hlayout.addWidget(self.TaskName)
            # Hlayout.addWidget(self.NewTask)

            # Vlayout.addLayout(Hlayout)      # TaskName + NewTask side by side, as one row
            # Vlayout.addWidget(self.TaskList)  # sits directly below that row


            central_layout = QFormLayout()
            # central_layout.addLayout(Vlayout)
            central_layout.addWidget(self.TaskName)
            central_layout.addWidget(self.NewTask)
            central_layout.addWidget(self.ListOfTasks)
            central_layout.addWidget(self.text)
            central_layout.addWidget(self.TaskList)
            central_layout.addWidget(self.DeleteTask)
            central_layout.addWidget(self.ClearTask)
            # central_layout.addRow(Formlayout)

            central_widget.setLayout(central_layout)

    def on_click(self):
            print('task added!')
            self.NewTask.setText(f"{input} added to list!")
            # TaskAdded = input()
            # tasks.append({"task":TaskAdded, "completed":False})
            # print(f"{TaskAdded} added to the list!")
    
    def on_click_clear(self):
          data = {
          }
          self.TaskList.clear()
          # WORKS AS INTENDED, BUT THE WHOLE APP CRASHES, I HAVE TO FIGURE OUT HOW TO FIX IT
        #   with open('todolisttest.json','w') as file:
        #     todo = json.load(file)
           


          
def main():
    app = QApplication(sys.argv)
    window = TodoList()
    window.setWindowTitle('To-Do List')
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main() 