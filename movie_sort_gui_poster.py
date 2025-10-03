import os
import requests
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import json
import datetime

TMDB_API_KEY = "1c69448f00f38a52bd1d96126f210817"
CACHE_DIR = "poster_cache"
os.makedirs(CACHE_DIR, exist_ok=True)


def fetch_poster(tmdb_id):
    """Fetch movie poster from TMDB API, using local cache if available."""
    poster_path = os.path.join(CACHE_DIR, f"{tmdb_id}.jpg")

    if os.path.exists(poster_path):
        return poster_path

    url = f"https://api.themoviedb.org/3/movie/{tmdb_id}?api_key={TMDB_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data.get("poster_path"):
            poster_url = f"https://image.tmdb.org/t/p/w500{data['poster_path']}"
            img_data = requests.get(poster_url).content
            with open(poster_path, "wb") as f:
                f.write(img_data)
            return poster_path
    return None


def user_compare(item1, item2, comparison_count, callback):
    """Display a GUI to compare two items and track comparisons."""

    def select(choice):
        comparison_count[0] += 1
        root.destroy()
        callback(choice)

    root = tk.Tk()
    root.title("What question am I actually trying to answer?")
    #Which movie is better?
    #Which movie would you rather watch?
    #Which movie would you give a higher rating to?
    #Which movie do you like more?


    poster1 = fetch_poster(item1[1])
    poster2 = fetch_poster(item2[1])

    frame = tk.Frame(root)
    frame.pack(pady=20)

    if poster1:
        img1 = ImageTk.PhotoImage(Image.open(poster1).resize((200, 300)))
        btn1 = tk.Button(frame, image=img1, command=lambda: select(item1))
        btn1.grid(row=0, column=0, padx=20)
    lbl1 = tk.Label(frame, text=item1[0])
    lbl1.grid(row=1, column=0)

    if poster2:
        img2 = ImageTk.PhotoImage(Image.open(poster2).resize((200, 300)))
        btn2 = tk.Button(frame, image=img2, command=lambda: select(item2))
        btn2.grid(row=0, column=1, padx=20)
    lbl2 = tk.Label(frame, text=item2[0])
    lbl2.grid(row=1, column=1)

    root.mainloop()


def merge(left, right, comparison_count):
    """Merge two lists using user comparisons."""
    result = []
    while left and right:
        user_compare(left[0], right[0], comparison_count,
                     lambda choice: result.append(left.pop(0)) if choice == left[0] else result.append(right.pop(0)))
    result.extend(left if left else right)
    return result


def merge_sort(items, comparison_count):
    """Sort the list using merge sort with user comparisons."""
    if len(items) <= 1:
        return items
    mid = len(items) // 2
    left = merge_sort(items[:mid], comparison_count)
    right = merge_sort(items[mid:], comparison_count)
    return merge(left, right, comparison_count)


def read_items_from_file(filename):
    """Read a list of items from a file with TMDB IDs."""
    with open(filename, 'r') as file:
        items = [line.strip().split(',') for line in file if line.strip()]
        #print(items)
        #for title, tmdb_id in items: print(title, tmdb_id)

    return [(title, tmdb_id) for title, tmdb_id in items]


def save_sorted_items(sorted_items, comparison_count):
    """Save the sorted results with timestamp."""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"sorted_movies_{timestamp}.txt"
    with open(filename, 'w') as file:
        file.write("Sorted Movies:\n")
        for title, tmdb_id in sorted_items:
            file.write(f"{title},{tmdb_id}\n")
        file.write(f"\nComparisons made: {comparison_count[0]}\n")
    print(f"Results saved to {filename}")


if __name__ == "__main__":
    filename = input("Enter the filename containing the list of movies: ").strip()
    try:
        items = read_items_from_file(filename)
        if not items:
            print("The file is empty or does not contain valid entries.")
        else:
            comparison_count = [0]
            sorted_items = merge_sort(items, comparison_count)
            print(f"Sorting complete with {comparison_count[0]} comparisons.")
            save_sorted_items(sorted_items, comparison_count)
    except FileNotFoundError:
        print(f"The file '{filename}' does not exist.")
