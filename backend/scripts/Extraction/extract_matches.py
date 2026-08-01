# extract_matches.py
# CricketIQ AI - Beginner script to read ALL IPL match JSON files
# inside a folder, pull out a few key fields from each, and save
# them all together into a single CSV file.

import json  # built-in module used to read and parse JSON files
import os    # built-in module used to work with file paths and folders
import csv   # built-in module used to write data out in CSV format

# This is the folder where all our match JSON files live.
input_folder = "../data/raw/"

# This is the folder + filename where we want to save our results.
output_folder = "../data/processed/"
output_file = os.path.join(output_folder, "matches.csv")

# If the "processed" folder doesn't exist yet, create it now.
# Without this, trying to open a file inside a missing folder would crash.
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# These are the column headers we want in our CSV file, in order.
csv_headers = [
    "Match ID",
    "Team 1",
    "Team 2",
    "Venue",
    "City",
    "Season",
    "Toss Winner",
    "Toss Decision",
    "Match Winner",
]

# Get a list of every file in the input folder, then keep only the
# ones that end in ".json" (in case other file types are in there too).
all_files = os.listdir(input_folder)
json_files = [f for f in all_files if f.endswith(".json")]

# This list will hold one row (as a dictionary) per match that we
# successfully process. We will write all of these to the CSV at the end.
all_match_rows = []

# This variable keeps count of how many matches we successfully export.
success_count = 0

# Loop through every JSON filename we found, one at a time.
for filename in json_files:

    # Build the full path to this specific file.
    file_path = os.path.join(input_folder, filename)

    # Open and load the JSON file into a Python dictionary called "data".
    with open(file_path, "r") as f:
        data = json.load(f)

    # We use a try/except block here so that if any field is missing or
    # the JSON is shaped differently than expected, we simply skip this
    # file instead of crashing the whole script.
    try:
        # Match ID comes from the filename, not from inside the JSON.
        match_id = os.path.splitext(filename)[0]

        # "teams" is a list of exactly two team names, e.g. ["Team A", "Team B"].
        teams = data["info"]["teams"]
        team_1 = teams[0]
        team_2 = teams[1]

        # Venue and city of the match.
        venue = data["info"]["venue"]
        city = data["info"]["city"]

        # Which season this match belongs to.
        season = data["info"]["season"]

        # Who won the toss, and what they chose to do (bat or field).
        toss_winner = data["info"]["toss"]["winner"]
        toss_decision = data["info"]["toss"]["decision"]

        # The overall match winner. Some matches (ties/no result) have no
        # winner, so we use .get() with a default value instead of a
        # direct lookup, which would raise an error if the key is missing.
        match_winner = data["info"]["outcome"].get("winner", "No Result")

        # If we reach this point, every required field was found successfully.
        # Build a dictionary for this match's row and add it to our list.
        match_row = {
            "Match ID": match_id,
            "Team 1": team_1,
            "Team 2": team_2,
            "Venue": venue,
            "City": city,
            "Season": season,
            "Toss Winner": toss_winner,
            "Toss Decision": toss_decision,
            "Match Winner": match_winner,
        }
        all_match_rows.append(match_row)

        # Increase our success counter by 1.
        success_count = success_count + 1

    except (KeyError, IndexError):
        # KeyError happens if a field like "venue" or "toss" is missing.
        # IndexError happens if "teams" doesn't have 2 entries.
        # Either way, we print a warning and skip this file gracefully.
        print("Skipping", filename, "- missing a required field.")
        continue

# Now we write all the collected match rows into our output CSV file.
# newline="" is recommended when writing CSVs to avoid extra blank lines.
with open(output_file, "w", newline="") as f:

    # DictWriter lets us write dictionaries directly as CSV rows, matching
    # each dictionary's keys to the column headers we defined earlier.
    writer = csv.DictWriter(f, fieldnames=csv_headers)

    # This writes the header row (the column names) as the first line.
    writer.writeheader()

    # This writes one CSV row for every match dictionary we collected.
    writer.writerows(all_match_rows)

# Finally, print a summary of how many matches were exported successfully.
print()
print("Total matches successfully exported:", success_count)
print("Saved to:", output_file)
