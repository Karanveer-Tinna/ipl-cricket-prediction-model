from flask import Flask, render_template
from pathlib import Path
import joblib
import pandas as pd

app = Flask(__name__)

PROJECT_ROOT = Path(__file__).resolve().parent.parent

MODEL_DIR = PROJECT_ROOT / "models" / "production"
DATA_DIR = PROJECT_ROOT / "data" / "processed"

model = joblib.load(MODEL_DIR / "no_score" / "best_model.pkl")
feature_columns = joblib.load(PROJECT_ROOT / "data" / "splits" / "no_score" / "X_test.pkl").columns.tolist()

historical_matches = pd.read_csv(DATA_DIR / "match_by_match.csv")

teams = sorted(pd.unique(pd.concat([historical_matches["team1"], historical_matches["team2"]])))
venues = sorted(historical_matches["venue"].unique())

@app.route("/")
def home():

   return render_template("index.html", teams = teams, venues = venues) 