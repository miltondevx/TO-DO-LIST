import json
import os
from datetime import datetime

# Define the filenames for storing data.....
DATA_FILE = "tasks.json"
LOG_FILE = "logs.json"

def load_tasks():
    """Loads tasks from the local JSON file."""
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, 'r') as file:
            return json.load(file)
    except (json.JSONDecodeError, IOError):
        return []

def save_tasks(tasks):
    """Saves the current list of tasks to the JSON file."""
    try:
        with open(DATA_FILE, 'w') as file:
            json.dump(tasks, file, indent=4)
    except IOError as e:
        print(f"Error saving tasks: {e}")

def log_action(action, task_title):
    """Logs an action (create, complete, delete) with a timestamp."""
    entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "action": action,
        "task": task_title
    }
    
    logs = []
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, 'r') as file:
                logs = json.load(file)
        except (json.JSONDecodeError, IOError):
            logs = []
    
    logs.append(entry)
    
    try:
        with open(LOG_FILE, 'w') as file:
            json.dump(logs, file, indent=4)
    except IOError as e:
        print(f"Error saving log: {e}")

def view_logs():
    """Displays the activity logs."""
    print("\n--- ACTIVITY LOGS ---")
    if not os.path.exists(LOG_FILE):
        print("No logs found.")
        return

    try:
        with open(LOG_FILE, 'r') as file:
            logs = json.load(file)
            if not logs:
                print("Log is empty.")
            else:
                for log in logs:
                    print(f"[{log['timestamp']}] {log['action']}: {log['task']}")
    except (json.JSONDecodeError, IOError):
        print("Error reading logs.")
    print("---------------------")

def view_tasks(tasks):
    """Displays all tasks with their status and creation date."""
    print("\n--- YOUR TASKS ---")
    if not tasks:
        print("Your list is empty.")
    else:
        for index, task in enumerate(tasks, start=1):
            status = "[x]" if task['completed'] else "[ ]"
            created = task.get('created_at', 'Unknown Time')
            print(f"{index}. {status} {task['title']} (Added: {created})")
    print("------------------")

def add_task(tasks):
    """Adds a new task with a timestamp."""
    title = input("Enter the task description: ").strip()
    if title:
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        tasks.append({"title": title, "completed": False, "created_at": created_at})
        save_tasks(tasks)
        log_action("Created", title)
        print(f"Task '{title}' added.")
    else:
        print("Task cannot be empty.")

def mark_complete(tasks):
    """Marks a specific task as done."""
    view_tasks(tasks)
    if not tasks:
        return

    try:
        task_num = int(input("Enter the number of the task to complete: "))
        if 1 <= task_num <= len(tasks):
            task = tasks[task_num - 1]
            task['completed'] = True
            save_tasks(tasks)
            log_action("Completed", task['title'])
            print("Task marked as complete.")
        else:
            print("Invalid task number.")
    except ValueError:
        print("Please enter a valid number.")

def delete_task(tasks):
    """Deletes a specific task."""
    view_tasks(tasks)
    if not tasks:
        return

    try:
        task_num = int(input("Enter the number of the task to delete: "))
        if 1 <= task_num <= len(tasks):
            removed = tasks.pop(task_num - 1)
            save_tasks(tasks)
            log_action("Deleted", removed['title'])
            print(f"Task '{removed['title']}' deleted.")
        else:
            print("Invalid task number.")
    except ValueError:
        print("Please enter a valid number.")

def main():
    """Main application loop."""
    tasks = load_tasks()
    
    while True:
        print("\n=== TO-DO LIST MENU ===")
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Mark Task as Complete")
        print("4. Delete Task")
        print("5. View Activity Logs")
        print("6. Quit")
        
        choice = input("Choose an option (1-6): ").strip()

        if choice == '1':
            add_task(tasks)
        elif choice == '2':
            view_tasks(tasks)
        elif choice == '3':
            mark_complete(tasks)
        elif choice == '4':
            delete_task(tasks)
        elif choice == '5':
            view_logs()
        elif choice == '6':
            print("Goodbye! Your tasks are saved.")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 6.")
#dude need to make an gui interface next update....
if __name__ == "__main__":
    main()