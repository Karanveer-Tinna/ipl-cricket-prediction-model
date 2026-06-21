import pandas as pd


def add_venue_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add venue-based historical features.

    Features added:
    - venue_avg_score
    - chasing_win_rate_venue
    - team1_win_rate_at_venue
    - team2_win_rate_at_venue

    Parameters
    ----------
    df : pd.DataFrame
        Match-level dataframe containing:
        ['date', 'venue', 'team1', 'team2',
         'team1_score', 'team2_score',
         'toss_winner', 'toss_decision', 'winner']

    Returns
    -------
    pd.DataFrame
        DataFrame with added venue features.
    """

    result_df = df.copy()

    result_df = (
        result_df
        .sort_values("date")
        .reset_index(drop=True)
    )

    result_df["venue_avg_score"] = 0.0
    result_df["chasing_win_rate_venue"] = 0.0
    result_df["team1_win_rate_at_venue"] = 0.0
    result_df["team2_win_rate_at_venue"] = 0.0

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

            result_df.at[idx, "venue_avg_score"] = round(
                avg_score.mean(),
                2
            )

        chasing_matches = venue_matches[
            venue_matches["toss_decision"] == "field"
        ]

        chasing_wins = chasing_matches[
            chasing_matches["toss_winner"]
            == chasing_matches["winner"]
        ]

        result_df.at[idx, "chasing_win_rate_venue"] = round(
            (
                len(chasing_wins)
                / len(chasing_matches)
            )
            if len(chasing_matches)
            else 0,
            3,
        )

        for team_col in ["team1", "team2"]:

            team = row[team_col]

            appearances = venue_matches[
                (venue_matches["team1"] == team)
                | (venue_matches["team2"] == team)
            ]

            wins = appearances[
                appearances["winner"] == team
            ]

            win_rate = (
                len(wins)
                / len(appearances)
                if len(appearances)
                else 0
            )

            result_df.at[
                idx,
                f"{team_col}_win_rate_at_venue"
            ] = round(win_rate, 3)

    print("Added venue_features:")
    print(" - venue_avg_score")
    print(" - chasing_win_rate_venue")
    print(" - team1_win_rate_at_venue")
    print(" - team2_win_rate_at_venue")

    return result_df