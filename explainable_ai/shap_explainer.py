import shap
import numpy as np
import logging

logger = logging.getLogger(__name__)

class ClauseExplainer:
    """
    SHAP/LIME Feature Attribution and Explainability.
    Module 9: Explainable AI Layer.
    """
    def __init__(self, risk_model):
        """
        Initialize with a trained RiskPredictionModel instance.
        """
        self.risk_model = risk_model
        self.explainer = None
        self._initialize_explainer()

    def _initialize_explainer(self):
        if self.risk_model.model and self.risk_model.vectorizer:
            try:
                # Using TreeExplainer for XGBoost
                self.explainer = shap.TreeExplainer(self.risk_model.model)
                logger.info("SHAP Explainer initialized successfully.")
            except Exception as e:
                logger.error(f"Failed to initialize SHAP Explainer: {e}")
        else:
            logger.warning("Risk model not fully loaded. Cannot initialize Explainer.")

    def explain_prediction(self, clause_text: str):
        """
        Generate feature attributions for a given clause prediction.
        """
        if not self.explainer or not self.risk_model.vectorizer:
            return {"error": "Explainer not initialized."}

        # Transform text to features
        features = self.risk_model.vectorizer.transform([clause_text]).toarray()
        
        # Calculate SHAP values
        shap_values = self.explainer.shap_values(features)
        
        # Depending on XGBoost objective, shap_values might be a list (multiclass) or array
        if isinstance(shap_values, list):
            # Take the SHAP values for the predicted class
            pred_class = self.risk_model.model.predict(features)[0]
            class_shap_values = shap_values[pred_class][0]
        else:
            class_shap_values = shap_values[0]

        # Map features back to words
        feature_names = self.risk_model.vectorizer.get_feature_names_out()
        
        # Get top contributing words
        word_contributions = []
        for idx, shap_val in enumerate(class_shap_values):
            if shap_val != 0:
                word_contributions.append({
                    "word": feature_names[idx],
                    "contribution": float(shap_val)
                })
                
        # Sort by absolute contribution descending
        word_contributions.sort(key=lambda x: abs(x["contribution"]), reverse=True)
        
        return {
            "top_features": word_contributions[:10],
            "explanation_summary": f"Identified {len(word_contributions)} key terms influencing the risk score."
        }
