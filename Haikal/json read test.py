# import json

# with open('todolisttest.json','r') as file:
#     todo = json.load(file)
#     for Tasks in todo["Tasks"]:
#         print(Tasks.get("task"))

import os
# CurrentDir = os.getcwd()
# print(f"your current directory is : {CurrentDir}")

# folder_creator = os.listdir()
# print(folder_creator)

# filename = 'todolists'
# if os.path.exists(filename):
#     print('file exists')
# else :
#     print('this file does not exist')
#     os.mkdir('todolists')

import pathlib
from pathlib import Path
import json

amogus = Path.cwd()
print(f"The directory is : {amogus}")


todolist_checker = Path.cwd()/"todolists"

if (todolist_checker.exists()):
    # print('this file exists') << old code, used and being kept for trouble shooting
    pass
else : 
    os.mkdir('todolists')

todo = Path.cwd()/"todolists"
# print(todo.cwd())
json_file = todo/"My ToDo list.json"

todo_files = todo.iterdir()

empty_chker = not any(todo_files)


if empty_chker :
    json_file.write_text(json.dumps([]), encoding="utf-8")
    print("File created using pathlib!") #Thank you Gemini for the help lol
else :
    print('has files')
    pass

