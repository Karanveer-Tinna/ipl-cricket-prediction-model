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
Data Cleaning (Standardize team names, venue names, and data formats and store in `processed`)
    |
    ▼
Exploratory Data Analysis (EDA) (Understand data distribution and historical trends) 
    |
    ▼
Feature Engineering (Head-to-head, recent form, scoring, strategy, and venue stats and store in `model_ready`)
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
