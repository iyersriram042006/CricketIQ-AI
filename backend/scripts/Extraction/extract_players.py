# extract_players.py
# CricketIQ AI - Beginner script to read ALL IPL match JSON files
# inside a folder, pull out every unique player mentioned across all
# matches, and save them into a single CSV file (one row per player).

import json  # built-in module used to read and parse JSON files
import os    # built-in module used to work with file paths and folders
import csv   # built-in module used to write data out in CSV format

# This is the folder where all our match JSON files live.
input_folder = "../data/raw/"

# This is the folder + filename where we want to save our results.
output_folder = "../data/processed/"
output_file = os.path.join(output_folder, "players.csv")

# If the "processed" folder doesn't exist yet, create it now.
# Without this, trying to open a file inside a missing folder would crash.
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# These are the column headers we want in our CSV file, in order.
csv_headers = ["Player ID", "Player Name"]

# Get a list of every file in the input folder, then keep only the
# ones that end in ".json" (in case other file types are in there too).
all_files = os.listdir(input_folder)
json_files = [f for f in all_files if f.endswith(".json")]

# This dictionary will hold every unique player we find across all
# match files. The key is the player's registry ID (a stable unique
# ID string), and the value is their name. Using a dictionary
# automatically prevents duplicate players from being added twice,
# even if the same player appears in hundreds of matches.
all_players = {}

# Loop through every JSON filename we found, one match file at a time.
for filename in json_files:

    # Build the full path to this specific file.
    file_path = os.path.join(input_folder, filename)

    # Try to open and load the file as JSON. If the file is broken or
    # not valid JSON at all, skip the whole file safely.
    try:
        with open(file_path, "r") as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError):
        print("Skipping", filename, "- could not read/parse this file.")
        continue

    # Every match file has a "registry" section inside "info" that maps
    # each player's (and official's) name to a stable unique ID. This
    # is the most reliable source of unique players, because it's the
    # SAME ID every time that player appears in ANY match file - unlike
    # relying on name spelling, which can vary slightly between files.
    try:
        registry_people = data["info"]["registry"]["people"]
    except KeyError:
        print("Skipping", filename, "- no player registry found.")
        continue

    # "registry_people" is a dictionary like:
    # { "SC Ganguly": "abcd1234...", "BB McCullum": "efgh5678..." }
    # We loop through it and add each player to our master dictionary.
    for player_name, player_id in registry_people.items():
        all_players[player_id] = player_name

# Now we build the final list of rows to write to the CSV, one row
# per unique player we collected.
final_rows = []
for player_id, player_name in all_players.items():
    final_rows.append({
        "Player ID": player_id,
        "Player Name": player_name,
    })

# Write all the player rows out to the output CSV file.
# newline="" is recommended when writing CSVs to avoid extra blank lines.
with open(output_file, "w", newline="") as f:

    # DictWriter lets us write dictionaries directly as CSV rows, matching
    # each dictionary's keys to the column headers we defined earlier.
    writer = csv.DictWriter(f, fieldnames=csv_headers)

    # This writes the header row (the column names) as the first line.
    writer.writeheader()

    # This writes one CSV row for every unique player we collected.
    writer.writerows(final_rows)

# Finally, print a summary of how many unique players were exported.
print()
print("Total unique players extracted:", len(final_rows))
print("Saved to:", output_file)
