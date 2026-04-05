import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
import joblib


df = pd.read_csv('heart.csv')

X = df.drop('target', axis=1)
y = df.target


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)


scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)


model = RandomForestClassifier(random_state=42)


param_grid = {
	'n_estimators': [100, 200],
	'max_depth': [10, 20, None],
	'min_samples_split': [2, 5],
	'min_samples_leaf': [1, 2],
	'max_features': ['sqrt', 'log2']
}
grid_search = GridSearchCV(
	estimator = model,
	param_grid = param_grid,
	cv = 5,
	scoring = 'accuracy',
	n_jobs = -1,
	verbose = 1
)
grid_search.fit(X_train_scaled, y_train)


best_model = grid_search.best_estimator_
best_params = grid_search.best_params_
best_cv_score = grid_search.best_score_


joblib.dump(grid_search.best_estimator_, "health_risk_predictor.pkl")
joblib.dump(scaler, "health_features_scaler.pkl")

feature_names = X.columns.tolist()
metadata = {
    'feature_names': feature_names,
    'best_params': best_params,
    'cv_accuracy': float(best_cv_score),
    'n_features': len(feature_names)
}

with open('model_metadata.json', 'w') as f:
    json.dump(metadata, f, indent=4)