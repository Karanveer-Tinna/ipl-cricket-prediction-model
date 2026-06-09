from collections import deque, defaultdict
import pandas as pd

# Track last 5 scores and conceded runs per team
team_last_5_scores = defaultdict(lambda: deque(maxlen=5))
team_last_5_conceded = defaultdict(lambda: deque(maxlen=5))

team1_avg_score_list = []
team1_avg_conceded_list = []
team2_avg_score_list = []
team2_avg_conceded_list = []

df = pd.read_csv("ipl_analysis_combined.csv")

for _, row in df.iterrows():
    team1 = row["team1"]
    team2 = row["team2"]
    team1_score = row["team1_score"]
    team2_score = row["team2_score"]

    # Averages of last 5 scores/conceded
    def avg(dq): return round(sum(dq)/len(dq), 2) if dq else 0

    team1_avg_score_list.append(avg(team_last_5_scores[team1]))
    team1_avg_conceded_list.append(avg(team_last_5_conceded[team1]))
    team2_avg_score_list.append(avg(team_last_5_scores[team2]))
    team2_avg_conceded_list.append(avg(team_last_5_conceded[team2]))

    # Update last 5 records
    team_last_5_scores[team1].append(team1_score)
    team_last_5_conceded[team1].append(team2_score)

    team_last_5_scores[team2].append(team2_score)
    team_last_5_conceded[team2].append(team1_score)

# Assign to DataFrame
df["team1_last_5_avg_score"] = team1_avg_score_list
df["team1_last_5_runs_conceded"] = team1_avg_conceded_list
df["team2_last_5_avg_score"] = team2_avg_score_list
df["team2_last_5_runs_conceded"] = team2_avg_conceded_list

df.to_csv("ipl_analysis_combined.csv", index=False)

