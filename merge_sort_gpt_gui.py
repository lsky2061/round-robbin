import datetime
import json
import tkinter as tk
import os

def user_compare_gui(item1, item2, comparison_count):
    """Ask the user to compare two items via GUI and increase the comparison count."""

    def on_select(choice):
        nonlocal selected
        selected = choice
        root.quit()

    selected = None
    root = tk.Tk()
    root.title("Item Comparison")

    tk.Label(root, text=f"Which do you prefer?", font=('Helvetica', 14)).pack(pady=10)
    tk.Button(root, text=item1, command=lambda: on_select(item1)).pack(pady=5)
    tk.Button(root, text=item2, command=lambda: on_select(item2)).pack(pady=5)

    root.mainloop()
    comparison_count[0] += 1
    root.destroy()
    return selected


def merge(left, right, comparison_count):
    """Merge two lists using user comparisons and track comparison count."""
    result = []
    while left and right:
        if user_compare_gui(left[0], right[0], comparison_count) == left[0]:
            result.append(left.pop(0))
        else:
            result.append(right.pop(0))
    result.extend(left if left else right)
    return result


def merge_sort(items, comparison_count):
    """Sort the list using merge sort with user comparisons and track comparison count."""
    if len(items) <= 1:
        return items

    mid = len(items) // 2
    left = merge_sort(items[:mid], comparison_count)
    right = merge_sort(items[mid:], comparison_count)

    return merge(left, right, comparison_count)


def read_items_from_file(filename):
    """Read a list of items from a file."""
    with open(filename, 'r') as file:
        items = [line.strip() for line in file if line.strip()]
    return items


def save_sorted_items_to_file(sorted_items, comparison_count):
    """Save the sorted items and comparison count to a file with a timestamped filename."""
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y%m%d_%H%M%S")
    filename = f"sorted_items_{timestamp}.txt"

    with open(filename, 'w') as file:
        file.write("Sorted Items:\n")
        for item in sorted_items:
            file.write(f"{item}\n")
        file.write(f"\nNumber of comparisons made: {comparison_count[0]}\n")

    print(f"Results saved to {filename}")


def save_progress(items, comparison_count, filename):
    """Save the current progress to a JSON file."""
    progress = {
        'items': items,
        'comparison_count': comparison_count[0]
    }
    with open(filename, 'w') as file:
        json.dump(progress, file)
    print(f"Progress saved to {filename}")


def load_progress(filename):
    """Load the saved progress from a JSON file."""
    with open(filename, 'r') as file:
        progress = json.load(file)
    return progress['items'], [progress['comparison_count']]


if __name__ == "__main__":
    import os

    action = input("Do you want to (L)oad progress or (S)tart a new session? (L/S): ").strip().upper()

    if action == 'L':
        progress_file = input("Enter the filename to load progress from: ").strip()
        if os.path.isfile(progress_file):
            items, comparison_count = load_progress(progress_file)
            print("Progress loaded.")
        else:
            print(f"The file '{progress_file}' does not exist.")
            items = None
    else:
        filename = input("Enter the filename containing the list of items: ").strip()
        try:
            items = read_items_from_file(filename)
            if not items:
                print("The file is empty or does not contain any valid items.")
                items = None
        except FileNotFoundError:
            print(f"The file '{filename}' does not exist.")
            items = None

        comparison_count = [0]

    if items is not None:
        print("Please help sort the following items by preference:")
        sorted_items = merge_sort(items, comparison_count)

        print("Your sorted list is:")
        print(sorted_items)
        print(f"Number of comparisons made: {comparison_count[0]}")

        save_sorted_items_to_file(sorted_items, comparison_count)
        save_progress(items, comparison_count, 'progress.json')
