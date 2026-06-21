from collections import deque, defaultdict
import pandas as pd


def add_team_form_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds rolling form features for both teams based on wins
    in their previous 5 matches.

    Parameters
    ----------
    df : pd.DataFrame
        Match-level dataframe containing:
        ['team1', 'team2', 'winner']

    Returns
    -------
    pd.DataFrame
        DataFrame with two new columns:
        - team1_form_last_5
        - team2_form_last_5
    """

    result_df = df.copy()

    team_last_5_results = defaultdict(lambda: deque(maxlen=5))

    team1_form_list = []
    team2_form_list = []

    for _, row in result_df.iterrows():
        team1 = row["team1"]
        team2 = row["team2"]
        winner = row["winner"]

        team1_wins_last5 = sum(team_last_5_results[team1])
        team2_wins_last5 = sum(team_last_5_results[team2])

        team1_form_list.append(team1_wins_last5)
        team2_form_list.append(team2_wins_last5)

        if winner == team1:
            team_last_5_results[team1].append(1)
            team_last_5_results[team2].append(0)

        elif winner == team2:
            team_last_5_results[team1].append(0)
            team_last_5_results[team2].append(1)

        else:
            team_last_5_results[team1].append(0)
            team_last_5_results[team2].append(0)

    result_df["team1_form_last_5"] = team1_form_list
    result_df["team2_form_last_5"] = team2_form_list

    print("Added team_form_features:")
    print(" - team1_form_last_5")
    print(" - team2_form_last_5")

    return result_df