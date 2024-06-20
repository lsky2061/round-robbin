import itertools

def load_items(file_name):
    with open(file_name, 'r') as file:
        items = [line.strip() for line in file]
    return items

def update_scores(scores, head_to_head, winner, loser):
    scores[winner][0] += 1
    scores[loser][1] += 1
    head_to_head[(winner, loser)] = head_to_head.get((winner, loser), 0) + 1
    head_to_head[(loser, winner)] = head_to_head.get((loser, winner), 0) - 1


def rank_items(scores, head_to_head):
    def sort_key(item):
        item_name = item[0]
        wins, losses = item[1]
        total_matches = wins + losses
        win_percentage = wins / total_matches if total_matches > 0 else 0
        return (win_percentage, item_name)

    ranked_items = sorted(scores.items(), key=sort_key, reverse=True)

    # Handle tie-breaking based on head-to-head results
    i = 0
    while i < len(ranked_items) - 1:
        j = i
        # Find the range of items with the same win percentage
        while j < len(ranked_items) - 1 and sort_key(ranked_items[j]) == sort_key(ranked_items[j + 1]):
            j += 1
        if j > i:
            # Sort the tied items based on head-to-head results
            tied_items = ranked_items[i:j + 1]
            tied_items.sort(key=lambda x: head_to_head.get((x[0], tied_items[0][0]), 0), reverse=True)
            ranked_items[i:j + 1] = tied_items
        i = j + 1

    return ranked_items


def main():
    file_name = input("Enter the name of the file containing the list of items: ")
    items = load_items(file_name)
    scores = {item: [0, 0] for item in items}
    head_to_head = {}

    combinations = list(itertools.combinations(items, 2))
    total_combinations = len(combinations)
    current_combination = 0

    print("Welcome to the item comparison program!")
    print(f"You will compare {total_combinations} pairs of items. Please choose the winner in each pair.")

    for item1, item2 in combinations:
        current_combination += 1
        print(f"\nComparison {current_combination}/{total_combinations}:")
        print(f"1. {item1}")
        print(f"2. {item2}")

        while True:
            choice = input("Enter the number of the winning item (1 or 2): ")
            if choice in ('1', '2'):
                break
            else:
                print("Invalid choice. Please enter 1 or 2.")

        winner = item1 if choice == '1' else item2
        loser = item2 if choice == '1' else item1
        update_scores(scores, head_to_head, winner, loser)

    ranked_items = rank_items(scores, head_to_head)
    print("\nRankings:")
    rank = 1
    for item, (wins, losses) in ranked_items:
        total_matches = wins + losses
        win_percentage = (wins / total_matches) * 100 if total_matches > 0 else 0
        print(f"{rank}. {item}: Wins - {wins}, Losses - {losses}, Win Percentage - {win_percentage:.2f}%")
        rank += 1

    print(head_to_head)

if __name__ == "__main__":
    main()
