# extract_powerplays.py
# CricketIQ AI - Beginner script to read ALL IPL match JSON files
# inside a folder, pull out the powerplay windows for every innings,
# and save one row per powerplay into a single CSV file.

import json  # built-in module used to read and parse JSON files
import os    # built-in module used to work with file paths and folders
import csv   # built-in module used to write data out in CSV format

# This is the folder where all our match JSON files live.
# We build this path based on WHERE THIS SCRIPT FILE ITSELF is located,
# instead of relying on the folder the terminal happens to be in when
# you run the script. This way, the script works correctly no matter
# which directory you run "python extract_powerplays.py" from.
#
# Your folder layout is:
#   CricketIQ-AI/                 <- project_root (this is where "data/" lives)
#     backend/
#       scripts/
#         Extraction/
#           extract_powerplays.py <- script_dir (this file)
#
# So we go up 3 levels from this script's folder: out of "Extraction",
# out of "scripts", out of "backend" - to land on "CricketIQ-AI".
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(os.path.dirname(script_dir)))
input_folder = os.path.join(project_root, "data", "raw")

# This is the folder + filename where we want to save our results.
output_folder = os.path.join(project_root, "data", "processed")
output_file = os.path.join(output_folder, "powerplays.csv")

# If the "processed" folder doesn't exist yet, create it now.
# Without this, trying to open a file inside a missing folder would crash.
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# These are the column headers we want in our CSV file, in order.
csv_headers = ["Match ID", "Innings Number", "From Over", "To Over", "Powerplay Type"]

# Get a list of every file in the input folder, then keep only the
# ones that end in ".json" (in case other file types are in there too).
all_files = os.listdir(input_folder)
json_files = [f for f in all_files if f.endswith(".json")]

# This list will hold one row (as a dictionary) per powerplay window
# that we successfully process.
all_powerplay_rows = []

# This variable keeps count of how many powerplays we successfully export.
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

    # Get the list of innings for this match. If "innings" is missing
    # entirely, treat it as an empty list so the loop below just does
    # nothing for this file.
    innings_list = data.get("innings", [])

    # Loop through each innings in this match. enumerate() gives us both
    # the position (starting at 0) and the innings data itself, so we
    # add 1 to get a human-friendly innings number (1, 2, ...).
    for innings_index, innings in enumerate(innings_list):
        innings_number = innings_index + 1

        # "powerplays" is a LIST of windows, e.g.
        #   [{"from": 0.1, "to": 5.6, "type": "mandatory"}]
        # We use .get() with an empty list as the default, so that an
        # innings with no powerplay data simply gives us nothing to
        # loop through below, per the "skip innings without powerplay
        # data" rule.
        powerplays_list = innings.get("powerplays", [])

        # If this innings has no powerplay information at all, skip it -
        # there is nothing to extract.
        if len(powerplays_list) == 0:
            continue

        # Loop through every powerplay window in this innings. Most
        # innings only have one (the mandatory powerplay), but some
        # matches include extra discretionary powerplays too.
        for powerplay in powerplays_list:

            # We use try/except here so that if any required field
            # (like "from", "to", or "type") is missing, we skip just
            # this one powerplay entry instead of crashing the script.
            try:
                from_over = powerplay["from"]
                to_over = powerplay["to"]
                powerplay_type = powerplay["type"]

                # Build and store the row for this powerplay window.
                powerplay_row = {
                    "Match ID": match_id,
                    "Innings Number": innings_number,
                    "From Over": from_over,
                    "To Over": to_over,
                    "Powerplay Type": powerplay_type,
                }
                all_powerplay_rows.append(powerplay_row)

                # Increase our success counter by 1 for each powerplay.
                success_count = success_count + 1

            except KeyError:
                # A required field was missing on this powerplay entry -
                # skip it safely and keep going.
                continue

# Now we write all the collected powerplay rows into our output CSV file.
# newline="" is recommended when writing CSVs to avoid extra blank lines.
with open(output_file, "w", newline="") as f:

    # DictWriter lets us write dictionaries directly as CSV rows, matching
    # each dictionary's keys to the column headers we defined earlier.
    writer = csv.DictWriter(f, fieldnames=csv_headers)

    # This writes the header row (the column names) as the first line.
    writer.writeheader()

    # This writes one CSV row for every powerplay window we collected.
    writer.writerows(all_powerplay_rows)

# Finally, print a summary of how many powerplays were exported.
print()
print("Total powerplays extracted:", success_count)
print("Saved to:", output_file)
