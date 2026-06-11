import numpy as np
from sklearn.metrics import f1_score, precision_score, recall_score, accuracy_score
from transformers import EvalPrediction
from typing import Dict

def compute_metrics(eval_pred: EvalPrediction) -> Dict[str, float]:
    """
    Computes standard classification metrics: F1 (macro), Precision (macro),
    Recall (macro), and Accuracy.
    
    Args:
        eval_pred (EvalPrediction): An object containing predictions and labels.
        
    Returns:
        Dict[str, float]: A dictionary of the computed metrics.
    """
    predictions, labels = eval_pred
    
    # Extract the predicted classes by taking the argmax over logits
    if isinstance(predictions, tuple):
        predictions = predictions[0]
        
    preds = np.argmax(predictions, axis=-1)
    
    # Calculate metrics using 'macro' average to account for potential class imbalance
    f1 = f1_score(labels, preds, average='macro', zero_division=0)
    precision = precision_score(labels, preds, average='macro', zero_division=0)
    recall = recall_score(labels, preds, average='macro', zero_division=0)
    accuracy = accuracy_score(labels, preds)
    
    return {
        'f1': float(f1),
        'precision': float(precision),
        'recall': float(recall),
        'accuracy': float(accuracy)
    }
