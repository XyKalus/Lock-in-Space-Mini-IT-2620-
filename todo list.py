"""To-do list
Basic features :
- a checkbox
- saving the made lists
- ability to make multiple lists
- list of completed and uncompleted tasks
 """

"""Saving should be in JSON, should I use lists to store the tasks?"""

import json

tasks = []

def TodoList():
    while True: 
        def TaskInitialise(): #The first thing that runs when you start the program, giving the user choice on what to do
            print("=") #figure out how to make it span from one end of the terminal to the other
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
            print(*tasks)

        StartDecide = input('Please choose from the following: ')
        pop = StartDecide

        if pop == '1' or pop.lower() == "add":
            TaskAdd()
        elif pop == '2' or pop.lower() == "view":
            ViewTask()
        elif pop == "5" or pop.lower() == "exit":
            break
        else :
            print('invalid input!')

        print(*tasks)

TodoList()

while True:
    rerun = input('still working? (Y/N)')
    if rerun == 'y':
        TodoList()
        break
    elif rerun == 'n':
        print('Goodbye!')
        break
    else:
        print('invalid input')
        continue