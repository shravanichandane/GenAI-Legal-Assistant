import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import classification_report
import joblib
import os
import logging

logger = logging.getLogger(__name__)

class RiskPredictionModel:
    """
    XGBoost-based model for predicting risk levels in legal clauses.
    Module 8: Risk Intelligence Layer.
    """
    def __init__(self, model_dir='models'):
        self.model_dir = model_dir
        self.model_path = os.path.join(model_dir, 'risk_xgb_model.joblib')
        self.vectorizer_path = os.path.join(model_dir, 'tfidf_vectorizer.joblib')
        self.model = None
        self.vectorizer = None
        
        if not os.path.exists(model_dir):
            os.makedirs(model_dir, exist_ok=True)
            
        self._load_model()

    def _load_model(self):
        try:
            if os.path.exists(self.model_path) and os.path.exists(self.vectorizer_path):
                self.model = joblib.load(self.model_path)
                self.vectorizer = joblib.load(self.vectorizer_path)
                logger.info("Loaded existing Risk Prediction Model.")
        except Exception as e:
            logger.error(f"Error loading model: {e}")

    def train(self, data: pd.DataFrame, text_col: str = 'text', label_col: str = 'risk_label'):
        """
        Train the XGBoost model on historical clause data.
        """
        logger.info("Training new Risk Prediction Model...")
        self.vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
        X = self.vectorizer.fit_transform(data[text_col])
        y = data[label_col]

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        self.model = xgb.XGBClassifier(
            objective='multi:softprob',
            eval_metric='mlogloss',
            use_label_encoder=False,
            max_depth=6,
            learning_rate=0.1,
            n_estimators=100
        )
        self.model.fit(X_train, y_train)
        
        preds = self.model.predict(X_test)
        logger.info(f"Training Complete. Evaluation:\n{classification_report(y_test, preds)}")

        joblib.dump(self.model, self.model_path)
        joblib.dump(self.vectorizer, self.vectorizer_path)
        logger.info("Model saved successfully.")

    def predict_risk(self, clause_text: str):
        """
        Predict risk level for a given clause.
        Returns risk score and confidence.
        """
        if self.model is None or self.vectorizer is None:
            logger.warning("Model not trained or loaded. Returning default prediction.")
            return {"risk_level": "UNKNOWN", "confidence": 0.0}

        features = self.vectorizer.transform([clause_text])
        probabilities = self.model.predict_proba(features)[0]
        prediction = self.model.predict(features)[0]
        
        risk_levels = {0: "LOW", 1: "MEDIUM", 2: "HIGH"}
        
        return {
            "risk_level": risk_levels.get(prediction, "UNKNOWN"),
            "confidence": float(np.max(probabilities)),
            "probabilities": {risk_levels[i]: float(prob) for i, prob in enumerate(probabilities)}
        }
