"""Simple Task Manager - Command-line app to manage study/homework tasks."""

import json
import os

TASKS_FILE = "tasks.json"


def load_tasks():
    """Load tasks from the JSON file. Return empty list if file missing or invalid."""
    if not os.path.exists(TASKS_FILE):
        return []

    try:
        with open(TASKS_FILE, "r", encoding="utf-8") as file:
            content = file.read().strip()
            if not content:
                return []
            return json.loads(content)
    except (json.JSONDecodeError, OSError):
        print("Warning: Could not read tasks file. Starting with empty list.")
        return []


def save_tasks(tasks):
    """Save tasks list to the JSON file."""
    try:
        with open(TASKS_FILE, "w", encoding="utf-8") as file:
            json.dump(tasks, file, indent=4)
    except OSError:
        print("Error: Could not save tasks.")


def generate_new_id(tasks):
    """Generate a unique ID."""
    if not tasks:
        return 1
    return max(task["id"] for task in tasks) + 1


def add_task(title):
    """Add a new task."""
    tasks = load_tasks()

    task = {
        "id": generate_new_id(tasks),
        "title": title,
        "done": False
    }

    tasks.append(task)
    save_tasks(tasks)
    print(f"Task added: '{title}'")


def list_tasks():
    """Display all tasks."""
    tasks = load_tasks()

    if not tasks:
        print("No tasks found. Add a task to get started!")
        return

    print("\n--- Your Tasks ---")
    for task in tasks:
        status = "?" if task["done"] else "?"
        print(f"[{status}] {task['id']}. {task['title']}")
    print("------------------\n")


def mark_done(task_id):
    """Mark a task as done."""
    tasks = load_tasks()

    for task in tasks:
        if task["id"] == task_id:
            if task["done"]:
                print("Task already marked as done.")
            else:
                task["done"] = True
                save_tasks(tasks)
                print(f"Task {task_id} marked as done.")
            return

    print("Error: Task ID not found.")


def show_menu():
    """Display menu."""
    print("\n===== Task Manager =====")
    print("1. Add task")
    print("2. View all tasks")
    print("3. Mark task as done")
    print("4. Quit")
    print("========================")


def main():
    """Main application loop."""
    print("Welcome to the Study Task Manager!")

    while True:
        show_menu()
        choice = input("Choose an option (1-4): ").strip()

        if choice == "1":
            title = input("Enter task title: ").strip()
            if title:
                add_task(title)
            else:
                print("Error: Task title cannot be empty.")

        elif choice == "2":
            list_tasks()

        elif choice == "3":
            list_tasks()
            try:
                task_id = int(input("Enter task ID: ").strip())
                mark_done(task_id)
            except ValueError:
                print("Error: Please enter a valid number.")

        elif choice == "4":
            print("Goodbye! Keep studying hard!")
            break

        else:
            print("Invalid option. Choose between 1 and 4.")


if __name__ == "__main__":
    main()
