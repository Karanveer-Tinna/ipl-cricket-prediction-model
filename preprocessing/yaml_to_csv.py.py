import os
import yaml
import pandas as pd
from tqdm import tqdm

# 👇 SET YOUR YAML FOLDER HERE
YAML_FOLDER = r"C:\Users\veerk\Downloads\ipl" # Folder where yaml folder is there
OUTPUT_CSV = "ipl_match_by_match.csv"

match_rows = []

for file in tqdm(os.listdir(YAML_FOLDER)):
    if file.endswith(".yaml"):
        with open(os.path.join(YAML_FOLDER, file), "r") as f:
            try:
                match = yaml.safe_load(f)
                match_id = file.replace(".yaml", "")
                info = match.get("info", {})
                date = info.get("dates", [None])[0]
                venue = info.get("venue")
                teams = info.get("teams", [None, None])
                team1, team2 = teams[0], teams[1]

                toss = info.get("toss", {})
                toss_winner = toss.get("winner")
                toss_decision = toss.get("decision")

                outcome = info.get("outcome", {})
                winner = outcome.get("winner", None)
                result_by = outcome.get("by", {})
                result = ""
                if "runs" in result_by:
                    result = f"won by {result_by['runs']} runs"
                elif "wickets" in result_by:
                    result = f"won by {result_by['wickets']} wickets"

                # Extract players (team1, team2)
                players_info = info.get("players", {})
                team1_players = players_info.get(team1, [])
                team2_players = players_info.get(team2, [])

                # Get batting order from innings
                innings = match.get("innings", [])
                first_batting_team = innings[0].get("1st innings", {}).get("team", "") if innings else ""
                second_batting_team = innings[1].get("2nd innings", {}).get("team", "") if len(innings) > 1 else ""

                # Get scores
                def get_team_score(innings_data):
                    total = 0
                    for delivery in innings_data.get("deliveries", []):
                        for _, ball_data in delivery.items():
                            total += ball_data.get("runs", {}).get("total", 0)
                    return total

                team1_score = get_team_score(innings[0].get("1st innings", {})) if innings else 0
                team2_score = get_team_score(innings[1].get("2nd innings", {})) if len(innings) > 1 else 0

                row = {
                    "match_id": match_id,
                    "date": date,
                    "venue": venue,
                    "team1": first_batting_team,
                    "team2": second_batting_team,
                    "toss_winner": toss_winner,
                    "toss_decision": toss_decision,
                    "winner": winner,
                    "result": result,
                    "team1_score": team1_score,
                    "team2_score": team2_score,
                    "team1_players": '' + ', '.join(team1_players) + '',
                    "team2_players": '' + ', '.join(team2_players) + ''
                }

                match_rows.append(row)

            except Exception as e:
                print(f"❌ Error in {file}: {e}")

# ✅ Create DataFrame & Export
df = pd.DataFrame(match_rows)
df.to_csv(OUTPUT_CSV, index=False)
print(f"✅ CSV saved as: {OUTPUT_CSV}")
