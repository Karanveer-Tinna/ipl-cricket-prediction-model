from collections import deque, defaultdict
import pandas as pd

# Read and sort dataset
df = pd.read_csv("ipl_ball_by_ball_revised_2.csv", parse_dates=['date'], dayfirst=True)
df = df.sort_values("date").reset_index(drop=True)

venue_replacements = {
    # Arun Jaitley
    "Arun Jaitley Stadium": "Arun Jaitley Stadium, Delhi",

    # Chinnaswamy
    "M Chinnaswamy Stadium": "M Chinnaswamy Stadium, Bengaluru",

    # Rajiv Gandhi
    "Rajiv Gandhi International Stadium": "Rajiv Gandhi International Stadium, Uppal, Hyderabad",
    "Rajiv Gandhi International Stadium, Uppal": "Rajiv Gandhi International Stadium, Uppal, Hyderabad",

    # HPCA Dharamsala
    "Himachal Pradesh Cricket Association Stadium": "Himachal Pradesh Cricket Association Stadium, Dharamsala",

    # Sawai Mansingh
    "Sawai Mansingh Stadium": "Sawai Mansingh Stadium, Jaipur",

    # DY Patil
    "Dr DY Patil Sports Academy": "Dr DY Patil Sports Academy, Mumbai",

    # Eden Gardens
    "Eden Gardens": "Eden Gardens, Kolkata",

    # Punjab Stadium
    "Punjab Cricket Association IS Bindra Stadium": "Punjab Cricket Association IS Bindra Stadium, Mohali, Chandigarh",
    "Punjab Cricket Association IS Bindra Stadium, Mohali": "Punjab Cricket Association IS Bindra Stadium, Mohali, Chandigarh",
    "Punjab Cricket Association Stadium, Mohali": "Punjab Cricket Association IS Bindra Stadium, Mohali, Chandigarh",

    # Wankhede
    "Wankhede Stadium": "Wankhede Stadium, Mumbai",

    # Chepauk
    "MA Chidambaram Stadium": "MA Chidambaram Stadium, Chepauk, Chennai",
    "MA Chidambaram Stadium, Chepauk": "MA Chidambaram Stadium, Chepauk, Chennai", 

    #Brabourne
    "Brabourne Stadium": "Brabourne Stadium, Mumbai",

    #YSRR Stadium
    "Dr. Y.S. Rajasekhara Reddy ACA-VDCA Cricket Stadium": "Dr. Y.S. Rajasekhara Reddy ACA-VDCA Cricket Stadium, Visakhapatnam",

    #MCA Stadium
    "Maharashtra Cricket Association Stadium": "Maharashtra Cricket Association Stadium, Pune",

    #Arun Jaitley
    "Feroz Shah Kotla":"Arun Jaitley Stadium, Delhi",

    #Narender Modi Stadium
    "Sardar Patel Stadium, Moter": "Narendra Modi Stadium, Ahmedabad", 

    #Sheilk Zayed Stadium
    "Sheikh Zayed Stadium" : "Zayed Cricket Stadium, Abu Dhabi"

}

# Apply the mapping to the DataFrame
df["venue"] = df["venue"].replace(venue_replacements)

team_replacements = {
    'Kings XI Punjab': 'Punjab Kings',
    'Royal Challengers Bangalore': 'Royal Challengers Bengaluru',
    'Delhi Daredevils': 'Delhi Capitals',
    'Rising Pune Supergiant':'Rising Pune Supergiants'
}

df["team1"] = df["team1"].replace(team_replacements)
df["team2"] = df["team2"].replace(team_replacements)
df["winner"] = df["winner"].replace(team_replacements)
df["toss_winner"] = df["toss_winner"].replace(team_replacements)

# Initialize tracking structures
team_last_5_results = defaultdict(lambda: deque(maxlen=5))
team_last_5_scores = defaultdict(lambda: deque(maxlen=5))
team_last_5_conceded = defaultdict(lambda: deque(maxlen=5))

# Initialize output lists
team1_form_list = []
team2_form_list = []
team1_avg_score_list = []
team1_avg_conceded_list = []
team2_avg_score_list = []
team2_avg_conceded_list = []

# Add new columns
new_columns = [
    "venue_avg_score", "chasing_win_rate_venue",
    "team1_win_rate_at_venue", "team2_win_rate_at_venue",
    "team1_total_wins_against_team2", "team2_total_wins_against_team1",
    "team1_wins_against_team2_last_three", "team2_wins_against_team1_last_three",
    "team1_chasing_win_rate", "team1_defending_win_rate",
    "team2_chasing_win_rate", "team2_defending_win_rate"
]
df[new_columns] = 0.0

# Average helper
def avg(dq):
    return round(sum(dq) / len(dq), 2) if dq else 0

# Process each match row-by-row
for idx, row in df.iterrows():
    team1, team2 = row['team1'], row['team2']
    team1_score, team2_score = row['team1_score'], row['team2_score']
    winner = row['winner']
    venue = row['venue']

    # --- Last 5 form and score-based features ---
    team1_form_list.append(sum(team_last_5_results[team1]))
    team2_form_list.append(sum(team_last_5_results[team2]))

    team1_avg_score_list.append(avg(team_last_5_scores[team1]))
    team1_avg_conceded_list.append(avg(team_last_5_conceded[team1]))
    team2_avg_score_list.append(avg(team_last_5_scores[team2]))
    team2_avg_conceded_list.append(avg(team_last_5_conceded[team2]))

    # Update form results
    if winner == team1:
        team_last_5_results[team1].append(1)
        team_last_5_results[team2].append(0)
    elif winner == team2:
        team_last_5_results[team1].append(0)
        team_last_5_results[team2].append(1)
    else:
        team_last_5_results[team1].append(0)
        team_last_5_results[team2].append(0)

    # Update score and conceded trackers
    team_last_5_scores[team1].append(team1_score)
    team_last_5_conceded[team1].append(team2_score)
    team_last_5_scores[team2].append(team2_score)
    team_last_5_conceded[team2].append(team1_score)

    # --- Historical feature calculations ---
    past_matches = df.iloc[:idx]

    # Venue average score
    venue_matches = past_matches[past_matches['venue'] == venue]
    if not venue_matches.empty:
        avg_score = (venue_matches['team1_score'] + venue_matches['team2_score']) / 2
        df.at[idx, 'venue_avg_score'] = avg_score.mean()

    # Chasing win rate at venue
    chasing = venue_matches[venue_matches['toss_decision'] == 'field']
    chasing_wins = chasing[chasing['toss_winner'] == chasing['winner']]
    df.at[idx, 'chasing_win_rate_venue'] = len(chasing_wins) / len(chasing) if len(chasing) else 0

    # Team win rate at venue
    for team_col in ['team1', 'team2']:
        team = row[team_col]
        appearances = venue_matches[(venue_matches['team1'] == team) | (venue_matches['team2'] == team)]
        wins = appearances[appearances['winner'] == team]
        df.at[idx, f'{team_col}_win_rate_at_venue'] = len(wins) / len(appearances) if len(appearances) else 0

    # Head-to-head total wins
    head_to_head = past_matches[
        ((past_matches['team1'] == team1) & (past_matches['team2'] == team2)) |
        ((past_matches['team1'] == team2) & (past_matches['team2'] == team1))
    ]
    df.at[idx, 'team1_total_wins_against_team2'] = (head_to_head['winner'] == team1).sum()
    df.at[idx, 'team2_total_wins_against_team1'] = (head_to_head['winner'] == team2).sum()

    # Last 3 matches head-to-head
    last_three = head_to_head.sort_values('date', ascending=False).head(3)
    df.at[idx, 'team1_wins_against_team2_last_three'] = (last_three['winner'] == team1).sum()
    df.at[idx, 'team2_wins_against_team1_last_three'] = (last_three['winner'] == team2).sum()

    # Chasing/defending win rate
    for team, prefix in [(team1, 'team1'), (team2, 'team2')]:
        chasing_matches = past_matches[
            ((past_matches['team1'] == team) | (past_matches['team2'] == team)) &
            (past_matches['toss_winner'] == team) &
            (past_matches['toss_decision'] == 'field')
        ]
        chasing_wins = chasing_matches[chasing_matches['winner'] == team]
        chasing_rate = len(chasing_wins) / len(chasing_matches) if len(chasing_matches) else 0

        defending_matches = past_matches[
            ((past_matches['team1'] == team) | (past_matches['team2'] == team)) &
            (past_matches['toss_winner'] == team) &
            (past_matches['toss_decision'] == 'bat')
        ]
        defending_wins = defending_matches[defending_matches['winner'] == team]
        defending_rate = len(defending_wins) / len(defending_matches) if len(defending_matches) else 0

        df.at[idx, f"{prefix}_chasing_win_rate"] = chasing_rate
        df.at[idx, f"{prefix}_defending_win_rate"] = defending_rate

# Add last-5 form and scoring columns
df["team1_form_last_5"] = team1_form_list
df["team2_form_last_5"] = team2_form_list
df["team1_last_5_avg_score"] = team1_avg_score_list
df["team1_last_5_runs_conceded"] = team1_avg_conceded_list
df["team2_last_5_avg_score"] = team2_avg_score_list
df["team2_last_5_runs_conceded"] = team2_avg_conceded_list

# Save final match-by-match dataset
df.to_csv("ipl_final_clean_dataset.csv", index=False)
