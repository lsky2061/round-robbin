import os
import requests
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import json
import datetime
import unicodedata
import re

TMDB_API_KEY = "1c69448f00f38a52bd1d96126f210817"
CACHE_DIR = "poster_cache"
os.makedirs(CACHE_DIR, exist_ok=True)

def slugify(value, allow_unicode=False):
    """
    Taken from https://github.com/django/django/blob/master/django/utils/text.py
    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value.lower())
    return re.sub(r'[-\s]+', '-', value).strip('-_')

def get_response(tmdb_id):
    url = f"https://api.themoviedb.org/3/movie/{tmdb_id}?api_key={TMDB_API_KEY}"
    response = requests.get(url)
    data = response.json()
    print(data)
    print(data.get("poster_path"))
    print(data.get("title"))
    return response.status_code

def fetch_poster(tmdb_id):
    """Fetch movie poster from TMDB API, using local cache if available."""
    url = f"https://api.themoviedb.org/3/movie/{tmdb_id}?api_key={TMDB_API_KEY}"
    response = requests.get(url)
    data = response.json()
    poster_path = ''
    title_safe = ''
    if response.status_code == 200:
        print("TMDB listing found for ",tmdb_id)
        if data.get("title"):
            title_safe = slugify(data['title'])
            poster_file_name = f"{title_safe}_{tmdb_id}.jpg"
            poster_path = os.path.join(CACHE_DIR,poster_file_name )
            print(f"Title of {tmdb_id} is {data['title']}")

        if os.path.exists(poster_path):
            print("We already have that poster!")
            return poster_path

        if data.get("poster_path"):
            poster_url = f"https://image.tmdb.org/t/p/w500{data['poster_path']}"
            img_data = requests.get(poster_url).content
            with open(poster_path, "wb") as f:
                f.write(img_data)
            print(f"poster for {data['title']} saved to {poster_path}")
            return poster_path
    return None


def read_items_from_file(filename):
    """Read a list of items from a file with TMDB IDs."""
    with open(filename, 'r') as file:
        items = [line.strip().split(',') for line in file if line.strip()]
        print(items)
        for title, tmdb_id in items: print(title, tmdb_id)

    return [(title, tmdb_id) for title, tmdb_id in items]

if __name__ == "__main__":
    filename = input("Enter the filename containing the list of movies: ").strip()
    try:
        items = read_items_from_file(filename)
        if not items:
            print("The file is empty or does not contain valid entries.")
        else:
            #print(items)
            for item in items:
                fetch_poster(item[1])
    except FileNotFoundError:
        print(f"The file '{filename}' does not exist.")