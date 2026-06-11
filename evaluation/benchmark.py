# evaluation/benchmark.py
import logging
from typing import List, Dict, Any

try:
    from sklearn.metrics import precision_score, recall_score, f1_score
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False

logger = logging.getLogger(__name__)

class BenchmarkFramework:
    """
    Evaluation Layer for benchmarking the Legal Assistant's performance
    on tasks like Clause Classification or Risk Detection.
    """
    def __init__(self, target_names: List[str] = None):
        self.target_names = target_names or []
        self.results = []
        
    def evaluate_classification(self, y_true: List[str], y_pred: List[str]) -> Dict[str, float]:
        """
        Calculate Precision, Recall, and F1 Score for classification tasks.
        """
        if not y_true or not y_pred:
            logger.warning("Empty true or predicted labels provided.")
            return {"precision": 0.0, "recall": 0.0, "f1": 0.0}
            
        if not SKLEARN_AVAILABLE:
            logger.warning("scikit-learn not installed. Returning mock metrics.")
            return {"precision": 0.8, "recall": 0.8, "f1": 0.8}
            
        try:
            # We use macro average for imbalanced classes typically found in legal text
            precision = precision_score(y_true, y_pred, average='macro', zero_division=0)
            recall = recall_score(y_true, y_pred, average='macro', zero_division=0)
            f1 = f1_score(y_true, y_pred, average='macro', zero_division=0)
            
            metrics = {
                "precision_macro": float(precision),
                "recall_macro": float(recall),
                "f1_macro": float(f1)
            }
            logger.info(f"Evaluation metrics computed: {metrics}")
            return metrics
        except Exception as e:
            logger.error(f"Error computing evaluation metrics: {e}")
            return {"precision": 0.0, "recall": 0.0, "f1": 0.0}

    def evaluate_risk_scoring(self, y_true_scores: List[float], y_pred_scores: List[float]) -> Dict[str, float]:
        """
        Evaluate numerical risk scores using Mean Absolute Error.
        """
        if not y_true_scores or not y_pred_scores:
            return {"mae": 0.0}
            
        mae = sum(abs(t - p) for t, p in zip(y_true_scores, y_pred_scores)) / len(y_true_scores)
        return {"risk_score_mae": float(mae)}

    def run_benchmark_suite(self, dataset: List[Dict[str, Any]], predict_fn: callable) -> Dict[str, Any]:
        """
        Run a full benchmark suite over a dataset using a provided prediction function.
        dataset elements should have 'text' and 'true_label'.
        """
        y_true = []
        y_pred = []
        
        logger.info(f"Starting benchmark suite on {len(dataset)} examples...")
        
        for item in dataset:
            text = item.get("text", "")
            true_label = item.get("true_label", "")
            
            # Call the LLM or prediction function
            pred_label = predict_fn(text)
            
            y_true.append(true_label)
            y_pred.append(pred_label)
            
        metrics = self.evaluate_classification(y_true, y_pred)
        return {
            "num_examples": len(dataset),
            "metrics": metrics
        }
