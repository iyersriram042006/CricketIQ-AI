# extract_extras_breakdown.py
# CricketIQ AI - Beginner script to read ALL IPL match JSON files
# inside a folder, pull out every extra (wide, no-ball, bye, leg-bye,
# penalty) recorded on any delivery, and save one row PER EXTRA TYPE
# into a single CSV file.

import json  # built-in module used to read and parse JSON files
import os    # built-in module used to work with file paths and folders
import csv   # built-in module used to write data out in CSV format

# This is the folder where all our match JSON files live.
# We build this path based on WHERE THIS SCRIPT FILE ITSELF is located,
# instead of relying on the folder the terminal happens to be in when
# you run the script. This way, the script works correctly no matter
# which directory you run "python extract_extras_breakdown.py" from.
#
# Your folder layout is:
#   CricketIQ-AI/                         <- project_root (this is where "data/" lives)
#     backend/
#       scripts/
#         Extraction/
#           extract_extras_breakdown.py   <- script_dir (this file)
#
# So we go up 3 levels from this script's folder: out of "Extraction",
# out of "scripts", out of "backend" - to land on "CricketIQ-AI".
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(os.path.dirname(script_dir)))
input_folder = os.path.join(project_root, "data", "raw")

# This is the folder + filename where we want to save our results.
output_folder = os.path.join(project_root, "data", "processed")
output_file = os.path.join(output_folder, "extras_breakdown.csv")

# If the "processed" folder doesn't exist yet, create it now.
# Without this, trying to open a file inside a missing folder would crash.
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# These are the column headers we want in our CSV file, in order.
csv_headers = [
    "Match ID",
    "Innings Number",
    "Over",
    "Ball Number",
    "Extra Type",
    "Extra Runs",
]

# These are the ONLY extra types we care about, in the exact spelling
# used inside the JSON's "extras" dictionary. We loop through this
# fixed list on every delivery instead of guessing at whatever keys
# might be present, so our output stays consistent and predictable.
extra_type_names = ["wides", "noballs", "byes", "legbyes", "penalty"]

# Get a list of every file in the input folder, then keep only the
# ones that end in ".json" (in case other file types are in there too).
all_files = os.listdir(input_folder)
json_files = [f for f in all_files if f.endswith(".json")]

# This list will hold one row (as a dictionary) per extra that we
# successfully process. We will write all of these to the CSV at the end.
all_extra_rows = []

# This variable keeps count of how many extras we successfully export.
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

                # Not every ball has extras. The "extras" key only
                # exists on the delivery when something unusual (wide,
                # no-ball, bye, etc) happened, so if it's missing we
                # skip straight to the next delivery - per the "skip
                # deliveries without extras" rule.
                if "extras" not in delivery:
                    continue

                # We use try/except here so that if "actual_delivery"
                # is missing or shaped unexpectedly, we skip just this
                # delivery's extras instead of crashing the script.
                try:
                    # "actual_delivery" looks like "0.1", "0.2", etc.
                    # The part after the dot is the ball number within
                    # the over.
                    actual_delivery = delivery["actual_delivery"]
                    ball_number = actual_delivery.split(".")[1]
                except (KeyError, IndexError):
                    # A required field was missing on this delivery -
                    # skip its extras safely and keep going.
                    continue

                extras_dict = delivery["extras"]

                # A single delivery's "extras" dictionary can contain
                # MORE THAN ONE extra type at once (for example, a wide
                # that also went for a bye). So we check each of our
                # five known extra types individually, and create a
                # SEPARATE row for each one that is actually present.
                for extra_type in extra_type_names:

                    if extra_type in extras_dict:
                        extra_runs = extras_dict[extra_type]

                        # Build and store the row for this extra.
                        extra_row = {
                            "Match ID": match_id,
                            "Innings Number": innings_number,
                            "Over": over_number,
                            "Ball Number": ball_number,
                            "Extra Type": extra_type,
                            "Extra Runs": extra_runs,
                        }
                        all_extra_rows.append(extra_row)

                        # Increase our success counter by 1 for each extra.
                        success_count = success_count + 1

# Now we write all the collected extra rows into our output CSV file.
# newline="" is recommended when writing CSVs to avoid extra blank lines.
with open(output_file, "w", newline="") as f:

    # DictWriter lets us write dictionaries directly as CSV rows, matching
    # each dictionary's keys to the column headers we defined earlier.
    writer = csv.DictWriter(f, fieldnames=csv_headers)

    # This writes the header row (the column names) as the first line.
    writer.writeheader()

    # This writes one CSV row for every extra we collected.
    writer.writerows(all_extra_rows)

# Finally, print a summary of how many records were exported.
print()
print("Total records extracted:", success_count)
print("Saved to:", output_file)
