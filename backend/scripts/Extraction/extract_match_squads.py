# extract_match_squads.py
# CricketIQ AI - Beginner script to read ALL IPL match JSON files
# inside a folder, pull out the playing XI for BOTH teams in every
# match, and save one row per player per match into a single CSV file.

import json  # built-in module used to read and parse JSON files
import os    # built-in module used to work with file paths and folders
import csv   # built-in module used to write data out in CSV format

# This is the folder where all our match JSON files live.
# We build this path based on WHERE THIS SCRIPT FILE ITSELF is located,
# instead of relying on the folder the terminal happens to be in when
# you run the script. This way, the script works correctly no matter
# which directory you run "python extract_match_squads.py" from.
#
# Your folder layout is:
#   CricketIQ-AI/                    <- project_root (this is where "data/" lives)
#     backend/
#       scripts/
#         Extraction/
#           extract_match_squads.py  <- script_dir (this file)
#
# So we go up 3 levels from this script's folder: out of "Extraction",
# out of "scripts", out of "backend" - to land on "CricketIQ-AI".
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(os.path.dirname(script_dir)))
input_folder = os.path.join(project_root, "data", "raw")

# This is the folder + filename where we want to save our results.
output_folder = os.path.join(project_root, "data", "processed")
output_file = os.path.join(output_folder, "match_squads.csv")

# If the "processed" folder doesn't exist yet, create it now.
# Without this, trying to open a file inside a missing folder would crash.
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# These are the column headers we want in our CSV file, in order.
csv_headers = ["Match ID", "Team Name", "Player ID", "Player Name"]

# Get a list of every file in the input folder, then keep only the
# ones that end in ".json" (in case other file types are in there too).
all_files = os.listdir(input_folder)
json_files = [f for f in all_files if f.endswith(".json")]

# This set will keep track of every (match_id, player_id) pair we've
# already added. We check against this before adding a new row, so
# that if the same player somehow appears twice in a squad list, we
# don't write a duplicate row for them.
seen_pairs = set()

# This list will hold one row (as a dictionary) per player-in-squad
# entry that we successfully process.
all_squad_rows = []

# This variable keeps count of how many squad rows we successfully export.
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

    # "info.players" is a dictionary shaped like:
    #   { "Kolkata Knight Riders": ["SC Ganguly", "BB McCullum", ...],
    #     "Royal Challengers Bangalore": ["R Dravid", "V Kohli", ...] }
    # This is the announced playing XI for each team in this match.
    # We use .get() with an empty dictionary as the default, in case
    # this section is missing from a particular file.
    players_by_team = data.get("info", {}).get("players", {})

    # The registry maps each player's name to a stable unique ID, the
    # SAME ID every time that player appears across ANY match file.
    # We use it here so Player ID matches what's already in players.csv.
    registry_people = data.get("info", {}).get("registry", {}).get("people", {})

    # Loop through each team and its list of players in this match.
    for team_name, player_names in players_by_team.items():

        # Loop through every player in this team's playing XI.
        for player_name in player_names:

            # Look up this player's registry ID by name. If the player
            # isn't found in the registry for some reason, we fall back
            # to an empty string rather than crashing, since we'd still
            # like to keep the player's name on record.
            player_id = registry_people.get(player_name, "")

            # Build a unique key for this (match, player) combination so
            # we can detect and skip duplicates.
            pair_key = (match_id, player_id, player_name)

            if pair_key in seen_pairs:
                # We've already added this exact player for this match -
                # skip it so we don't write a duplicate row.
                continue

            # Mark this pair as seen, then build and store the row.
            seen_pairs.add(pair_key)

            squad_row = {
                "Match ID": match_id,
                "Team Name": team_name,
                "Player ID": player_id,
                "Player Name": player_name,
            }
            all_squad_rows.append(squad_row)

            # Increase our success counter by 1 for each squad entry.
            success_count = success_count + 1

# Now we write all the collected squad rows into our output CSV file.
# newline="" is recommended when writing CSVs to avoid extra blank lines.
with open(output_file, "w", newline="") as f:

    # DictWriter lets us write dictionaries directly as CSV rows, matching
    # each dictionary's keys to the column headers we defined earlier.
    writer = csv.DictWriter(f, fieldnames=csv_headers)

    # This writes the header row (the column names) as the first line.
    writer.writeheader()

    # This writes one CSV row for every squad entry we collected.
    writer.writerows(all_squad_rows)

# Finally, print a summary of how many squad entries were exported.
print()
print("Total squads extracted:", success_count)
print("Saved to:", output_file)
