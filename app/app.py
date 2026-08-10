from flask import Flask, render_template, request
from pathlib import Path
import joblib
import pandas as pd
from src.features import add_head_to_head_features, add_team_form_features, add_team_scoring_features, add_team_strategy_features, add_venue_features

app = Flask(__name__)

PROJECT_ROOT = Path(__file__).resolve().parent.parent

MODEL_DIR = PROJECT_ROOT / "models" / "production"
DATA_DIR = PROJECT_ROOT / "data" / "processed"

no_score_model = joblib.load(MODEL_DIR / "no_score" / "best_model.pkl")
with_score_model = joblib.load(MODEL_DIR / "with_score" / "best_model.pkl")
no_score_feature_columns = joblib.load(PROJECT_ROOT / "data" / "splits" / "no_score" / "X_test.pkl").columns.tolist()
with_score_feature_columns = joblib.load(PROJECT_ROOT / "data" / "splits" / "with_score" / "X_test.pkl").columns.tolist()

historical_matches = pd.read_csv(DATA_DIR / "match_by_match.csv")

teams = sorted(pd.unique(pd.concat([historical_matches["team1"], historical_matches["team2"]]).dropna()))
venues = sorted(historical_matches["venue"].unique())

@app.route("/")
def home():
   return render_template("index.html", teams = teams, venues = venues) 

@app.route("/predict", methods=["POST"])
def predict():

   team1 = request.form["team1"]
   team2 = request.form["team2"]
   venue = request.form["venue"]
   toss_winner = request.form["toss_winner"]
   toss_decision = request.form["toss_decision"]
   team1_score = request.form.get("team1_score")

   new_match = {
      "match_id": -1,
      "date": pd.Timestamp.today().date(),
      "venue": venue,
      "team1": team1,
      "team2": team2,
      "toss_winner": toss_winner,
      "toss_decision": toss_decision,
      "winner":None,
      "result":None,
      "team1_score": float(team1_score) if team1_score else None,
      "team2_score": None,
      "team1_players": None,
      "team2_players": None
   }

   combined = pd.concat([historical_matches, pd.DataFrame([new_match])], ignore_index=True)
   combined["date"] = pd.to_datetime(combined["date"])

   combined["toss_winner_slot"] = (combined["toss_winner"] == combined["team1"]).astype(int)

   combined = add_head_to_head_features(combined)
   combined = add_team_form_features(combined)
   combined = add_team_scoring_features(combined)
   combined = add_team_strategy_features(combined)
   combined = add_venue_features(combined)

   if team1_score:
      model = with_score_model
      feature_columns = with_score_feature_columns
   else:
      model = no_score_model
      feature_columns = no_score_feature_columns

   X = combined.iloc[[-1]][feature_columns]

   prediction =  model.predict(X)[0]
   probability = model.predict_proba(X)[0]

   if prediction == 1:
      prediction_winner = team1
   else:
      prediction_winner = team2

   class_probabilities = dict(zip(model.classes_, probability))
   team1_probability = class_probabilities[1] * 100
   team2_probability = class_probabilities[0] * 100

   return render_template("result.html", winner=prediction_winner, team1=team1, team2=team2, 
                          team1_probability = round(team1_probability, 2), team2_probability = round(team2_probability, 2))


if __name__ == "__main__":
   app.run(debug=True)
