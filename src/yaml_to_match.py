import os
import yaml
import pandas as pd
from tqdm import tqdm

YAML_FOLDER = r"..\dataset" 
OUTPUT_CSV = "ipl_match_by_match.csv"

match_rows = []
import os
import yaml
import pandas as pd
from tqdm import tqdm


def convert_yaml_to_match_csv(
    yaml_folder: str,
    output_csv_path: str
) -> pd.DataFrame:
    """
    Convert IPL YAML match files into a match-by-match CSV.

    This function reads all YAML files from the specified directory,
    extracts match-level metadata such as teams, venue, toss information,
    result, scores, and player lists, and saves the extracted data as a CSV.

    Parameters
    ----------
    yaml_folder : str
        Path containing YAML files.

    output_csv_path : str
        Full path where the CSV will be saved.

    Returns
    -------
    pd.DataFrame
        Match-by-match dataframe.
    """

    match_rows = []

    for file in tqdm(os.listdir(yaml_folder)):
        if file.endswith(".yaml"):
            file_path = os.path.join(yaml_folder, file)

            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    match = yaml.safe_load(f)

                match = yaml.safe_load(f)
                match_id = file.replace(".yaml", "")
                info = match.get("info", {})
                date = info.get("dates", [None])[0]
                venue = info.get("venue")
                teams = info.get("teams", [None, None])
                team1, team2 = teams[0], teams[1]

                toss = info.get("toss", {})
                toss_winner = toss.get("winner")
                toss_decision = toss.get("decision")

                outcome = info.get("outcome", {})
                winner = outcome.get("winner", None)
                result_by = outcome.get("by", {})
                result = ""
                if "runs" in result_by:
                    result = f"won by {result_by['runs']} runs"
                elif "wickets" in result_by:
                    result = f"won by {result_by['wickets']} wickets"

                players_info = info.get("players", {})
                team1_players = players_info.get(team1, [])
                team2_players = players_info.get(team2, [])

                innings = match.get("innings", [])
                first_batting_team = innings[0].get("1st innings", {}).get("team", "") if innings else ""
                second_batting_team = innings[1].get("2nd innings", {}).get("team", "") if len(innings) > 1 else ""

                def get_team_score(innings_data):
                    total = 0
                    for delivery in innings_data.get("deliveries", []):
                        for _, ball_data in delivery.items():
                            total += ball_data.get("runs", {}).get("total", 0)
                    return total

                team1_score = get_team_score(innings[0].get("1st innings", {})) if innings else 0
                team2_score = get_team_score(innings[1].get("2nd innings", {})) if len(innings) > 1 else 0

                row = {
                    "match_id": match_id,
                    "date": date,
                    "venue": venue,
                    "team1": first_batting_team,
                    "team2": second_batting_team,
                    "toss_winner": toss_winner,
                    "toss_decision": toss_decision,
                    "winner": winner,
                    "result": result,
                    "team1_score": team1_score,
                    "team2_score": team2_score,
                    "team1_players": '' + ', '.join(team1_players) + '',
                    "team2_players": '' + ', '.join(team2_players) + ''
                }

                match_rows.append(row)

            except Exception as e:
                print(f"Error in {file}: {e}")

    df = pd.DataFrame(match_rows)
    df.to_csv(output_csv_path, index=False)
    print(f"Match-by-Match CSV saved at {output_csv_path}")
    return df
