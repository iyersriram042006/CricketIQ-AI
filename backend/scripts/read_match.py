# read_match.py
# CricketIQ AI - Beginner script to read ALL IPL match JSON files
# inside a folder and print out each filename plus a final count.

import json  # built-in module used to read and parse JSON files
import os    # built-in module used to work with file paths and folders

# This is the folder where all our match JSON files live.
folder_path = "../data/raw/"

# os.listdir() gives us a list of every file/folder name inside "folder_path".
# We store it here so we can loop over it below.
all_files = os.listdir(folder_path)

# We only want files that end in ".json" (in case other file types are
# ever added to the folder), so we filter the list using a list comprehension.
json_files = [f for f in all_files if f.endswith(".json")]

# This variable will keep track of how many match files we have processed.
# We start at 0 and add 1 each time we successfully read a file.
match_count = 0

# Loop through every JSON filename in our filtered list, one at a time.
for filename in json_files:

    # Build the full path to this specific file by joining the folder
    # path and the filename together (works correctly on any operating system).
    file_path = os.path.join(folder_path, filename)

    # Open the file in read mode ("r") and load its contents into a
    # Python dictionary called "data". The "with" statement automatically
    # closes the file for us once we're done reading it.
    with open(file_path, "r") as f:
        data = json.load(f)

    # --- Match ID (filename) ---
    # os.path.splitext() splits the filename into name + extension, so we
    # keep just the name part (e.g. "335982" from "335982.json") as the match ID.
    match_id = os.path.splitext(filename)[0]

    # Print the filename/match ID for this file so we can see progress.
    print("Found match file:", filename, "| Match ID:", match_id)

    # Increase our running total by 1 since we just processed one match file.
    match_count = match_count + 1

# After the loop finishes, print the total number of match files found.
print()
print("Total number of matches:", match_count)
