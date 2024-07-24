import datetime
def user_compare(item1, item2, comparison_count):
    """Ask the user to compare two items and increase the comparison count."""
    while True:
        response = input(f"Which do you prefer? (1) {item1} or (2) {item2}: ").strip()
        if response == "1":
            comparison_count[0] += 1
            return item1
        elif response == "2":
            comparison_count[0] += 1
            return item2
        else:
            print("Invalid input. Please enter '1' or '2'.")


def merge(left, right, comparison_count):
    """Merge two lists using user comparisons and track comparison count."""
    result = []
    while left and right:
        if user_compare(left[0], right[0], comparison_count) == left[0]:
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


if __name__ == "__main__":
    filename = input("Enter the filename containing the list of items: ").strip()

    try:
        items = read_items_from_file(filename)
        if not items:
            print("The file is empty or does not contain any valid items.")
        else:
            print("Please help sort the following items by preference:")
            comparison_count = [0]
            sorted_items = merge_sort(items, comparison_count)

            print("Your sorted list is:")
            print(sorted_items)
            print(f"Number of comparisons made: {comparison_count[0]}")

            save_sorted_items_to_file(sorted_items, comparison_count)
    except FileNotFoundError:
        print(f"The file '{filename}' does not exist.")
