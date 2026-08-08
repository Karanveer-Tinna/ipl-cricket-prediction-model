# IPL Match Winner Prediction Using Machine Learning

## Project Overview

This project presents an end-to-end machine learning pipeline for predicting the winner of Indian Premier League (IPL) cricket matches using historical match data and engineered statistical features. The pipeline begins with converting raw YAML match files into structured datasets, followed by data cleaning, exploratory data analysis (EDA), and feature engineering to derive team, venue, and match-specific statistics.

Multiple supervised machine learning algorithms, including Logistic Regression, Support Vector Machine (SVM), Decision Tree, Random Forest, and XGBoost, are trained and evaluated using two feature configurations: one based solely on pre-match information and another incorporating the first innings score. Model performance is assessed using standard classification metrics, and the best-performing model is further interpreted using feature importance and SHAP analysis.

The project also demonstrates a complete inference workflow by generating features for unseen matches, loading the trained production model, and producing match winner predictions. A lightweight Flask-based web application is included to provide an interactive interface for making predictions using the trained model.

The objective of this project is to develop a reproducible and interpretable machine learning solution that demonstrates the complete lifecycle of a predictive analytics application, from raw data ingestion to model deployment.

## Project Structure

The project is organised into modular components to separate data processing, model development, deployment, and other resources
```
├── app/            # Flask Web Application for model inference
├── data/           # Raw, intermediate and processed datasets
├── models/         # Trained models and production artifacts
├── notebooks/      # Jupyter notebooks for the complete ML workflow
├── src/            # Reusable source code for preprocessing, feature engineering, and inference
└── README.md       # Project documentation
```
### Folder Description
- app/ – Flask application, HTML templates, CSS and static assets for the prediction dashboard.
- data/ – Stores the raw YAML files, intermediate CSV datasets, and processed datasets used for training and inference
- model/ – Contains trained machine learning models, and production-ready model artifacts.
- notebooks/ – Documents the complete workflow, including data ingestion, cleaning, exploratory data analysis, feature engineering, model training, interpretation, and inference.
- src/ – Contains reusable Python modules

## Dataset

The project uses historical Indian Premier League (IPL) match data spanning from 2008 to 2026, comprising 1,242 matches. The original dataset is provided in YAML format, with each file representing a single match and containing detailed information, such as match metadata, team lineups, innings, deliveries, and outcomes. The YAML files are present in the raw subfolder in the data folder.

During the data ingestion stage, the YAML files are parsed and converted into structured CSV dataset for analysis and model development. The project primarily utilizes two datasets:
- `match_by_match.csv` - Match-level information, including teams, venue, toss details, match result, and scores.
- `ball_by_ball.csv` - Ball-by-ball records containing delivery-level events and statistic.
These datasets are subsequently cleaned, standardized, and used to generate historical performance, venue, and team-specific features for machine learning.

## Data Pipeline

The project follows a structured end-to-end machine learning pipeline that transforms raw IPL match data into predictions through a series of modular processing stage.

```             
Raw YAML Match Files
    │
    ▼ 
Data Ingestion (YAML in `raw` → Structured CSV Datasets in `interim`)
    |
    ▼
Data Cleaning (Standardize team names, venue names, and data formats → `processed`)
    |
    ▼
Exploratory Data Analysis (EDA) (Understand data distribution and historical trends) 
    |
    ▼
Feature Engineering (Head-to-head, recent form, scoring, strategy, and venue features → `final`)
    |
    ▼
Model Training & Evaluation (Train and compare multiple machine learning models)
    |
    ▼
Model Interpretation (Feature Importance and SHAP analysis)
    |
    ▼
Inference (Generate features for unseen matches and predict the winner)
    |
    ▼
Flask Dashboard (Interative web interface for match winner prediction)
```
Each stage builds upon the previous one to ensure a reproducible workflow, with reusable preprocessing and feature engineering modules shared across the training, inference, and deployment.

Note: The `ball_by_ball` dataset is used exclusively for exploratory data analysis (EDA) to derive match-level insights and visualizations. The machine learning models are trained and evaluated solely on the `match_by_match` dataset, which also serves as the basis for match prediction.

## Feature Engineering

Historical match-level features are generated chronologically, ensuring that each match uses only information available before it was played. This prevents target leakage and keeps training features consistent with inference.

The engineered features include:

- **Head-to-head record:** total wins and wins overall and in the last three meetings between the two competing teams.
- **Recent team form:** number of wins in each team’s previous five matches.
- **Recent scoring performance:** average runs scored and conceded across the previous five matches.
- **Toss-based strategy:** historical win rates when a team chose to chase (`field`) or defend (`bat`) after winning the toss.
- **Venue context:** historical average score, chasing win rate, and each team’s win rate at the venue.

These features are added to the processed match-level dataset and saved in `data/final/match_by_match.csv` for model training and prediction.

## Model Evaluation

Models are trained using an 80/20 train-test split (`random_state=2026`). Hyperparameters are tuned with five-fold `GridSearchCV` on the training data, and the holdout set is evaluated using accuracy, ROC-AUC, precision-recall AUC, classification reports, and confusion matrices.

Logistic Regression, Decision Tree, Random Forest, Support Vector Classifier, and XGBoost models are compared for two prediction settings:

- **Pre-match (`no_score`):** uses only information available before the match. The selected XGBoost model achieved **57.38% accuracy**, **0.4972 ROC-AUC**, and **0.4468 PR-AUC**.
- **First-innings (`with_score`):** additionally includes the first-innings score. The selected XGBoost model achieved **69.26% accuracy**, **0.7508 ROC-AUC**, **0.6674 PR-AUC**, and a **0.69 macro F1-score**.

The production pipelines and their metadata are stored in `models/production/no_score/` and `models/production/with_score/`.

## Model Performance

**XGBoost** was selected as the production model for both prediction modes. The pre-match pipeline is intended for predictions before play begins, while the first-innings pipeline is the recommended option once the opening innings score is known.

| Production model | Accuracy | ROC-AUC | Macro F1 |
| --- | ---: | ---: | ---: |
| Pre-match XGBoost (`no_score`) | 57.38% | 0.4972 | 0.54 |
| First-innings XGBoost (`with_score`) | 69.26% | 0.7508 | 0.69* |

The **first-innings XGBoost pipeline** is the strongest production model, providing the best overall holdout performance and balanced class predictions.

## Model Interpretation

The production XGBoost models are interpreted in `notebooks/06_model_interpretation.ipynb` using feature importance and SHAP values:

- **Feature Importance:** ranks the inputs that contribute most to overall model predictions. In the first-innings model, `team1_score` is the strongest predictor; the pre-match model relies more on historical head-to-head, venue, and team-performance features.
- **SHAP Summary Plot:** shows the overall impact and direction of every feature across the test set, helping explain which values increase or decrease the predicted win probability.
- **SHAP Waterfall Plot:** explains an individual prediction by showing how each feature moves the model output from its baseline value to the final predicted outcome.
