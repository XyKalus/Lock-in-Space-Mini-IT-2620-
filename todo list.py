# """To-do list
# Basic features :
# - a checkbox
# - saving the made lists
# - ability to make multiple lists
# - list of completed and uncompleted tasks
#  """

# """Saving should be in JSON, should I use lists to store the tasks?"""

# import shutil
# import json

# tasks = []


# def TodoList():
#     while True: 
#         def TaskInitialise(): #The first thing that runs when you start the program, giving the user choice on what to do

#             print("=" * shutil.get_terminal_size().columns)
#  #figure out how to make it span from one end of the terminal to the other
#             print("To-do list")
#             print('1.New task')
#             print('2.View tasks')
#             print('3.Delete tasks')
#             print('4.Mark all as complete')
#             print('5.Exit')

#         TaskInitialise()

#         def TaskAdd(): #This function controls the adding of new tasks and tracks its completion
#             TaskAdded = input('Task name: ')
#             tasks.append({"task":TaskAdded, "completed":False})
#             print(f"{TaskAdded} added to the list!")

#             global x
#             x = {
#                 "name":f"{TaskAdded}",
#                 "status" : "Incomplete",
#             }

#             with open("tasklist.json", "w") as c:
#                 json.dump(tasklist,c)
            

#         def ViewTask ():
#             if len(tasks) == 0:
#                 print('you currently have no tasks')
#             else:
#                 print('here are your existing tasks:')
#                 # print(*tasks)
#                 json.loads(x)

#         def DeleteTask():
#             print(*tasks)
#             print('Please select which task to delete')
#             DeleteInput = input('enter a number: ')
#             tasks.pop(DeleteInput)

#         def ClearTask():
#             while True:
#                 clearing = input('Are you sure to mark all as complete?(y/n): ')
#                 if clearing.lower() == 'y' or clearing.lower() == 'yes':
#                     tasks.clear
#                     print('All tasks marked as completed!')
#                     print(tasks)
#                     break
#                 elif clearing.lower() == 'n' or clearing.lower() == 'no':
#                     pass
#                     break
#                 else:
#                     print('invalid input!')
            

#         StartDecide = input('Please choose from the following: ')
#         p = StartDecide

#         if p == '1' or p.lower() == "add":
#             TaskAdd()
#         elif p == '2' or p.lower() == "view":
#             ViewTask()
#         elif p == "3" or p.lower() == "delete":
#             DeleteTask()
#         elif p == "4" or p.lower() == 'complete':
#             ClearTask()
#         elif p == "5" or p.lower() == "exit":
#             break
#         else :
#             print('invalid input!')

#         print(*tasks)

# TodoList()

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

"""
Simple CLI To-Do List Application
----------------------------------
Data is stored using Python dictionaries and lists, then saved/loaded as JSON.

Data structure (what actually lives in todo_data.json):

{
    "My To-do list": [
        {"task": "Buy groceries", "completed": False},
        {"task": "Walk the dog", "completed": True}
    ],
    "Work": [
        {"task": "Finish report", "completed": False}
    ]
}

- The outer dictionary maps a LIST NAME (string) -> a LIST of tasks.
- Each task is itself a dictionary with a "task" description and a
  "completed" boolean flag.
"""

import json
import os

DATA_FILE = "todo_data.json"
DEFAULT_LIST_NAME = "My To-do list"


# ---------------------------------------------------------------------------
# Loading and saving data
# ---------------------------------------------------------------------------

def load_data():
    """Load all to-do lists from the JSON file.

    Returns a dictionary of {list_name: [task_dict, ...]}.
    If the file doesn't exist yet, creates a default empty list.
    """
    if not os.path.exists(DATA_FILE):
        return {DEFAULT_LIST_NAME: []}

    with open(DATA_FILE, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            # File exists but is empty/corrupted - start fresh
            data = {DEFAULT_LIST_NAME: []}

    if not data:
        data = {DEFAULT_LIST_NAME: []}

    return data


def save_data(data):
    """Save the entire dictionary of to-do lists back to the JSON file."""
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)


# ---------------------------------------------------------------------------
# Core functions
# ---------------------------------------------------------------------------

def add_task(data, current_list):
    """1. Add/create a new task in the current list."""
    task_description = input("Enter the new task: ").strip()

    if not task_description:
        print("Task cannot be empty. Nothing was added.\n")
        return

    # Build a task dictionary and pass it into the list for the current list
    new_task = {
        "task": task_description,
        "completed": False
    }
    data[current_list].append(new_task)

    save_data(data)
    print(f'Added "{task_description}" to "{current_list}".\n')


def view_tasks(data, current_list):
    """2. View tasks, with the option to switch to a different list.

    Returns the (possibly new) current_list name, since the user may
    switch lists from here.
    """
    print("\nAvailable to-do lists:")
    for name in data.keys():
        marker = " (current)" if name == current_list else ""
        print(f"  - {name}{marker}")

    chosen = input(
        f'\nWhich list do you want to view? (Press Enter to stay on "{current_list}"): '
    ).strip()

    if chosen:
        current_list = chosen
        if current_list not in data:
            # Creates a brand new empty list on the fly
            data[current_list] = []
            save_data(data)
            print(f'Created new list "{current_list}".')

    tasks = data[current_list]

    print(f'\n--- {current_list} ---')
    if not tasks:
        print("(No tasks yet)")
    else:
        for index, task in enumerate(tasks, start=1):
            status = "[X]" if task["completed"] else "[ ]"
            print(f"{index}. {status} {task['task']}")
    print()

    return current_list


def delete_task(data, current_list):
    """3. Delete a task from the current list."""
    tasks = data[current_list]

    if not tasks:
        print(f'"{current_list}" has no tasks to delete.\n')
        return

    print(f'\n--- {current_list} ---')
    for index, task in enumerate(tasks, start=1):
        status = "[X]" if task["completed"] else "[ ]"
        print(f"{index}. {status} {task['task']}")

    choice = input("\nEnter the number of the task to delete: ").strip()

    if not choice.isdigit():
        print("Invalid input. Nothing was deleted.\n")
        return

    choice = int(choice)
    if 1 <= choice <= len(tasks):
        removed = tasks.pop(choice - 1)  # remove from the list by index
        save_data(data)
        print(f'Deleted "{removed["task"]}".\n')
    else:
        print("That task number doesn't exist. Nothing was deleted.\n")


def mark_all_complete(data, current_list):
    """4. Mark every task in the current list as complete."""
    tasks = data[current_list]

    if not tasks:
        print(f'"{current_list}" has no tasks to mark.\n')
        return

    for task in tasks:
        task["completed"] = True

    save_data(data)
    print(f'All tasks in "{current_list}" marked as complete.\n')


def exit_app():
    """5. Exit the application."""
    print("Goodbye!")


# ---------------------------------------------------------------------------
# Main program loop
# ---------------------------------------------------------------------------

def print_menu(current_list):
    print(f'=== To-Do List App (current list: "{current_list}") ===')
    print("1. Add task")
    print("2. View tasks / switch list")
    print("3. Delete task")
    print("4. Mark all tasks as complete")
    print("5. Exit")


def main():
    data = load_data()
    current_list = DEFAULT_LIST_NAME

    # Make sure the default list exists in the data dictionary
    if current_list not in data:
        data[current_list] = []
        save_data(data)

    while True:
        print_menu(current_list)
        choice = input("Choose an option (1-5): ").strip()

        if choice == "1":
            add_task(data, current_list)
        elif choice == "2":
            current_list = view_tasks(data, current_list)
        elif choice == "3":
            delete_task(data, current_list)
        elif choice == "4":
            mark_all_complete(data, current_list)
        elif choice == "5":
            exit_app()
            break
        else:
            print("Invalid choice, please enter a number from 1 to 5.\n")


if __name__ == "__main__":
    main()