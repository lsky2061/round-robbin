import itertools
import json


def load_items(file_name):
    with open(file_name, 'r') as file:
        items = [line.strip() for line in file]
    return items


def update_scores(scores, head_to_head, winner, loser):
    scores[winner][0] += 1  # Increment wins for the winner
    scores[loser][1] += 1  # Increment losses for the loser

    # Update head-to-head results
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
            tied_items.sort(key=lambda x: (
                head_to_head.get((x[0], tied_items[0][0]), 0),
                -sum(head_to_head.get((x[0], y[0]), 0) for y in tied_items if x != y)
            ), reverse=True)
            ranked_items[i:j + 1] = tied_items
        i = j + 1

    return ranked_items


def save_state(file_name, scores, head_to_head, combinations, current_combination):
    # Convert tuple keys in head_to_head to strings
    head_to_head_str_keys = {f"{k[0]}|{k[1]}": v for k, v in head_to_head.items()}
    state = {
        'scores': scores,
        'head_to_head': head_to_head_str_keys,
        'combinations': combinations,
        'current_combination': current_combination
    }
    with open(file_name, 'w') as file:
        json.dump(state, file)


def load_state(file_name):
    with open(file_name, 'r') as file:
        state = json.load(file)
    # Convert string keys in head_to_head back to tuples
    head_to_head = {tuple(k.split('|')): v for k, v in state['head_to_head'].items()}
    state['head_to_head'] = head_to_head
    return state


def main():
    choice = input("Do you want to (1) start a new tournament or (2) load an existing one? Enter 1 or 2: ")
    if choice == '1':
        file_name = input("Enter the name of the file containing the list of items: ")
        items = load_items(file_name)
        scores = {item: [0, 0] for item in items}  # Initialize scores for each item
        head_to_head = {}  # Initialize head-to-head results
        combinations = list(itertools.combinations(items, 2))  # Generate all possible combinations of items
        current_combination = 0
    elif choice == '2':
        state_file = input("Enter the name of the file containing the saved state: ")
        state = load_state(state_file)
        scores = state['scores']
        head_to_head = state['head_to_head']
        combinations = state['combinations']
        current_combination = state['current_combination']
    else:
        print("Invalid choice. Exiting.")
        return

    total_combinations = len(combinations)

    print("Welcome to the item comparison program!")
    print(f"You will compare {total_combinations} pairs of items. Please choose the winner in each pair.")
    print("You can save the tournament progress at any time by entering 'save'.")

    for combination_index in range(current_combination, total_combinations):
        item1, item2 = combinations[combination_index]
        print(f"\nComparison {combination_index + 1}/{total_combinations}:")
        print(f"1. {item1}")
        print(f"2. {item2}")

        while True:
            choice = input("Enter the number of the winning item (1 or 2) or type 'save' to save and exit: ")
            if choice in ('1', '2'):
                break
            elif choice.lower() == 'save':
                save_state("saved_tournament.json", scores, head_to_head, combinations, combination_index)
                print("Progress saved. You can resume the tournament later.")
                return
            else:
                print("Invalid choice. Please enter 1, 2, or 'save'.")

        winner = item1 if choice == '1' else item2
        loser = item2 if choice == '1' else item1
        update_scores(scores, head_to_head, winner, loser)
        current_combination = combination_index + 1

    ranked_items = rank_items(scores, head_to_head)
    print("\nRankings:")
    rank = 1
    for item, (wins, losses) in ranked_items:
        print(f"{rank}. {item}: Wins - {wins}, Losses - {losses}")
        rank += 1


if __name__ == "__main__":
    main()
