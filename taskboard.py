"""A tiny task board for practicing Git. Requires Python 3, no packages."""

import argparse
import json
from pathlib import Path


DATA_FILE = Path(__file__).with_name("tasks.json")


def load_tasks():
    """Load sample data relative to this script, regardless of cwd."""
    return json.loads(DATA_FILE.read_text())


def priority_label(priority):
    """Turn a stored priority into a display label."""
    return {1: "LOW", 2: "MEDIUM", 3: "HIGH"}[priority]


def render_heading():
    """Print the heading shared by both views."""
    print("Pocket Tasks — demo edition")
    print("============")
    print()


def selected_tasks(tasks, args):
    """Select and order tasks for the list view."""
    result = list(tasks)
    if args.open:
        result = [task for task in result if not task["done"]]
    elif args.completed:
        result = [task for task in result if task["done"]]
    return sorted(result, key=lambda task: task["title"].casefold())


def render_tasks(tasks):
    """Display task status, priority, and title in a compact list."""
    for task in tasks:
        status = "x" if task["done"] else " "
        label = priority_label(task["priority"])
        print(f"[{status}] {label:6} {task['title']}")
    if not tasks:
        print("No tasks match this view.")
    print()


def render_summary(tasks):
    """Display totals computed from the entire task board."""
    completed = sum(task["done"] for task in tasks)
    remaining = len(tasks) - completed
    print(f"Total:     {len(tasks)}")
    print(f"Completed: {completed}")
    print(f"Open:      {remaining}")
    urgent = sum(task["priority"] == 3 for task in tasks)
    print(f"High:      {urgent}")
    print("Tip: run list --open to choose your next task.")


def build_parser():
    """Create the command-line interface."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["list", "summary"], default="list", nargs="?")
    filters = parser.add_mutually_exclusive_group()
    filters.add_argument("--open", action="store_true", help="show only open tasks")
    filters.add_argument("--completed", action="store_true", help="show only completed tasks")
    return parser


def main():
    """Route the requested view to its renderer."""
    args = build_parser().parse_args()
    tasks = load_tasks()
    render_heading()
    if args.command == "list":
        render_tasks(selected_tasks(tasks, args))
    else:
        render_summary(tasks)


if __name__ == "__main__":
    main()
