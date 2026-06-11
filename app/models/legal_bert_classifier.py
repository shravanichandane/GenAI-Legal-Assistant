import logging
from typing import Tuple
from transformers import pipeline

logger = logging.getLogger(__name__)

class LegalBertClassifier:
    """
    Phase 1 Legal-BERT Inference Pipeline.
    
    NOTE: For the MVP, since `nlpaueb/legal-bert-base-uncased` is not natively a zero-shot NLI model,
    we are using `facebook/bart-large-mnli` as a stand-in to simulate the behavior. 
    This class will be updated to use the fine-tuned Legal-BERT model in Phase 2.
    """
    
    def __init__(self):
        try:
            logger.info("Initializing LegalBertClassifier (using typeform/distilbert-base-uncased-mnli for ultra-fast load)...")
            self.classifier = pipeline("zero-shot-classification", model="typeform/distilbert-base-uncased-mnli")
            self.labels = [
                "LIABILITY", 
                "INDEMNITY", 
                "TERMINATION", 
                "PAYMENT", 
                "CONFIDENTIALITY", 
                "INTELLECTUAL_PROPERTY", 
                "GENERAL"
            ]
            logger.info("LegalBertClassifier initialized successfully.")
        except Exception as e:
            logger.error(f"Failed to initialize zero-shot pipeline: {e}")
            self.classifier = None
            self.labels = []

    def predict(self, text: str) -> Tuple[str, float]:
        """
        Predicts the clause type for the given text.
        Returns a tuple of (predicted_label, confidence_score).
        """
        if not self.classifier:
            logger.warning("Classifier is not loaded. Returning fallback.")
            return "GENERAL", 0.0
            
        if not text or not text.strip():
            return "GENERAL", 0.0
            
        try:
            result = self.classifier(text, candidate_labels=self.labels)
            predicted_label = result['labels'][0]
            confidence = result['scores'][0]
            
            return predicted_label, confidence
        except Exception as e:
            logger.error(f"Prediction failed: {e}")
            return "GENERAL", 0.0
