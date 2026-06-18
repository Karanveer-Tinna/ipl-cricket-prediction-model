import os
import yaml
import pandas as pd
from tqdm import tqdm

YAML_FOLDER = r"C:\Users\veerk\Downloads\ipl_2008"
OUTPUT_CSV = "ipl_ball_by_ball_revised.csv"

rows = []

for file in tqdm(os.listdir(YAML_FOLDER)):
    if file.endswith(".yaml"):
        with open(os.path.join(YAML_FOLDER, file), "r") as f:
            try:
                match = yaml.safe_load(f)
                match_id = file.replace(".yaml", "")
                innings = match.get("innings", [])

                for inning in innings:
                    for inning_name, inning_data in inning.items():
                        batting_team = inning_data.get("team", "")
                        deliveries = inning_data.get("deliveries", [])  # Typo fix: deliveries

                        for delivery in deliveries:
                            for ball, info in delivery.items():
                                over, ball_number = map(int, str(ball).split('.'))  # Ensure over and ball are integers
                                row = {
                                    "match_id": match_id,
                                    "inning": inning_name,
                                    "batting_team": batting_team,
                                    "bowling_team": info.get("bowler", ""),  # temp; fix below
                                    "over": over,
                                    "ball": ball_number,
                                    "batsman": info.get("batsman", ""),  # Added batsman
                                    "runs_batsman": info.get("runs", {}).get("batsman", 0),
                                    "runs_total": info.get("runs", {}).get("total", 0)
                                }
                                rows.append(row)
            except Exception as e:
                print(f"❌ Error in {file}: {e}")

df = pd.DataFrame(rows)

# Fix bowling_team using non-striker team
def fix_bowling_team(row, match_innings):
    teams = match_innings.get(row["match_id"], ("", ""))
    return teams[1] if row["batting_team"] == teams[0] else teams[0]

# Build match teams for correction
match_teams = {}
for file in os.listdir(YAML_FOLDER):
    if file.endswith(".yaml"):
        with open(os.path.join(YAML_FOLDER, file), "r") as f:
            match = yaml.safe_load(f)
            match_id = file.replace(".yaml", "")
            teams = match.get("info", {}).get("teams", ["", ""])
            match_teams[match_id] = (teams[0], teams[1])

df["bowling_team"] = df.apply(lambda x: fix_bowling_team(x, match_teams), axis=1)

df.to_csv(OUTPUT_CSV, index=False)
print(f"✅ Ball-by-ball data saved as: {OUTPUT_CSV}")