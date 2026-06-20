import pandas as pd


def add_venue_head_to_head_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds venue and head-to-head based features.

    Features added:
    - venue_avg_score
    - chasing_win_rate_venue
    - team1_win_rate_at_venue
    - team2_win_rate_at_venue
    - team1_total_wins_against_team2
    - team2_total_wins_against_team1
    - team1_wins_against_team2_last_three
    - team2_wins_against_team1_last_three

    Parameters
    ----------
    df : pd.DataFrame
        Match-level dataframe.

    Returns
    -------
    pd.DataFrame
        DataFrame with added venue and head-to-head features.
    """

    result_df = df.copy()

    result_df = (
        result_df.sort_values("date")
        .reset_index(drop=True)
    )

    result_df["venue_avg_score"] = 0.0
    result_df["chasing_win_rate_venue"] = 0.0
    result_df["team1_win_rate_at_venue"] = 0.0
    result_df["team2_win_rate_at_venue"] = 0.0
    result_df["team1_total_wins_against_team2"] = 0.0
    result_df["team2_total_wins_against_team1"] = 0.0
    result_df["team1_wins_against_team2_last_three"] = 0.0
    result_df["team2_wins_against_team1_last_three"] = 0.0

    for idx, row in result_df.iterrows():

        past_matches = result_df.iloc[:idx]

        venue_matches = past_matches[
            past_matches["venue"] == row["venue"]
        ]

        if not venue_matches.empty:
            avg_score = (
                venue_matches["team1_score"]
                + venue_matches["team2_score"]
            ) / 2

            result_df.at[idx, "venue_avg_score"] = avg_score.mean()

        # ---------------- Chasing Win Rate ----------------
        chasing = venue_matches[
            venue_matches["toss_decision"] == "field"
        ]

        chasing_wins = chasing[
            chasing["toss_winner"] == chasing["winner"]
        ]

        result_df.at[idx, "chasing_win_rate_venue"] = (
            len(chasing_wins) / len(chasing)
            if len(chasing)
            else 0
        )

        # ---------------- Team Win Rates at Venue ----------------
        for team_col in ["team1", "team2"]:

            team = row[team_col]

            appearances = venue_matches[
                (venue_matches["team1"] == team)
                | (venue_matches["team2"] == team)
            ]

            wins = appearances[
                appearances["winner"] == team
            ]

            result_df.at[
                idx,
                f"{team_col}_win_rate_at_venue"
            ] = (
                len(wins) / len(appearances)
                if len(appearances)
                else 0
            )

        # ---------------- Head-to-Head Features ----------------
        team1 = row["team1"]
        team2 = row["team2"]

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

        result_df.at[
            idx,
            "team1_total_wins_against_team2"
        ] = (head_to_head["winner"] == team1).sum()

        result_df.at[
            idx,
            "team2_total_wins_against_team1"
        ] = (head_to_head["winner"] == team2).sum()

        # ---------------- Last 3 Head-to-Head Matches ----------------
        last_three = (
            head_to_head
            .sort_values("date", ascending=False)
            .head(3)
        )

        result_df.at[
            idx,
            "team1_wins_against_team2_last_three"
        ] = (last_three["winner"] == team1).sum()

        result_df.at[
            idx,
            "team2_wins_against_team1_last_three"
        ] = (last_three["winner"] == team2).sum()

    print("Added venue_head_to_head_features:")
    print(" - venue_avg_score")
    print(" - chasing_win_rate_venue")
    print(" - team1_win_rate_at_venue")
    print(" - team2_win_rate_at_venue")
    print(" - team1_total_wins_against_team2")
    print(" - team2_total_wins_against_team1")
    print(" - team1_wins_against_team2_last_three")
    print(" - team2_wins_against_team1_last_three")

    return result_df