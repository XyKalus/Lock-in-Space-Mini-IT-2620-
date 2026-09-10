"""To-do list
Basic features :
- a checkbox
- saving the made lists
- ability to make multiple lists
- list of completed and uncompleted tasks
 """

"""Saving should be in JSON, should I use lists to store the tasks?"""

"""URGENT : work on GUI"""

import shutil
import json

tasks = []
# print(help(tasks))


def TodoList():
    while True: 
        def TaskInitialise(): #The first thing that runs when you start the program, giving the user choice on what to do

            print("=" * shutil.get_terminal_size().columns)
 #figure out how to make it span from one end of the terminal to the other
            print("To-do list")
            print('1.New task')
            print('2.View tasks')
            print('3.Delete tasks')
            print('4.Mark all as complete')
            print('5.Exit')

        TaskInitialise()

        def TaskAdd(): #This function controls the adding of new tasks and tracks its completion
            TaskAdder = input('Task name: ')
            tasks.append({"task":TaskAdder, "completed":False})
            print(f"{TaskAdder} added to the list!") 
            

        def ViewTask ():
            if len(tasks) == 0:
                print('you currently have no tasks')
            else:
                for task in tasks :
                    print(task)

        def DeleteTask():
            print(*tasks)
            print('Please select which task to delete')
            DeleteInput = input('enter a number: ')
            tasks.pop(DeleteInput)

        def ClearTask():
            while True:
                clearing = input('Are you sure to mark all as complete?(y/n): ')
                if clearing.lower() == 'y' or clearing.lower() == 'yes':
                    tasks.clear
                    print('All tasks marked as completed!')
                    print(tasks)
                    break
                elif clearing.lower() == 'n' or clearing.lower() == 'no':
                    pass
                    break
                else:
                    print('invalid input!')
            

        StartDecide = input('Please choose from the following: ')
        p = StartDecide

        if p == '1' or p.lower() == "add":
            TaskAdd()
        elif p == '2' or p.lower() == "view":
            ViewTask()
        elif p == "3" or p.lower() == "delete":
            DeleteTask()
        elif p == "4" or p.lower() == 'complete':
            ClearTask()
        elif p == "5" or p.lower() == "exit":
            break
        else :
            print('invalid input!')

        # print(*tasks)

TodoList()

while True:
    rerun = input('still working? (Y/N): ')
    if rerun.lower() == 'y':
        TodoList()
        break
    elif rerun.lower() == 'n':
        print('Goodbye!')
        break
    else:
        print('invalid input')
        continue