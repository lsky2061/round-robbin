import itertools


def load_items(file_name):
    with open(file_name, 'r') as file:
        items = [line.strip() for line in file]
    return items


def update_scores(scores, winner, loser):
    scores[winner][0] += 1
    scores[loser][1] += 1


def rank_items(scores):
    ranked_items = sorted(scores.items(), key=lambda x: (x[1][0], -x[1][1]), reverse=True)
    return ranked_items


def main():
    file_name = input("Enter the name of the file containing the list of items: ")
    items = load_items(file_name)
    scores = {item: [0, 0] for item in items}

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
        update_scores(scores, winner, loser)

    ranked_items = rank_items(scores)
    print("\nRankings:")
    rank = 1
    for item, (wins, losses) in ranked_items:
        print(f"{rank}. {item}: Wins - {wins}, Losses - {losses}")
        rank += 1


if __name__ == "__main__":
    main()


