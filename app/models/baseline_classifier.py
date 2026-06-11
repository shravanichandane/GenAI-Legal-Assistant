"""
Baseline Clause Classifier
==========================

This is the Tier 0 baseline NLP model. It demonstrates the fundamental
pipeline of text classification:

    Raw Text → Preprocessing → TF-IDF Vectorization → Logistic Regression

By building this baseline first, you have a benchmark to compare
against Legal-BERT in Tier 1. If Legal-BERT only achieves 85% accuracy
while this baseline achieves 84%, the complexity of BERT might not
be justified!
"""

import pickle
import os
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, accuracy_score, f1_score
from typing import List, Tuple, Dict, Any

# Define the models directory for saving/loading
MODELS_DIR = Path(__file__).resolve().parent
MODEL_PATH = MODELS_DIR / "baseline_model.pkl"

class BaselineClauseClassifier:
    """
    A simple TF-IDF + Logistic Regression classifier for legal clauses.
    
    This handles:
    1. Tokenization (splitting text into words)
    2. Embeddings (TF-IDF: converting words to numbers based on importance)
    3. Classification (Logistic Regression: learning boundary lines between classes)
    """

    def __init__(self):
        # We use a scikit-learn Pipeline. This ensures that the exact same
        # tokenization and TF-IDF scaling applied during training is also
        # applied during prediction.
        self.pipeline = Pipeline([
            # 1. TF-IDF Vectorizer:
            # - stop_words="english": removes common words like "the", "and"
            # - ngram_range=(1,2): considers single words AND 2-word phrases
            #   (e.g., "force majeure" or "hold harmless")
            ('tfidf', TfidfVectorizer(stop_words='english', ngram_range=(1, 2))),
            
            # 2. Logistic Regression:
            # - class_weight="balanced": handles imbalanced legal datasets
            #   (e.g., if you have 100 GENERAL clauses and only 5 INDEMNITY clauses)
            ('clf', LogisticRegression(class_weight='balanced', random_state=42))
        ])
        
        self.is_trained = False
        self.classes_ = []

    def train(self, X_train: List[str], y_train: List[str]):
        """
        Train the baseline model.
        
        Args:
            X_train: List of clause text strings.
            y_train: List of clause type labels (e.g., 'INDEMNITY', 'GENERAL').
        """
        if not X_train or not y_train:
            raise ValueError("Training data cannot be empty.")
            
        print(f"Training Baseline Classifier on {len(X_train)} samples...")
        self.pipeline.fit(X_train, y_train)
        
        self.classes_ = list(self.pipeline.classes_)
        self.is_trained = True
        print(f"Trained successfully! Classes: {self.classes_}")

    def evaluate(self, X_test: List[str], y_test: List[str]) -> Dict[str, Any]:
        """
        Evaluate the model on a test set.
        
        Returns:
            A dictionary containing accuracy, f1_score, and the full classification report.
        """
        if not self.is_trained:
            raise RuntimeError("Model must be trained before evaluation.")
            
        y_pred = self.pipeline.predict(X_test)
        
        # Calculate metrics
        acc = accuracy_score(y_test, y_pred)
        f1_macro = f1_score(y_test, y_pred, average='macro')
        report = classification_report(y_test, y_pred)
        
        print("\n--- Evaluation Results ---")
        print(f"Accuracy: {acc:.4f}")
        print(f"Macro F1-Score: {f1_macro:.4f}")
        print("\nClassification Report:")
        print(report)
        
        return {
            "accuracy": acc,
            "f1_macro": f1_macro,
            "report": report
        }

    def predict(self, text: str) -> Tuple[str, float]:
        """
        Predict the clause type and confidence score for a single string of text.
        
        Returns:
            Tuple of (predicted_class, confidence_score)
        """
        if not self.is_trained:
            raise RuntimeError("Model must be trained before predicting.")
            
        # The pipeline automatically handles TF-IDF vectorization
        pred_class = self.pipeline.predict([text])[0]
        
        # Get probability/confidence
        probs = self.pipeline.predict_proba([text])[0]
        class_idx = list(self.pipeline.classes_).index(pred_class)
        confidence = probs[class_idx]
        
        return pred_class, float(confidence)

    def save_model(self, filepath: str = str(MODEL_PATH)):
        """Save the trained pipeline to disk."""
        if not self.is_trained:
            raise RuntimeError("Cannot save an untrained model.")
            
        with open(filepath, 'wb') as f:
            pickle.dump({
                "pipeline": self.pipeline,
                "classes": self.classes_
            }, f)
        print(f"Model saved to {filepath}")

    def load_model(self, filepath: str = str(MODEL_PATH)):
        """Load a trained pipeline from disk."""
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Model file not found at {filepath}")
            
        with open(filepath, 'rb') as f:
            data = pickle.load(f)
            self.pipeline = data["pipeline"]
            self.classes_ = data["classes"]
            self.is_trained = True
        print(f"Model loaded from {filepath}")

