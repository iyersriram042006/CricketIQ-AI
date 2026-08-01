# player_stats.py
# CricketIQ AI - Beginner script to read the deliveries.csv file we
# already generated, calculate basic batting statistics for every
# player, and save the results into a new CSV file.

import csv  # built-in module used to read and write CSV files

# This is the file we will read our ball-by-ball data from.
input_file = "../data/processed/deliveries.csv"

# This is the file we will save our calculated player stats to.
output_file = "../data/processed/player_stats.csv"

# This dictionary will hold the running stats for every batter.
# The key will be the batter's name, and the value will be another
# dictionary holding their runs, balls faced, fours, and sixes so far.
# Example: { "SC Ganguly": {"runs": 10, "balls": 8, "fours": 1, "sixes": 0} }
player_stats = {}

# Open the deliveries CSV file and read it row by row.
with open(input_file, "r") as f:

    # DictReader lets us access each row using the column names
    # (like row["Batter"]) instead of numeric positions.
    reader = csv.DictReader(f)

    # Loop through every single delivery (ball) in the file.
    for row in reader:

        # We use try/except so that if a row has bad or missing data
        # (like a run value that isn't a number), we just skip that
        # row instead of crashing the whole script.
        try:
            batter = row["Batter"]
            batter_runs = int(row["Batter Runs"])

            # "Wides" tells us if this delivery was a wide ball. We use
            # .get() with a default of "0" in case an older deliveries.csv
            # (generated before this column existed) doesn't have it.
            wides = int(row.get("Wides", 0) or 0)

            # If this is the first time we've seen this batter, create a
            # fresh stats dictionary for them, starting everything at 0.
            if batter not in player_stats:
                player_stats[batter] = {
                    "runs": 0,
                    "balls": 0,
                    "fours": 0,
                    "sixes": 0,
                }

            # Add this ball's runs to the batter's running total.
            # (Runs off a wide go to "extras" in real scoring, not to the
            # batter, so "Batter Runs" is already correctly 0 on wides.)
            player_stats[batter]["runs"] += batter_runs

            # Count this delivery as one ball faced by the batter, UNLESS
            # it was a wide. In real cricket scoring, a wide does not
            # count as a ball faced because the batter didn't get a fair
            # opportunity to play a shot. No-balls, byes, and leg-byes
            # still count as balls faced, so we only check for wides here.
            if wides == 0:
                player_stats[batter]["balls"] += 1

            # If the batter scored exactly 4 runs off this ball, count a four.
            if batter_runs == 4:
                player_stats[batter]["fours"] += 1

            # If the batter scored exactly 6 runs off this ball, count a six.
            if batter_runs == 6:
                player_stats[batter]["sixes"] += 1

        except (KeyError, ValueError):
            # KeyError = a column is missing from this row.
            # ValueError = "Batter Runs" couldn't be converted to a number.
            # Either way, skip this row safely and move on.
            continue

# Now that we've gone through every delivery, we calculate the strike
# rate for each player and prepare the final rows to write out.
# Strike Rate = (Runs / Balls Faced) * 100, rounded to 2 decimal places.
final_rows = []

for batter, stats in player_stats.items():

    runs = stats["runs"]
    balls = stats["balls"]
    fours = stats["fours"]
    sixes = stats["sixes"]

    # Guard against dividing by zero, just in case a player has 0 balls faced.
    if balls > 0:
        strike_rate = round((runs / balls) * 100, 2)
    else:
        strike_rate = 0.0

    # Build one row of output data for this player.
    final_rows.append({
        "Batter": batter,
        "Runs": runs,
        "Balls Faced": balls,
        "Fours": fours,
        "Sixes": sixes,
        "Strike Rate": strike_rate,
    })

# These are the column headers for our output CSV file, in order.
csv_headers = ["Batter", "Runs", "Balls Faced", "Fours", "Sixes", "Strike Rate"]

# Write all the player stats rows out to the output CSV file.
# newline="" is recommended when writing CSVs to avoid extra blank lines.
with open(output_file, "w", newline="") as f:

    # DictWriter lets us write dictionaries directly as CSV rows, matching
    # each dictionary's keys to the column headers we defined above.
    writer = csv.DictWriter(f, fieldnames=csv_headers)

    # Write the header row (the column names) as the first line.
    writer.writeheader()

    # Write one CSV row for every player we calculated stats for.
    writer.writerows(final_rows)

# Finally, print a short summary so we know the script worked.
print("Player stats calculated for", len(final_rows), "batters.")
print("Saved to:", output_file)
