from collections import deque, defaultdict
import pandas as pd

df = pd.read_csv("ipl_match_summary.csv")

# Keep a sliding window of last 5 match results per team
team_last_5_results = defaultdict(lambda: deque(maxlen=5))

team1_form_list = []
team2_form_list = []

for _, row in df.iterrows():
    team1 = row["team1"]
    team2 = row["team2"]
    winner = row["winner"]

    # Count past wins from deque for each team
    team1_wins_last5 = sum(team_last_5_results[team1])
    team2_wins_last5 = sum(team_last_5_results[team2])

    team1_form_list.append(team1_wins_last5)
    team2_form_list.append(team2_wins_last5)

    # Update match result for each team
    if winner == team1:
        team_last_5_results[team1].append(1)
        team_last_5_results[team2].append(0)
    elif winner == team2:
        team_last_5_results[team1].append(0)
        team_last_5_results[team2].append(1)
    else:
        # In case of tie/no result
        team_last_5_results[team1].append(0)
        team_last_5_results[team2].append(0)

# Add the new columns
df["team1_form_last_5"] = team1_form_list
df["team2_form_last_5"] = team2_form_list

# saving the dataframe
df.to_csv('ipl_match_analysis_demo.csv')
