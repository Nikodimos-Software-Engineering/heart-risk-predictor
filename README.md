# Heart Disease Risk Predictor

An interactive web application that predicts heart disease risk using machine learning. Enter your health metrics and get an instant risk assessment with explainable AI (SHAP).

## Features

- **Risk Prediction** – Real-time classification using a trained Random Forest model
- **Interactive UI** – Built with Streamlit; input 13 clinical features via sliders and dropdowns
- **Model Explainability** – SHAP waterfall plots show which factors influence your risk
- **Trained Model** – GridSearchCV-optimized Random Forest with ~98.5% cross-validation accuracy

## Dataset

Uses the [Cleveland Heart Disease](https://archive.ics.uci.edu/ml/datasets/heart+Disease) database. The target variable indicates presence of coronary artery disease (>50% diameter narrowing in at least one major vessel). See [Description.md](Description.md) for full feature details.

## Installation

```bash
git clone <repo-url>
cd heart-risk-predictor
pip install -r requirements.txt
```

## Usage

### Run the web app

```bash
streamlit run main.py
```

### Retrain the model

```bash
python train_model.py
```

This runs grid search over Random Forest hyperparameters, saves the best model as `health_risk_predictor.pkl`, the scaler as `health_features_scaler.pkl`, and metadata as `model_metadata.json`.

## Project Structure

```
├── main.py                    # Streamlit web application
├── train_model.py             # Model training pipeline
├── heart.csv                  # Cleveland Heart Disease dataset
├── requirements.txt           # Python dependencies
├── Description.md             # Feature descriptions and clinical insights
├── model_metadata.json        # Best hyperparameters and CV score
├── health_risk_predictor.pkl  # Trained Random Forest model
└── health_features_scaler.pkl # StandardScaler fitted on training data
```

## Dependencies

streamlit, scikit-learn, pandas, numpy, shap, matplotlib, joblib

## Disclaimer

This tool is for **educational purposes only**. Not a substitute for professional medical advice.
