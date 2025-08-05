#!/usr/bin/env python3
# Author ID:akhatri12
# OPS445 Group Project - Mark Task as Done Feature

import argparse
import json
import os

FILENAME = 'tasks.json'  # File to store tasks

# FUNCTION TO LOAD TASKS FROM FILE
def load_tasks():
    # Return empty list if file does not exist
    if not os.path.exists(FILENAME):
        return []
    
    # Open file and load JSON data into Python list
    with open(FILENAME, 'r') as f:
        return json.load(f)

# FUNCTION TO SAVE TASKS TO FILE
def save_tasks(tasks):
    # Open file in write mode and save tasks list as JSON
    with open(FILENAME, 'w') as f:
        json.dump(tasks, f, indent=2)

# FUNCTION TO MARK A TASK AS DONE
def mark_done(args):
    tasks = load_tasks()                  # Load current tasks from file
    index = int(args.index) - 1           # Convert 1-based to 0-based index

    # Check if index is valid
    if 0 <= index < len(tasks):
        tasks[index]['done'] = True       # Mark task as done
        save_tasks(tasks)                  # Save updated tasks to file
        print("Task marked as done.")     # Notify user
    else:
        print("Invalid task number.")     # Error message if invalid index

# FUNCTION TO LIST ALL TASKS
def list_tasks(args):
    tasks = load_tasks()                  # Load tasks from file

    # Loop through tasks and print details
    for i, task in enumerate(tasks):
        status = "Done" if task['done'] else "Pending"
        print(f"{i+1}. [{status}] {task['title']} (Due: {task['due']}, Priority: {task['priority']})")

# MAIN FUNCTION TO PARSE ARGUMENTS AND CALL FUNCTIONS

def main():
    parser = argparse.ArgumentParser(description="Simple To-Do List Manager")
    subparsers = parser.add_subparsers()

    # Placeholder add command (required for argparse structure)
    parser_add = subparsers.add_parser('add')
    parser_add.set_defaults(func=lambda args: print("Add command placeholder"))

    # Parser for 'done' command to mark task as done
    parser_done = subparsers.add_parser('done', help='Mark a task as completed')
    parser_done.add_argument('index', help='Task number from the list')
    parser_done.set_defaults(func=mark_done)

    # Parser for 'list' command to display all tasks
    parser_list = subparsers.add_parser('list', help='List all tasks')
    parser_list.set_defaults(func=list_tasks)

    args = parser.parse_args()

    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()

# RUN MAIN ONLY IF SCRIPT IS EXECUTED DIRECTLY
if __name__ == '__main__':
    main()

