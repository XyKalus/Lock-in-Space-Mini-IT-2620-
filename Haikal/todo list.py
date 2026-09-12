"""
REWORK THIS ENTIRE THING IN PYQT6 

To-do list
Basic features :
- a checkbox
- saving the made lists
- ability to make multiple lists
- list of completed and uncompleted tasks
 """

"""Saving should be in JSON, should I use lists to store the tasks?"""

import shutil
import json

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
            # text = QLabel("type your event here", self) #for my understanding > self means the Window
            # # button.setFont(QFont(font_family,60))
            # text.setGeometry(0,0,90,90) #(x,y,width,height)
            # text.setStyleSheet("color: white;"
            #                     "background-color: black;") # this code is only here for testing, will either keep or change
            # text.setAlignment(Qt.AlignmentFlag.AlignCenter) # controls the alignment of the label, the | is used to label 2 css properties at once

            
            """Button that adds a new task"""
            self.NewTask = QPushButton('+', self)
            self.NewTask.setGeometry (0,0,400,200) #(x,y,width,height)
            # self.event_button.setFont(QFont(font_family,60))
            self.NewTask.clicked.connect(self.on_click)

            """Button that show the list of existing tasks"""
            self.TaskList = QPushButton('list', self)
            self.TaskList.setGeometry (0,0,400,200) #(x,y,width,height)
            # self.event_button.setFont(QFont(font_family,60))
            self.TaskList.clicked.connect(self.on_click)
            
            """Where you type in the task"""
            self.TaskName = QLineEdit()
            self.TaskName.setPlaceholderText('Type in your task')
            # self.layout.addRow("Task name:", self.name_input)

            Vlayout = QVBoxLayout()
            Glayout = QGridLayout()
            Hlayout = QHBoxLayout()

            # """Glayout spacing"""
            # Glayout.setVerticalSpacing(0)
        

            # Vlayout.addWidget(self.TaskName)
            # Vlayout.addWidget(self.NewTask)


            # Vlayout.addWidget(self.TaskList)

            # central_layout = QVBoxLayout()
            # central_layout.addLayout(Hlayout)

            # central_widget.setLayout(central_layout)
            Hlayout.setSpacing(0)
            Hlayout.setContentsMargins(0,0,0,0)

            Vlayout.setSpacing(0)
            Vlayout.setContentsMargins(0,0,0,0)

            Hlayout.addWidget(self.TaskName)
            Hlayout.addWidget(self.NewTask)

            Vlayout.addLayout(Hlayout)      # TaskName + NewTask side by side, as one row
            Vlayout.addWidget(self.TaskList)  # sits directly below that row

            central_layout = QHBoxLayout()
            central_layout.addLayout(Vlayout)

            central_widget.setLayout(central_layout)

    def on_click(self):
            print('task added!')
            self.NewTask.setText('done!')
            # TaskAdded = input()
            # tasks.append({"task":TaskAdded, "completed":False})
            # print(f"{TaskAdded} added to the list!")



# def TodoListCLI():
    # while True: 
    #     def TaskInitialise(): #The first thing that runs when you start the program, giving the user choice on what to do

    #         print("=" * shutil.get_terminal_size().columns)
    #         #figure out how to make it span from one end of the terminal to the other
    #         print("To-do list")
    #         print('1.New task')
    #         print('2.View tasks')
    #         print('3.Delete tasks')
    #         print('4.Mark all as complete')
    #         print('5.Exit')

    #     TaskInitialise()

    #     def TaskAdd(): #This function controls the adding of new tasks and tracks its completion
            # TaskAdded = input('Task name: ')
            # tasks.append({"task":TaskAdded, "completed":False})
            # print(f"{TaskAdded} added to the list!")

    #         global x
    #         x = {
    #             "name":f"{TaskAdded}",
    #             "status" : "Incomplete",
    #         }

    #         with open("tasklist.json", "w") as c:
    #             json.dump(tasklist,c)
            

    #     def ViewTask ():
    #         if len(tasks) == 0:
    #             print('you currently have no tasks')
    #         else:
    #             print('here are your existing tasks:')
    #             # print(*tasks)
    #             json.loads(x)

    #     def DeleteTask():
    #         print(*tasks)
    #         print('Please select which task to delete')
    #         DeleteInput = input('enter a number: ')
    #         tasks.pop(DeleteInput)

    #     def ClearTask():
    #         while True:
    #             clearing = input('Are you sure to mark all as complete?(y/n): ')
    #             if clearing.lower() == 'y' or clearing.lower() == 'yes':
    #                 tasks.clear
    #                 print('All tasks marked as completed!')
    #                 print(tasks)
    #                 break
    #             elif clearing.lower() == 'n' or clearing.lower() == 'no':
    #                 pass
    #                 break
    #             else:
    #                 print('invalid input!')
            

    #     StartDecide = input('Please choose from the following: ')
    #     p = StartDecide

    #     if p == '1' or p.lower() == "add":
    #         TaskAdd()
    #     elif p == '2' or p.lower() == "view":
    #         ViewTask()
    #     elif p == "3" or p.lower() == "delete":
    #         DeleteTask()
    #     elif p == "4" or p.lower() == 'complete':
    #         ClearTask()
    #     elif p == "5" or p.lower() == "exit":
    #         break
    #     else :
    #         print('invalid input!')

    #     print(*tasks)

# TodoListCLI()

# while True:
#     rerun = input('still working? (Y/N): ')
#     if rerun.lower() == 'y':
#         TodoList()
#         break
#     elif rerun.lower() == 'n':
#         print('Goodbye!')
#         break
#     else:
#         print('invalid input')
#         continue


def main():
    app = QApplication(sys.argv)
    window = TodoList()
    window.setWindowTitle('To-Do List')
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main() 