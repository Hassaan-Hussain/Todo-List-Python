import json
import os
import datetime as dt

def load_tasks():
    try:
        with open("Tasks.json", "r") as file:
            tasks = json.load(file)
            return tasks
    except Exception as e:
        print(e, '\n')
        return []

def save_task(tasks):
    with open("Tasks.json", "w") as file:
        json.dump(tasks, file, indent=3)

def show_task(tasks):
    print("*" * 50)
    if not tasks:
        print("No Tasks available!")
    for i, task in enumerate(tasks, start=1):
        print(f"Task-{i}: {task}")

def add_task(tasks):
    try:
        name = input("Enter you task: ").strip()
        while True:
            due_date = input("Enter due date (yyyy-mm-dd):  ").strip()
            try:
                dt.datetime.strptime(due_date, "%Y-%m-%d")
                break
            except ValueError:
                print("Invalid Date format. Use yyyy-mm-dd.")
        priority = input("Enter task's priority (low, medium, high):  ").lower()
        category = input("Enter task category: ").lower()
        status = input("Enter task status (Complete/Incomplete): ").lower()
        new_task = {"Name":name, "Due Date":due_date, "Priority":priority, "Category":category, "Status":status}
        tasks.append(new_task) 
        save_task(tasks)
        print("Task added successfully.")
    except Exception as e:
        print(e)

def update_task(tasks):
    if not tasks:
        print("No Tasks available!")
    show_task(tasks)
    choice = input("Update Status or Data? Type(status or data): ").lower()
    if choice == 'data':
        try:
            update = int(input("Enter task number to update: "))
            if 0 <= update <= len(tasks):
                new_name = input("Enter new name: ")
                new_due_date = input("Enter new due date: ")
                new_priority = input("Enter task's priority (low, medium, high):  ").lower()
                new_category = input("Enter task category: ")
                new_status = input("Enter task status: ")
                tasks[update-1] = {"Name":new_name, "Due Date":new_due_date, "Priority":new_priority, "Category":new_category, "Status":new_status}
                save_task(tasks)
                print("Task updated.")
            else:
                print("Invalid Input")
        except Exception as e:
            print(e)
    if choice == 'status':
        try:
            show_task(tasks)
            update = int(input("Enter task number to update: "))
            if 0 <= update <= len(tasks):
                new_status = input("Enter new status: ")
                tasks[update-1]["Status"] = new_status
                save_task(tasks)
                print("Status Updated.")
        except Exception as e:
            print(e)
    else:
        print("Invalid Input.")

def delete_task(tasks):
    if not tasks:
        print("No Tasks available!")
    show_task(tasks)
    task_number = int(input("Enter Task number to delete: "))
    del tasks[task_number-1]
    save_task(tasks)
    print("Task deleted.")

def show_by_priority(tasks):
    try:
        priority = input("Enter priority to check related tasks: ").lower()
        desired_tasks = [task for task in tasks if task['Priority'] == priority]
        if not desired_tasks:
            print(f"No Tasks found with {priority} priority.")
        else:
            print(f"Tasks with {priority} priority are:")
            for task in desired_tasks:
                print(task)
    except KeyError:
        print("Error: 'priority' key missing in one or more tasks")
    except Exception as e:
        print(e)

def show_by_status(tasks):
    try:
        status = input("Enter status to view tasks: ").lower()
        tasks_by_status = [task for task in tasks if task['Status'] == status]
        if not tasks_by_status:
            print(f"No tasks available with {status} status.")
        else:
            for task in tasks_by_status:
                print(task)
    except KeyError:
        print("Error: 'Status' key is missing in one or more tasks.")
    except Exception as e:
        print(e)

def check_reminders(tasks):
    show_task(tasks)
    try:
        name = input("Enter task name to check due date: ").lower()
        task = [task for task in tasks if task["Name"].lower() == name]
        due_date = task[0]["Due Date"]
        due_date = dt.datetime.strptime(due_date, "%Y-%m-%d").date()
        today = dt.datetime.today().date()
        if due_date == today:
            print("Time has come")
        elif due_date > today:
            days_left = (due_date - today).days
            print(f"Days remaining till due date are {days_left}")
    except Exception as e:
        print(e)

def search_task(tasks):
    try:
        search_query = input("Enter (name, due date or category) to search task: ").strip().lower()
        found_tasks = [
            task for task in tasks 
            if (search_query in task['Name'].lower() or
            search_query in task['Category'].lower() or
            search_query in task['Due Date'])
        ]
        if not found_tasks:
            print(f"No task found with {search_query}.")
        else:
            print(f"Total task(s) are {len(found_tasks)}")
            for task in found_tasks:
                print(task)
    except KeyError as e:
        print(f"Error: Invalid task field - {e}")
    except Exception as e:
        print(e)

def help_sort(tasks):
    list_to_sort = []
    try:
        sort_by = input("Sort tasks by (Name, Priority or Due date): ").strip().lower()
        if sort_by == "name":
            for task in tasks:
                list_to_sort.append(task["Name"])
            return list_to_sort
        if sort_by == "priority":
            for task in tasks:
                list_to_sort.append(task["Priority"])
            return list_to_sort
        if sort_by == "due date":
            for task in tasks:
                list_to_sort.append(task["Due Date"])
            return list_to_sort
        else: 
            print("Invalid Input.")
    except Exception as e:
        print(e)

def sort_tasks(tasks):
    try:
        sorted_tasks = []
        new_list = help_sort(tasks)
        new_list.sort()
        for item in new_list:
            for task in tasks:
                if ((task["Name"] == item) or (task["Priority"] == item) or (task["Due Date"] == item)):
                    tasks.remove(task)
                    sorted_tasks.append(task)
                    break
        print("Sorted Tasks are: ")
        for task in sorted_tasks:
            print(task)
        save_task(sorted_tasks)
    except Exception as e:
        print(e)

def main():
    while True:
        print("*" * 50,  
              "\n               To Do App"
              "\n1- Show Tasks"
              "\n2- Add Task"
              "\n3- Update Task"
              "\n4- Delete Task"
              "\n5- Show by priority"
              "\n6- Show by Status" 
              "\n7- Check Due date reminder" 
              "\n8- Search task" 
              "\n9- Sort tasks"
              "\n0- Exit the App")
        choice = input("Select Between (0-9): ")
        match choice:
            case "1":
                tasks = load_tasks()
                os.system('cls')
                show_task(tasks)
            case "2":
                tasks = load_tasks()
                os.system('cls')
                add_task(tasks)
            case "3":
                tasks = load_tasks()
                os.system('cls')
                update_task(tasks)
            case "4":
                tasks = load_tasks()
                os.system('cls')
                delete_task(tasks)
            case "5":
                tasks = load_tasks()
                os.system('cls')
                show_by_priority(tasks)
            case "6":
                tasks = load_tasks()
                os.system('cls')
                show_by_status(tasks)
            case "7":
                tasks = load_tasks()
                os.system('cls')
                check_reminders(tasks)
            case "8":
                tasks = load_tasks()
                os.system('cls')
                search_task(tasks)
            case "9":
                tasks = load_tasks()
                os.system('cls')
                sort_tasks(tasks)
            case "0":
                os.system('cls')
                print("Program exited.")
                break
            case _:
                print("Invalid Input.")

if __name__ == "__main__":
    main()
