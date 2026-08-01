# extract_teams.py
# CricketIQ AI - Beginner script to read ALL IPL match JSON files
# inside a folder, pull out every unique team name mentioned across
# all matches, and save them into a single CSV file with a simple
# auto-incrementing Team ID (1, 2, 3, ...).

import json  # built-in module used to read and parse JSON files
import os    # built-in module used to work with file paths and folders
import csv   # built-in module used to write data out in CSV format

# This is the folder where all our match JSON files live.
# We build this path based on WHERE THIS SCRIPT FILE ITSELF is located,
# instead of relying on the folder the terminal happens to be in when
# you run the script. This way, the script works correctly no matter
# which directory you run "python extract_teams.py" from.
#
# os.path.abspath(__file__) = full path to this script file
# os.path.dirname(...)      = the folder containing this script
#
# Your folder layout is:
#   CricketIQ-AI/              <- project_root (this is where "data/" lives)
#     backend/
#       scripts/
#         Extraction/
#           extract_teams.py   <- script_dir (this file)
#
# So we go up 3 levels from this script's folder: out of "Extraction",
# out of "scripts", out of "backend" - to land on "CricketIQ-AI".
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(os.path.dirname(script_dir)))
input_folder = os.path.join(project_root, "data", "raw")

# This is the folder + filename where we want to save our results.
output_folder = os.path.join(project_root, "data", "processed")
output_file = os.path.join(output_folder, "teams.csv")

# If the "processed" folder doesn't exist yet, create it now.
# Without this, trying to open a file inside a missing folder would crash.
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# These are the column headers we want in our CSV file, in order.
csv_headers = ["Team ID", "Team Name"]

# Get a list of every file in the input folder, then keep only the
# ones that end in ".json" (in case other file types are in there too).
all_files = os.listdir(input_folder)
json_files = [f for f in all_files if f.endswith(".json")]

# We use a "set" here instead of a list because a set automatically
# throws away duplicates. Since the same team name will appear in
# hundreds of match files, a set is the simplest way to collect only
# the UNIQUE team names without writing extra duplicate-checking code.
unique_team_names = set()

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

    # Each match file lists the two participating teams under
    # info.teams, e.g. ["Kolkata Knight Riders", "Royal Challengers Bangalore"].
    # We use .get() with an empty list as the default, in case "teams"
    # is missing from a particular file for some reason.
    teams_in_match = data.get("info", {}).get("teams", [])

    # Add each team name from this match into our set of unique names.
    # If a team name is already in the set, .add() simply does nothing
    # extra - it won't create a duplicate.
    for team_name in teams_in_match:
        unique_team_names.add(team_name)

# Now we turn our set of unique team names into a sorted list. Sorting
# alphabetically makes the output predictable and easy to read, and
# also means Team IDs stay consistent every time we re-run the script
# on the same data (instead of changing order randomly, which sets
# don't guarantee on their own).
sorted_team_names = sorted(unique_team_names)

# Build the final list of rows to write to the CSV. We use enumerate()
# starting at 1 so the first team gets Team ID 1, the second gets 2,
# and so on - a simple auto-incrementing ID.
final_rows = []
for team_id, team_name in enumerate(sorted_team_names, start=1):
    final_rows.append({
        "Team ID": team_id,
        "Team Name": team_name,
    })

# Write all the team rows out to the output CSV file.
# newline="" is recommended when writing CSVs to avoid extra blank lines.
with open(output_file, "w", newline="") as f:

    # DictWriter lets us write dictionaries directly as CSV rows, matching
    # each dictionary's keys to the column headers we defined earlier.
    writer = csv.DictWriter(f, fieldnames=csv_headers)

    # This writes the header row (the column names) as the first line.
    writer.writeheader()

    # This writes one CSV row for every unique team we collected.
    writer.writerows(final_rows)

# Finally, print a summary of how many unique teams were exported.
print()
print("Total unique teams extracted:", len(final_rows))
print("Saved to:", output_file)
