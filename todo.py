import json
from datetime import datetime
import os

from colorama import Fore, Style, init
init(autoreset=True)

TASKS_FILE = "tasks.json"

def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, "r") as f:
        return json.load(f)

def save_tasks(tasks):
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=4)

def add_task(title, due_date=None, priority="medium"):
    tasks = load_tasks()
    tasks.append({
        "title": title,
        "completed": False,
        "due_date": due_date if due_date else "",
        "priority": priority
    })
    save_tasks(tasks)
    print("Task added!")

def list_tasks():
    tasks = load_tasks()
    if not tasks:
        print("No tasks found.")
        return

    completed = sum(task["completed"] for task in tasks)
    print(f"\nTotal: {len(tasks)} | Completed: {completed} | Remaining: {len(tasks) - completed}")
    print("-" * 50)

    # Priority colors
    priority_colors = {
        "high": Fore.RED,
        "medium": Fore.YELLOW,
        "low": Fore.GREEN
    }

    for i, task in enumerate(tasks):
        status = f"{Fore.GREEN}✅" if task["completed"] else f"{Fore.RED}❌"
        due = f"(Due: {task['due_date']})" if task["due_date"] else ""
        priority = task.get("priority", "medium").lower()
        color = priority_colors.get(priority, Fore.WHITE)
        priority_display = f"{color}[{priority.capitalize()}]{Style.RESET_ALL}"

        print(f"{i+1}. {status} {priority_display} {task['title']} {due}")
    print()

def complete_task(index):
    tasks = load_tasks()
    if 0 <= index < len(tasks):
        tasks[index]["completed"] = True
        save_tasks(tasks)
        print("Task marked as completed!")
    else:
        print("Invalid task index.")

def delete_task(index):
    tasks = load_tasks()
    if 0 <= index < len(tasks):
        deleted = tasks.pop(index)
        save_tasks(tasks)
        print(f"Deleted task: {deleted['title']}")
    else:
        print("Invalid task index.")

# Simple CLI
if __name__ == "__main__":
    while True:
        print("\n1. Add Task\n2. List Tasks\n3. Complete Task\n4. Delete Task\n5. Exit")
        choice = input("Choose: ")

        if choice == "1":
            title = input("Task title: ")
            due_date = input("Due date (YYYY-MM-DD, optional): ")
            due_date = due_date if due_date.strip() else None

            priority = input("Priority (low/medium/high): ").lower()
            if priority not in ["low", "medium", "high"]:
                priority = "medium"

            add_task(title, due_date, priority)

        elif choice == "2":
            list_tasks()

        elif choice == "3":
            try:
                idx = int(input("Task number to complete: ")) - 1
                complete_task(idx)
            except ValueError:
                print("Please enter a valid number.")

        elif choice == "4":
            try:
                idx = int(input("Task number to delete: ")) - 1
                delete_task(idx)
            except ValueError:
                print("Please enter a valid number.")

        elif choice == "5":
            break

        else:
            print("Invalid option.")