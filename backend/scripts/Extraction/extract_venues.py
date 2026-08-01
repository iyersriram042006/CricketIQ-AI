# extract_venues.py
# CricketIQ AI - Beginner script to read ALL IPL match JSON files
# inside a folder, pull out every unique venue (along with its city)
# mentioned across all matches, and save them into a single CSV file
# with a simple auto-incrementing Venue ID (1, 2, 3, ...).

import json  # built-in module used to read and parse JSON files
import os    # built-in module used to work with file paths and folders
import csv   # built-in module used to write data out in CSV format

# This is the folder where all our match JSON files live.
# We build this path based on WHERE THIS SCRIPT FILE ITSELF is located,
# instead of relying on the folder the terminal happens to be in when
# you run the script. This way, the script works correctly no matter
# which directory you run "python extract_venues.py" from.
#
# Your folder layout is:
#   CricketIQ-AI/              <- project_root (this is where "data/" lives)
#     backend/
#       scripts/
#         Extraction/
#           extract_venues.py  <- script_dir (this file)
#
# So we go up 3 levels from this script's folder: out of "Extraction",
# out of "scripts", out of "backend" - to land on "CricketIQ-AI".
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(os.path.dirname(script_dir)))
input_folder = os.path.join(project_root, "data", "raw")

# This is the folder + filename where we want to save our results.
output_folder = os.path.join(project_root, "data", "processed")
output_file = os.path.join(output_folder, "venues.csv")

# If the "processed" folder doesn't exist yet, create it now.
# Without this, trying to open a file inside a missing folder would crash.
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# These are the column headers we want in our CSV file, in order.
csv_headers = ["Venue ID", "Venue Name", "City"]

# Get a list of every file in the input folder, then keep only the
# ones that end in ".json" (in case other file types are in there too).
all_files = os.listdir(input_folder)
json_files = [f for f in all_files if f.endswith(".json")]

# This dictionary will hold every unique venue we find across all
# match files. The key is the venue name, and the value is its city.
# Using a dictionary automatically prevents duplicate venues from being
# added twice, even if the same venue appears in hundreds of matches.
unique_venues = {}

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

    # Each match file lists the venue and city under "info". We use
    # .get() with an empty string as the default, in case either field
    # is missing from a particular file for some reason.
    venue_name = data.get("info", {}).get("venue", "")
    city = data.get("info", {}).get("city", "")

    # Only add this venue if it actually has a name. A blank venue
    # name would be useless as a lookup value, so we skip those.
    if venue_name != "":
        # If we've already seen this venue before, we simply leave the
        # existing entry as-is (dictionaries automatically overwrite on
        # a repeated key, so the city just gets confirmed, not duplicated).
        unique_venues[venue_name] = city

# Now we turn our dictionary of unique venues into a sorted list of
# (venue_name, city) pairs. Sorting alphabetically by venue name makes
# the output predictable and easy to read, and also means Venue IDs
# stay consistent every time we re-run the script on the same data.
sorted_venue_names = sorted(unique_venues.keys())

# Build the final list of rows to write to the CSV. We use enumerate()
# starting at 1 so the first venue gets Venue ID 1, the second gets 2,
# and so on - a simple auto-incrementing ID.
final_rows = []
for venue_id, venue_name in enumerate(sorted_venue_names, start=1):
    final_rows.append({
        "Venue ID": venue_id,
        "Venue Name": venue_name,
        "City": unique_venues[venue_name],
    })

# Write all the venue rows out to the output CSV file.
# newline="" is recommended when writing CSVs to avoid extra blank lines.
with open(output_file, "w", newline="") as f:

    # DictWriter lets us write dictionaries directly as CSV rows, matching
    # each dictionary's keys to the column headers we defined earlier.
    writer = csv.DictWriter(f, fieldnames=csv_headers)

    # This writes the header row (the column names) as the first line.
    writer.writeheader()

    # This writes one CSV row for every unique venue we collected.
    writer.writerows(final_rows)

# Finally, print a summary of how many unique venues were exported.
print()
print("Total unique venues extracted:", len(final_rows))
print("Saved to:", output_file)
