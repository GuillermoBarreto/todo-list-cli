import json
from pathlib import Path

TASKS_FILE = Path(__file__).with_name("tasks.json")

def load_tasks():
    if TASKS_FILE.exists():
        try:
            with TASKS_FILE.open("r", encoding="utf-8") as file:
                return json.load(file)
        except json.JSONDecodeError:
            print("Warning: tasks.json is corrupted. Starting with an empty task list.")
            return []
    return []

def save_tasks(tasks):
    with TASKS_FILE.open("w", encoding="utf-8") as file:
        json.dump(tasks, file, indent=4)

def show_tasks(tasks):
    if not tasks:
        print("No tasks yet!")
        return
    for i, task in enumerate(tasks):
        status = "x" if task["done"] else " "
        print(f"{i + 1}. [{status}] {task['title']}")

def add_task(tasks):
    title = input("Enter task: ").strip()
    if not title:
        print("Task cannot be empty.")
        return
    tasks.append({"title": title, "done": False})
    save_tasks(tasks)
    print("Task added!")

def choose_task(tasks, prompt):
    show_tasks(tasks)
    if not tasks:
        return None
    try:
        index = int(input(prompt)) - 1
    except ValueError:
        print("Please enter a valid task number.")
        return None
    if not 0 <= index < len(tasks):
        print("Task number is out of range.")
        return None
    return index


def complete_task(tasks):
    index = choose_task(tasks, "Enter task number to complete: ")
    if index is None:
        return
    if tasks[index]["done"]:
        print("Task is already complete.")
        return
    tasks[index]["done"] = True
    save_tasks(tasks)
    print("Task marked as done!")

def delete_task(tasks):
    index = choose_task(tasks, "Enter task number to delete: ")
    if index is None:
        return
    removed = tasks.pop(index)
    save_tasks(tasks)
    print(f"Deleted: {removed['title']}")

def main():
    tasks = load_tasks()
    while True:
        print("\n1. View Tasks\n2. Add Task\n3. Complete Task\n4. Delete Task\n5. Exit")
        try:
            choice = input("Choose: ").strip()
        except EOFError:
            # Ctrl+D or ended piped input: exit cleanly instead of a traceback.
            print()
            break
        if choice == "1":
            show_tasks(tasks)
        elif choice == "2":
            add_task(tasks)
        elif choice == "3":
            complete_task(tasks)
        elif choice == "4":
            delete_task(tasks)
        elif choice == "5":
            break
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()
