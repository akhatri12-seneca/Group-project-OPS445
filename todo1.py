#!/usr/bin/env python3

import json      # To save and load tasks as JSON
import argparse  # To handle command-line arguments
import os        # To check if file exists

TASKS_FILE = 'tasks.json'  # Name of the file where tasks are stored

# -------------------------
# Load tasks from file
# -------------------------
def load_tasks():
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, 'r') as f:
            return json.load(f)  # Read JSON list of tasks
    return []  # If file doesn’t exist, return empty list

# -------------------------
# Save tasks to file
# -------------------------
def save_tasks(tasks):
    with open(TASKS_FILE, 'w') as f:
        json.dump(tasks, f, indent=2)  # Write tasks as JSON with indentation

# -------------------------
# Add a new task
# -------------------------
def add_task(args):
    tasks = load_tasks()  # Load current tasks

    new_task = {
        'title': args.title,        # Task name
        'due': args.due,            # Due date
        'priority': args.priority,  # Priority (low/medium/high)
        'done': False               # Task starts as not done
    }

    tasks.append(new_task)       # Add new task to the list
    save_tasks(tasks)            # Save updated task list
    print("Task added.")

# -------------------------
# List all tasks
# -------------------------
def list_tasks(args):
    tasks = load_tasks()

    if not tasks:
        print("No tasks found.")
        return

    for i, task in enumerate(tasks, 1):
        status = "DONE" if task['done'] else "NOT DONE"
        print(f"{i}. {task['title']} (Due: {task['due']}, Priority: {task['priority']}) [{status}]")

# -------------------------
# Mark a task as done
# -------------------------
def mark_done(args):
    tasks = load_tasks()

    index = int(args.index) - 1  # Convert to zero-based index

    if 0 <= index < len(tasks):
        tasks[index]['done'] = True
        save_tasks(tasks)
        print("✅ Task marked as done.")
    else:
        print("Invalid task number.")

# -------------------------
# Main: Command Parser
# -------------------------
def main():
    parser = argparse.ArgumentParser(description="Simple To-Do List Manager")

    subparsers = parser.add_subparsers(help='Available commands')

    # -- add command --
    parser_add = subparsers.add_parser('add', help='Add a new task')
    parser_add.add_argument('title', help='Title of the task')
    parser_add.add_argument('--due', required=True, help='Due date (e.g., 2025-07-20)')
    parser_add.add_argument('--priority', choices=['low', 'medium', 'high'], default='low')
    parser_add.set_defaults(func=add_task)

    # -- list command --
    parser_list = subparsers.add_parser('list', help='List all tasks')
    parser_list.set_defaults(func=list_tasks)

    # -- done command --
    parser_done = subparsers.add_parser('done', help='Mark task as done')
    parser_done.add_argument('index', help='Task number to mark as done')
    parser_done.set_defaults(func=mark_done)

    # Parse and run the selected command
    args = parser.parse_args()
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()

# Run only if this script is executed directly
if __name__ == '__main__':
    main()