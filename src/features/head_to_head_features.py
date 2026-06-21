# head_to_head_features.py

import pandas as pd


def add_head_to_head_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add historical head-to-head features between team1 and team2.

    Features added:
    - team1_total_wins_against_team2
    - team2_total_wins_against_team1
    - team1_wins_against_team2_last_three
    - team2_wins_against_team1_last_three

    Parameters
    ----------
    df : pd.DataFrame
        Match-level dataframe containing:
        ['date', 'team1', 'team2', 'winner']

    Returns
    -------
    pd.DataFrame
        DataFrame with added head-to-head features.
    """

    result_df = df.copy()

    # Ensure matches are processed chronologically
    result_df = (
        result_df
        .sort_values("date")
        .reset_index(drop=True)
    )

    # Initialize columns
    result_df["team1_total_wins_against_team2"] = 0
    result_df["team2_total_wins_against_team1"] = 0
    result_df["team1_wins_against_team2_last_three"] = 0
    result_df["team2_wins_against_team1_last_three"] = 0

    # Generate features using only past matches
    for idx, row in result_df.iterrows():

        past_matches = result_df.iloc[:idx]

        team1 = row["team1"]
        team2 = row["team2"]

        # All previous meetings between the two teams
        head_to_head = past_matches[
            (
                (past_matches["team1"] == team1)
                & (past_matches["team2"] == team2)
            )
            |
            (
                (past_matches["team1"] == team2)
                & (past_matches["team2"] == team1)
            )
        ]

        # Total wins
        team1_total_wins = (
            head_to_head["winner"] == team1
        ).sum()

        team2_total_wins = (
            head_to_head["winner"] == team2
        ).sum()

        result_df.at[
            idx,
            "team1_total_wins_against_team2"
        ] = team1_total_wins

        result_df.at[
            idx,
            "team2_total_wins_against_team1"
        ] = team2_total_wins

        # Last 3 head-to-head matches
        last_three = (
            head_to_head
            .sort_values("date", ascending=False)
            .head(3)
        )

        team1_last_three_wins = (
            last_three["winner"] == team1
        ).sum()

        team2_last_three_wins = (
            last_three["winner"] == team2
        ).sum()

        result_df.at[
            idx,
            "team1_wins_against_team2_last_three"
        ] = team1_last_three_wins

        result_df.at[
            idx,
            "team2_wins_against_team1_last_three"
        ] = team2_last_three_wins

    print("Added head_to_head_features:")
    print(" - team1_total_wins_against_team2")
    print(" - team2_total_wins_against_team1")
    print(" - team1_wins_against_team2_last_three")
    print(" - team2_wins_against_team1_last_three")

    return result_df