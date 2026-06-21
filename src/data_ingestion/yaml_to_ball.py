import os
import yaml
import pandas as pd
from tqdm import tqdm

def convert_yaml_to_ball_csv(
    yaml_folder: str,
    output_csv_path: str
) -> pd.DataFrame:
    """
    Convert IPL YAML match files into a ball-by-ball CSV.

    This function reads all YAML files from the specified directory,
    extracts delivery-level information such as innings, batting team,
    bowling team, batsman, over number, ball number, and runs scored,
    and saves the extracted data as a CSV.

    Parameters
    ----------
    yaml_folder : str
        Path containing YAML files.

    output_csv_path : str
        Full path where the CSV will be saved.

    Returns
    -------
    pd.DataFrame
        Ball-by-ball dataframe.
    """

    ball_rows = []
    match_teams = {}

    for file in tqdm(os.listdir(yaml_folder)):
        if file.endswith(".yaml"):
            file_path = os.path.join(yaml_folder, file)

            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    match = yaml.safe_load(f)

                match_id = file.replace(".yaml", "")

                # Store team information
                teams = match.get("info", {}).get("teams", ["", ""])
                if len(teams) == 2:
                    match_teams[match_id] = (teams[0], teams[1])
                else:
                    match_teams[match_id] = ("", "")

                innings = match.get("innings", [])

                for inning in innings:
                    for inning_name, inning_data in inning.items():
                        batting_team = inning_data.get("team", "")
                        deliveries = inning_data.get("deliveries", [])

                        for delivery in deliveries:
                            for ball, info in delivery.items():
                                over, ball_number = map(
                                    int, str(ball).split(".")
                                )

                                team1, team2 = match_teams[match_id]

                                if batting_team == team1:
                                    bowling_team = team2
                                else:
                                    bowling_team = team1

                                row = {
                                    "match_id": match_id,
                                    "inning": inning_name,
                                    "batting_team": batting_team,
                                    "bowling_team": bowling_team,
                                    "over": over,
                                    "ball": ball_number,
                                    "batsman": info.get("batsman", ""),
                                    "bowler": info.get("bowler", ""),
                                    "non_striker": info.get(
                                        "non_striker", ""
                                    ),
                                    "runs_batsman": info.get(
                                        "runs", {}
                                    ).get("batsman", 0),
                                    "runs_total": info.get(
                                        "runs", {}
                                    ).get("total", 0),
                                }

                                ball_rows.append(row)

            except Exception as e:
                print(f"Error in {file}: {e}")

    df = pd.DataFrame(ball_rows)
    df.to_csv(output_csv_path, index=False)

    print(f"Ball-by-Ball CSV saved at {output_csv_path}")

    return df
