import pandas as pd

# Read dataset
df = pd.read_csv("ipl_master_dataset_revised.csv", parse_dates=['date'], dayfirst=True)

# Sort by date
df = df.sort_values("date").reset_index(drop=True)

# Initialize new columns
df["venue_avg_score"] = 0.0
df["chasing_win_rate_venue"] = 0.0
df["team1_win_rate_at_venue"] = 0.0
df["team2_win_rate_at_venue"] = 0.0
df["team1_total_wins_against_team2"] = 0.0
df["team2_total_wins_against_team1"] = 0.0
df["team1_wins_against_team2_last_three"] = 0.0
df["team2_wins_against_team1_last_three"] = 0.0


# Loop through each match to calculate values from historical data
for idx, row in df.iterrows():
    past_matches = df.iloc[:idx]  # Only past data
    
    # Venue average score
    venue_matches = past_matches[past_matches['venue'] == row['venue']]
    if not venue_matches.empty:
        avg_score = (venue_matches['team1_score'] + venue_matches['team2_score']) / 2
        df.at[idx, 'venue_avg_score'] = avg_score.mean()
    
    # Chasing win rate at venue
    chasing = venue_matches[venue_matches['toss_decision'] == 'field']
    chasing_wins = chasing[chasing['toss_winner'] == chasing['winner']]
    df.at[idx, 'chasing_win_rate_venue'] = len(chasing_wins) / len(chasing) if len(chasing) else 0

    # Team win rates at venue
    for team_col in ['team1', 'team2']:
        team = row[team_col]
        appearances = venue_matches[(venue_matches['team1'] == team) | (venue_matches['team2'] == team)]
        wins = appearances[appearances['winner'] == team]
        df.at[idx, f'{team_col}_win_rate_at_venue'] = len(wins) / len(appearances) if len(appearances) else 0

    # Total head-to-head wins
    team1, team2 = row['team1'], row['team2']
    head_to_head = past_matches[
        ((past_matches['team1'] == team1) & (past_matches['team2'] == team2)) |
        ((past_matches['team1'] == team2) & (past_matches['team2'] == team1))
    ]
    df.at[idx, 'team1_total_wins_against_team2'] = (head_to_head['winner'] == team1).sum()
    df.at[idx, 'team2_total_wins_against_team1'] = (head_to_head['winner'] == team2).sum()

    # Last 3 matches
    last_three = head_to_head.sort_values('date', ascending=False).head(3)
    df.at[idx, 'team1_wins_against_team2_last_three'] = (last_three['winner'] == team1).sum()
    df.at[idx, 'team2_wins_against_team1_last_three'] = (last_three['winner'] == team2).sum()

df.to_csv("ipl_analysis_combined.csv", index=False)