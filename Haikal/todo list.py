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
import os
import pathlib
from pathlib import Path
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
from PyQt6.QtGui import QIcon, QFont

tasks = []

todolist_checker = Path.cwd()/"todolists"
if not todolist_checker.exists(): 
        os.mkdir('todolists')#check if the folder named "todolists" exist
# print('this file exists') << old code, used and being kept for trouble shooting

        
todo = Path.cwd()/"todolists"

json_file = todo/"My ToDo list.json" #PATHLIB : finds (or the intended use for this, create) a file with the name
todo_files = list(todolist_checker.glob("*.json"))#PATHLIB : views the files in the directory
empty_chker = not any(todo_files) #PATHLIB : checks if the directory has any files

if  empty_chker :
        json_file = todolist_checker / "My ToDo list.json"
        json_file.write_text(
              json.dumps({"Tasks": []}, indent=4), encoding="utf-8")
        print("File created using pathlib!") #Thank you Gemini for the help lol
else :
        print('has files')
        pass


# app = QApplication([])

class TodoList(QMainWindow):
        def __init__(self):
            print('initUI called')
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
            self.NewTask.clicked.connect(self.on_click_add)


      




            """drop down menu (previously just a button) that show the list of existing tasks"""
            # self.TaskList = QPushButton('list', self)
            # self.TaskList.setGeometry (0,0,80,40) #(x,y,width,height)
            # # self.event_button.setFont(QFont(font_family,60))
            # self.TaskList.clicked.connect(self.on_click)

            "Checkbox stuff here"
            self.Checker = QCheckBox()

            self.TaskList = QListWidget()
            todolist_path = Path.cwd()/"todolists"

            todolists_folder = Path.cwd()/"todolists"
            todolists_json = list(todolists_folder.glob("*.json"))

            list_names = [filename.stem for filename in todolists_json]

            self.TaskList.itemChanged.connect(self.on_task_checked)

            self.ListOfTasks= QComboBox()
            self.ListOfTasks.setEditable(True)
            self.ListOfTasks.setInsertPolicy(QComboBox.InsertPolicy.NoInsert)
            self.ListOfTasks.lineEdit().editingFinished.connect(self.ListRenamer)
        

            for i, name in enumerate(list_names):
                  self.ListOfTasks.addItem(name)
                  self.ListOfTasks.setItemData(i, todolists_json[i])

            self.ListOfTasks.currentIndexChanged.connect(self.ListSwitcher)

            if list_names:
                 self.ListSwitcher()
             
            
            """Where you type in the task"""
            self.TaskName = QLineEdit()
            self.TaskName.setPlaceholderText('Type in your task')
            # self.layout.addRow("Task name:", self.name_input)

            "Add a new list"
            self.NewListButton = QPushButton('New List', self)
            self.NewListButton.setGeometry(0, 0, 20, 40)
            self.NewListButton.clicked.connect(self.on_click_new_list)
        
            """Clear button here"""
            self.ClearTask = QPushButton('Mark all as complete', self)
            self.ClearTask.setGeometry (0,0,40,40)
            self.ClearTask.clicked.connect(self.on_click_clear)

            """Clears the tasks from the list"""
            self.DeleteTask = QPushButton('Delete task', self)
            self.DeleteTask.setGeometry(0,0,20,40)
            self.DeleteTask.clicked.connect(self.clearlist)


            Vlayout = QVBoxLayout()
            Glayout = QGridLayout()
            Hlayout = QHBoxLayout()
            Formlayout = QFormLayout()

            # """Glayout spacing"""
            # Glayout.setVerticalSpacing(0)


            Formlayout.addWidget(self.TaskName) 
            Formlayout.addWidget(self.NewTask)
            Formlayout.addWidget(self.TaskList)
            Formlayout.addWidget(self.DeleteTask)
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
            central_layout.addWidget(self.NewListButton)
            central_layout.addWidget(self.text)
            central_layout.addWidget(self.TaskList)
        #     central_layout.addWidget(self.DeleteTask)
            central_layout.addWidget(self.ClearTask)
            central_layout.addWidget(self.DeleteTask)
            # central_layout.addRow(Formlayout)

            central_widget.setLayout(central_layout)

        def on_click_add(self):
            print('task added!')
            self.NewTask.setText(f"{input} added to list!")
            newtask = self.TaskName.text().strip()

            if not newtask:
                   return

            index = self.ListOfTasks.currentIndex()
            file_path = self.ListOfTasks.itemData(index)

            if file_path is None:
                   return

            with open(file_path, 'r') as f:
                   todo = json.load(f)

            todo['Tasks'].append({
                   "task" : newtask,
                   "completed" : False,
            })

            with open(file_path,'w') as f:
                json.dump(todo, f, indent=4)

            self.TaskName.clear()
            self.ListSwitcher()
            # TaskAdded = input()
            # tasks.append({"task":TaskAdded, "completed":False})
            # print(f"{TaskAdded} added to the list!")
#             todolist_checker = Path.cwd()/"todolists"
#             if not todolist_checker.exists(): 
#                 os.mkdir('todolists')#check if the folder named "todolists" exist
#     # print('this file exists') << old code, used and being kept for trouble shooting
           
                
#             todo = Path.cwd()/"todolists"

#             json_file = todo/"My ToDo list.json" #PATHLIB : finds (or the intended use for this, create) a file with the name
#             todo_files = todo.iterdir() #PATHLIB : views the files in the directory
#             empty_chker = not any(todo_files) #PATHLIB : checks if the directory has any files

#         if  empty_chker :
#                 json_file = todo_files/ "My ToDo list.json"
#                 json_file.write_text(json.dumps({"Tasks:" "[]"}, indent=4), encoding="utf-8")
#                 print("File created using pathlib!") #Thank you Gemini for the help lol
#         else :
#                 print('has files')

#                 pass

        def ListSwitcher(self):
                index = self.ListOfTasks.currentIndex()
                file_path = self.ListOfTasks.itemData(index)

                self.TaskList.clear()

                with open(file_path,'r') as f:
                        todo = json.load(f)
                        for Tasks in todo["Tasks"]:
                                taskfunction = Tasks.get("task")
                                # is_completed = Tasks.get("completed", True)

                                item = self.TaskItemLister(Tasks)

                                # font = item.font()
                                # # font = QFont()
                                # font.setStrikeOut(is_completed)
                                # font.setItalic(is_completed)
                                # font.setBold(is_completed)
                                # item.setFont(font)

                                self.TaskList.addItem(item)
        

        def ListRenamer(self):
                print('listswitcher called')
                index = self.ListOfTasks.currentIndex()
                new_name = self.ListOfTasks.currentText().strip()

                if not new_name:
                        return

                OldFilePath = self.ListOfTasks.itemData(index)
                NewFilePath = OldFilePath.with_name(new_name + ".json")

                if OldFilePath == NewFilePath:
                        return

                try:
                        OldFilePath.rename(NewFilePath)
                        self.ListOfTasks.setItemData(index, NewFilePath)
                        self.ListOfTasks.setItemText(index, new_name)
                except FileExistsError:
                        print(f"A list named '{new_name}' already exists.")
                except FileNotFoundError:
                        print(f"Could not find the original file: {OldFilePath.name}")

                index = self.ListOfTasks.currentIndex()
                file_path = self.ListOfTasks.itemData(index)

                self.TaskList.blockSignals(True)   # pause itemChanged while rebuilding
                self.TaskList.clear()

                with open(file_path, 'r') as f:
                        todo = json.load(f)
                        for Tasks in todo["Tasks"]:
                                item = self.build_task_item(Tasks)
                                self.TaskList.addItem(item)

                self.TaskList.blockSignals(False) 


        def TaskItemLister(self, task_dict):
                index = self.ListOfTasks.currentIndex()
                file_path = self.ListOfTasks.itemData(index)

                
                task_text = task_dict.get("task")
                is_completed = task_dict.get("completed", False)

                item = QListWidgetItem(task_text)

                
                task_text = task_dict.get("task")
                is_completed = task_dict.get("completed", False)

                item = QListWidgetItem(task_text)
                item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
                item.setCheckState(Qt.CheckState.Checked if is_completed else Qt.CheckState.Unchecked)

                return item

    
        def on_click_clear(self):
                index = self.ListOfTasks.currentIndex()
                file_path = self.ListOfTasks.itemData(index)

                if file_path is None:
                        return

                with open(file_path, 'r') as f:
                        todo = json.load(f)

                for task in todo["Tasks"]:
                        task["completed"] = True

                with open(file_path, 'w') as f:
                        json.dump(todo, f, indent=4)

                self.ListSwitcher()
          # WORKS AS INTENDED, BUT THE WHOLE APP CRASHES, I HAVE TO FIGURE OUT HOW TO FIX IT
        #   with open('todolisttest.json','w') as file:
        #     todo = json.load(file)

        def on_task_checked(self, item):
               index = self.ListOfTasks.currentIndex()
               file_path = self.ListOfTasks.itemData(index)

               with open(file_path, 'r') as f:
                      todo = json.load(f)
               
               task_text = item.text()
               is_checked = item.checkState() == Qt.CheckState.Checked

               for task in todo["Tasks"]:
                      if task.get('task') == task_text:
                             task["completed"] = is_checked
                             break
               with open(file_path, 'w') as f:
                      json.dump(todo, f, indent=4)

        def on_click_new_list(self):
                todolists_folder = Path.cwd() / "todolists"

                base_name = "New List"
                new_file = todolists_folder / f"{base_name}.json"

                # Avoid overwriting an existing file if "New List.json" already exists
                counter = 1
                while new_file.exists():
                        new_file = todolists_folder / f"{base_name} ({counter}).json"
                        counter += 1

                new_file.write_text(
                        json.dumps({"Tasks": []}, indent=4),
                        encoding="utf-8"
                )

                # Add it to the dropdown and switch straight to it
                index = self.ListOfTasks.count()
                self.ListOfTasks.addItem(new_file.stem)
                self.ListOfTasks.setItemData(index, new_file)
                self.ListOfTasks.setCurrentIndex(index)

        def clearlist(self):
                index = self.ListOfTasks.currentIndex()
                file_path = self.ListOfTasks.itemData(index)

                if file_path is None:
                        return

                with open(file_path, 'r') as f:
                        todo = json.load(f)

                todo["Tasks"] = []

                with open(file_path, 'w') as f:
                        json.dump(todo, f, indent=4)

                self.ListSwitcher()
          
def main():
    app = QApplication(sys.argv)
    window = TodoList()
    window.setWindowTitle('To-Do List')
    window.setWindowFlags(window.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main() 