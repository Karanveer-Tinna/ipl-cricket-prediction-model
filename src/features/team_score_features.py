from collections import deque, defaultdict
import pandas as pd


def add_team_scoring_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds rolling scoring features based on each team's
    previous 5 matches.

    Features added:
    - team1_last_5_avg_score
    - team1_last_5_runs_conceded
    - team2_last_5_avg_score
    - team2_last_5_runs_conceded

    Parameters
    ----------
    df : pd.DataFrame
        Match-level dataframe containing:
        ['team1', 'team2', 'team1_score', 'team2_score']

    Returns
    -------
    pd.DataFrame
        DataFrame with the new scoring features.
    """

    result_df = df.copy()

    team_last_5_scores = defaultdict(lambda: deque(maxlen=5))
    team_last_5_conceded = defaultdict(lambda: deque(maxlen=5))

    team1_avg_score_list = []
    team1_avg_conceded_list = []
    team2_avg_score_list = []
    team2_avg_conceded_list = []

    def avg(dq):
        return round(sum(dq) / len(dq), 2) if dq else 0

    for _, row in result_df.iterrows():
        team1 = row["team1"]
        team2 = row["team2"]
        team1_score = row["team1_score"]
        team2_score = row["team2_score"]

        team1_avg_score_list.append(avg(team_last_5_scores[team1]))
        team1_avg_conceded_list.append(avg(team_last_5_conceded[team1]))

        team2_avg_score_list.append(avg(team_last_5_scores[team2]))
        team2_avg_conceded_list.append(avg(team_last_5_conceded[team2]))

        team_last_5_scores[team1].append(team1_score)
        team_last_5_conceded[team1].append(team2_score)

        team_last_5_scores[team2].append(team2_score)
        team_last_5_conceded[team2].append(team1_score)

    result_df["team1_last_5_avg_score"] = team1_avg_score_list
    result_df["team1_last_5_runs_conceded"] = team1_avg_conceded_list
    result_df["team2_last_5_avg_score"] = team2_avg_score_list
    result_df["team2_last_5_runs_conceded"] = team2_avg_conceded_list

    print("Added team_scoring_features:")
    print(" - team1_last_5_avg_score")
    print(" - team1_last_5_runs_conceded")
    print(" - team2_last_5_avg_score")
    print(" - team2_last_5_runs_conceded")

    return result_df