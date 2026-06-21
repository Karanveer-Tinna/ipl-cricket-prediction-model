import pandas as pd


def add_team_strategy_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds historical chasing and defending win-rate features.

    Features added:
    - team1_chasing_win_rate
    - team1_defending_win_rate
    - team2_chasing_win_rate
    - team2_defending_win_rate

    Parameters
    ----------
    df : pd.DataFrame
        Match-level dataframe containing:
        ['date', 'team1', 'team2',
         'toss_winner', 'toss_decision', 'winner']

    Returns
    -------
    pd.DataFrame
        DataFrame with added strategy features.
    """

    result_df = (
        df.copy()
        .sort_values("date")
        .reset_index(drop=True)
    )

    # Initialize columns
    result_df["team1_chasing_win_rate"] = 0.0
    result_df["team1_defending_win_rate"] = 0.0
    result_df["team2_chasing_win_rate"] = 0.0
    result_df["team2_defending_win_rate"] = 0.0

    for idx, row in result_df.iterrows():

        past_matches = result_df.iloc[:idx]

        team1 = row["team1"]
        team2 = row["team2"]

        for team in [team1, team2]:

            team_matches = past_matches[
                (past_matches["team1"] == team)
                | (past_matches["team2"] == team)
            ]

            # Chasing matches
            chasing_matches = team_matches[
                (team_matches["toss_winner"] == team)
                & (team_matches["toss_decision"] == "field")
            ]

            chasing_wins = chasing_matches[
                chasing_matches["winner"] == team
            ]

            chasing_rate = (
                len(chasing_wins) / len(chasing_matches)
                if len(chasing_matches)
                else 0
            )

            # Defending matches
            defending_matches = team_matches[
                (team_matches["toss_winner"] == team)
                & (team_matches["toss_decision"] == "bat")
            ]

            defending_wins = defending_matches[
                defending_matches["winner"] == team
            ]

            defending_rate = (
                len(defending_wins) / len(defending_matches)
                if len(defending_matches)
                else 0
            )

            if team == team1:
                result_df.at[idx, "team1_chasing_win_rate"] = round(
                    chasing_rate, 3
                )
                result_df.at[idx, "team1_defending_win_rate"] = round(
                    defending_rate, 3
                )
            else:
                result_df.at[idx, "team2_chasing_win_rate"] = round(
                    chasing_rate, 3
                )
                result_df.at[idx, "team2_defending_win_rate"] = round(
                    defending_rate, 3
                )

    print("Added team_strategy_features:")
    print(" - team1_chasing_win_rate")
    print(" - team1_defending_win_rate")
    print(" - team2_chasing_win_rate")
    print(" - team2_defending_win_rate")

    return result_df