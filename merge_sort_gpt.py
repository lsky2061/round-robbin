def user_compare(item1, item2):
    """Ask the user to compare two items."""
    while True:
        response = input(f"Which do you prefer? (1) {item1} or (2) {item2}: ").strip()
        if response == "1":
            return item1
        elif response == "2":
            return item2
        else:
            print("Invalid input. Please enter '1' or '2'.")


def merge(left, right):
    """Merge two lists using user comparisons."""
    result = []
    while left and right:
        if user_compare(left[0], right[0]) == left[0]:
            result.append(left.pop(0))
        else:
            result.append(right.pop(0))
    result.extend(left if left else right)
    return result


def merge_sort(items):
    """Sort the list using merge sort with user comparisons."""
    if len(items) <= 1:
        return items

    mid = len(items) // 2
    left = merge_sort(items[:mid])
    right = merge_sort(items[mid:])

    return merge(left, right)


def read_items_from_file(filename):
    """Read a list of items from a file."""
    with open(filename, 'r') as file:
        items = [line.strip() for line in file if line.strip()]
    return items


if __name__ == "__main__":
    filename = input("Enter the filename containing the list of items: ").strip()

    try:
        items = read_items_from_file(filename)
        if not items:
            print("The file is empty or does not contain any valid items.")
        else:
            print("Please help sort the following items by preference:")
            sorted_items = merge_sort(items)

            print("Your sorted list is:")
            print(sorted_items)
    except FileNotFoundError:
        print(f"The file '{filename}' does not exist.")
