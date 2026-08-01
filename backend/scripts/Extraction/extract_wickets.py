# extract_wickets.py
# CricketIQ AI - Beginner script to read ALL IPL match JSON files
# inside a folder, pull out ONE row for every wicket that fell,
# and save them all into a single CSV file.

import json  # built-in module used to read and parse JSON files
import os    # built-in module used to work with file paths and folders
import csv   # built-in module used to write data out in CSV format

# This is the folder where all our match JSON files live.
input_folder = "../data/raw/"

# This is the folder + filename where we want to save our results.
output_folder = "../data/processed/"
output_file = os.path.join(output_folder, "wickets.csv")

# If the "processed" folder doesn't exist yet, create it now.
# Without this, trying to open a file inside a missing folder would crash.
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# These are the column headers we want in our CSV file, in order.
csv_headers = [
    "Match ID",
    "Innings Number",
    "Batting Team",
    "Over",
    "Ball Number",
    "Batter Out",
    "Bowler",
    "Fielder",
    "Kind of Wicket",
]

# Get a list of every file in the input folder, then keep only the
# ones that end in ".json" (in case other file types are in there too).
all_files = os.listdir(input_folder)
json_files = [f for f in all_files if f.endswith(".json")]

# This list will hold one row (as a dictionary) per wicket that we
# successfully process. We will write all of these to the CSV at the end.
all_wicket_rows = []

# This variable keeps count of how many wickets we successfully export.
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
    # entirely, treat it as an empty list so the loop below just does nothing.
    innings_list = data.get("innings", [])

    # Loop through each innings in this match. enumerate() gives us both
    # the position (starting at 0) and the innings data itself, so we
    # add 1 to get a human-friendly innings number (1, 2, ...).
    for innings_index, innings in enumerate(innings_list):
        innings_number = innings_index + 1

        # Which team is batting in this innings.
        batting_team = innings.get("team", "")

        # Get the list of overs bowled in this innings.
        overs_list = innings.get("overs", [])

        # Loop through every over in this innings.
        for over_data in overs_list:

            # The over number, e.g. 0, 1, 2, ...
            over_number = over_data.get("over", "")

            # Get the list of deliveries (balls) bowled in this over.
            deliveries_list = over_data.get("deliveries", [])

            # Loop through every single delivery (ball) in this over.
            for delivery in deliveries_list:

                # Not every ball has a wicket. The "wickets" key only
                # exists on the delivery when someone got out on that
                # ball, so if it's missing we skip straight to the next
                # delivery - nothing to extract here.
                if "wickets" not in delivery:
                    continue

                # We use try/except here so that if any required field
                # (like "bowler" or "actual_delivery") is missing or
                # shaped unexpectedly, we skip just this delivery's
                # wickets instead of crashing the entire script.
                try:
                    bowler = delivery["bowler"]

                    # "actual_delivery" looks like "0.1", "0.2", etc.
                    # The part after the dot is the ball number within the over.
                    actual_delivery = delivery["actual_delivery"]
                    ball_number = actual_delivery.split(".")[1]

                    # "wickets" is a LIST because, rarely, more than one
                    # wicket can happen on the same ball (e.g. a batter is
                    # out AND the non-striker is run out backing up). We
                    # loop through every wicket entry so we don't miss any.
                    for wicket in delivery["wickets"]:

                        # Who got out, and how (caught, bowled, run out, etc).
                        batter_out = wicket["player_out"]
                        kind_of_wicket = wicket["kind"]

                        # "fielders" is only present for dismissals that
                        # involve a fielder (caught, run out, stumped).
                        # Bowled/LBW/hit wicket/retired hurt/obstructing
                        # the field usually have no fielders at all, so we
                        # use .get() with an empty list as the default.
                        fielders_list = wicket.get("fielders", [])

                        # A dismissal can (rarely) involve more than one
                        # fielder, e.g. a relay throw for a run out. We
                        # join all their names together with a comma so
                        # we don't lose any information, or leave this
                        # blank if there were no fielders at all.
                        fielder_names = [
                            fielder.get("name", "") for fielder in fielders_list
                        ]
                        fielder = ", ".join(fielder_names)

                        # Build a dictionary for this wicket's row.
                        wicket_row = {
                            "Match ID": match_id,
                            "Innings Number": innings_number,
                            "Batting Team": batting_team,
                            "Over": over_number,
                            "Ball Number": ball_number,
                            "Batter Out": batter_out,
                            "Bowler": bowler,
                            "Fielder": fielder,
                            "Kind of Wicket": kind_of_wicket,
                        }
                        all_wicket_rows.append(wicket_row)

                        # Increase our success counter by 1 for each wicket.
                        success_count = success_count + 1

                except (KeyError, IndexError):
                    # KeyError happens if a field like "player_out" or
                    # "kind" is missing. IndexError happens if
                    # "actual_delivery" has no dot in it.
                    # Either way, we just skip this delivery's wickets
                    # and keep going.
                    continue

# Now we write all the collected wicket rows into our output CSV file.
# newline="" is recommended when writing CSVs to avoid extra blank lines.
with open(output_file, "w", newline="") as f:

    # DictWriter lets us write dictionaries directly as CSV rows, matching
    # each dictionary's keys to the column headers we defined earlier.
    writer = csv.DictWriter(f, fieldnames=csv_headers)

    # This writes the header row (the column names) as the first line.
    writer.writeheader()

    # This writes one CSV row for every wicket dictionary we collected.
    writer.writerows(all_wicket_rows)

# Finally, print a summary of how many wickets were exported successfully.
print()
print("Total wickets successfully exported:", success_count)
print("Saved to:", output_file)
