# extract_player_of_match.py
# CricketIQ AI - Beginner script to read ALL IPL match JSON files
# inside a folder, pull out the Player of the Match award(s) from
# every match, and save one row per awarded player into a CSV file.

import json  # built-in module used to read and parse JSON files
import os    # built-in module used to work with file paths and folders
import csv   # built-in module used to write data out in CSV format

# This is the folder where all our match JSON files live.
# We build this path based on WHERE THIS SCRIPT FILE ITSELF is located,
# instead of relying on the folder the terminal happens to be in when
# you run the script. This way, the script works correctly no matter
# which directory you run "python extract_player_of_match.py" from.
#
# Your folder layout is:
#   CricketIQ-AI/                       <- project_root (this is where "data/" lives)
#     backend/
#       scripts/
#         Extraction/
#           extract_player_of_match.py  <- script_dir (this file)
#
# So we go up 3 levels from this script's folder: out of "Extraction",
# out of "scripts", out of "backend" - to land on "CricketIQ-AI".
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(os.path.dirname(script_dir)))
input_folder = os.path.join(project_root, "data", "raw")

# This is the folder + filename where we want to save our results.
output_folder = os.path.join(project_root, "data", "processed")
output_file = os.path.join(output_folder, "player_of_match.csv")

# If the "processed" folder doesn't exist yet, create it now.
# Without this, trying to open a file inside a missing folder would crash.
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# These are the column headers we want in our CSV file, in order.
csv_headers = ["Match ID", "Player ID", "Player Name"]

# Get a list of every file in the input folder, then keep only the
# ones that end in ".json" (in case other file types are in there too).
all_files = os.listdir(input_folder)
json_files = [f for f in all_files if f.endswith(".json")]

# This list will hold one row (as a dictionary) per Player of the
# Match entry that we successfully process.
all_potm_rows = []

# This variable keeps count of how many records we successfully export.
success_count = 0

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

    # Match ID comes from the filename, not from inside the JSON.
    match_id = os.path.splitext(filename)[0]

    # "info.player_of_match" is a LIST, e.g. ["SC Ganguly"], because a
    # match can (rarely) have a joint award shared by more than one
    # player. We use .get() with an empty list as the default, so that
    # matches with no award (or a missing field) simply give us nothing
    # to loop through below, instead of crashing the script.
    potm_list = data.get("info", {}).get("player_of_match", [])

    # If this match has no Player of the Match at all, skip it - there
    # is nothing to extract, per the "skip matches where the award is
    # unavailable" rule.
    if len(potm_list) == 0:
        continue

    # The registry maps each player's name to a stable unique ID, the
    # SAME ID every time that player appears across ANY match file.
    # We use it here so Player ID matches what's already in players.csv.
    registry_people = data.get("info", {}).get("registry", {}).get("people", {})

    # Loop through every player who received the award for this match.
    # Usually this list has just one name, but we loop through it so
    # joint awards each get their own row.
    for player_name in potm_list:

        # Look up this player's registry ID by name. If the player
        # isn't found in the registry for some reason, we fall back
        # to an empty string rather than crashing, since we'd still
        # like to keep the player's name on record.
        player_id = registry_people.get(player_name, "")

        # Build and store the row for this award.
        potm_row = {
            "Match ID": match_id,
            "Player ID": player_id,
            "Player Name": player_name,
        }
        all_potm_rows.append(potm_row)

        # Increase our success counter by 1 for each award recorded.
        success_count = success_count + 1

# Now we write all the collected rows into our output CSV file.
# newline="" is recommended when writing CSVs to avoid extra blank lines.
with open(output_file, "w", newline="") as f:

    # DictWriter lets us write dictionaries directly as CSV rows, matching
    # each dictionary's keys to the column headers we defined earlier.
    writer = csv.DictWriter(f, fieldnames=csv_headers)

    # This writes the header row (the column names) as the first line.
    writer.writeheader()

    # This writes one CSV row for every Player of the Match entry we collected.
    writer.writerows(all_potm_rows)

# Finally, print a summary of how many records were exported.
print()
print("Total records extracted:", success_count)
print("Saved to:", output_file)
