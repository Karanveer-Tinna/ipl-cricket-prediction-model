# IPL Match Winner Prediction Using Machine Learning

## Project Overview

This project presents an end-to-end machine learning pipeline for predicting the winner of Indian Premier League (IPL) cricket matches using historical match data and engineered statistical features. The pipeline begins with converting raw YAML match files into structured datasets, followed by data cleaning, exploratory data analysis (EDA), and feature engineering to derive team, venue, and match-specific statistics.

Multiple supervised machine learning algorithms, including Logistic Regression, Support Vector Machine (SVM), Decision Tree, Random Forest, and XGBoost, are trained and evaluated using two feature configurations: one based solely on pre-match information and another incorporating the first innings score. Model performance is assessed using standard classification metrics, and the best-performing model is further interpreted using feature importance and SHAP analysis.

The project also demonstrates a complete inference workflow by generating features for unseen matches, loading the trained production model, and producing match winner predictions. A lightweight Flask-based web application is included to provide an interactive interface for making predictions using the trained model.

The objective of this project is to develop a reproducible and interpretable machine learning solution that demonstrates the complete lifecycle of a predictive analytics application, from raw data ingestion to model deployment.

## Project Structure

The project is organised into modular components to separate data processing, model development, deployment, and other resources

├── app/
├── data/
├── models/
├── notebooks/
├── src/
└── README.md

### Folder Description
- app/ – Flask application, HTML templates, CSS and static assets for the prediction dashboard.
- data/ – Stores the raw YAML files, intermediate CSV datasets, and processed datasets used for training and inference
- model/ – Contains trained machine learning models, and production-ready model artifacts.
- notebooks/ – Documents the complete workflow, including data ingestion, cleaning, exploratory data analysis, feature engineering, model training, interpretation, and inference.
- src/ – Contains reusable Python modules

## Dataset

The project uses historical Indian Premier League (IPL) match data spanning from 2008 to 2026, comprising 1,242 matches. The original dataset is provided in YAML format, with each file representing a single match and containing detailed information, such as match metadata, team lineups, innings, deliveries, and outcomes. The YAML files are present in the raw subfolder in the data folder.

During the data ingestion stage, the YAML files are parsed and converted into structured CSV dataset for analysis and model development.