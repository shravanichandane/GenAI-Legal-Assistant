import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc
import os

def plot_roc_curve(y_true, y_scores, save_path="roc_curve.png", title="Receiver Operating Characteristic"):
    """
    Plots the ROC curve for a given set of true labels and prediction scores.
    
    Args:
        y_true (array-like): True binary labels.
        y_scores (array-like): Target scores, can either be probability estimates of the positive class.
        save_path (str): Path to save the plot.
        title (str): Title of the plot.
    """
    fpr, tpr, _ = roc_curve(y_true, y_scores)
    roc_auc = auc(fpr, tpr)
    
    plt.figure(figsize=(8, 8))
    plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (area = {roc_auc:.2f})')
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title(title)
    plt.legend(loc="lower right")
    
    os.makedirs(os.path.dirname(os.path.abspath(save_path)), exist_ok=True)
    plt.savefig(save_path, bbox_inches='tight')
    plt.close()

def plot_multiple_roc_curves(mlflow_run_data, save_path="multiple_roc_curves.png", title="ROC Curves across MLflow Runs"):
    """
    Plots multiple ROC curves from different MLflow runs.
    
    Args:
        mlflow_run_data (list of dicts): [{'run_name': 'Model A', 'y_true': [...], 'y_scores': [...]}, ...]
        save_path (str): Path to save the plot.
        title (str): Title of the plot.
    """
    plt.figure(figsize=(10, 8))
    
    for data in mlflow_run_data:
        run_name = data.get('run_name', 'Unknown Run')
        y_true = data.get('y_true', [])
        y_scores = data.get('y_scores', [])
        
        if len(y_true) > 0 and len(y_scores) > 0:
            fpr, tpr, _ = roc_curve(y_true, y_scores)
            roc_auc = auc(fpr, tpr)
            plt.plot(fpr, tpr, lw=2, label=f'{run_name} (AUC = {roc_auc:.2f})')
            
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title(title)
    plt.legend(loc="lower right")
    
    os.makedirs(os.path.dirname(os.path.abspath(save_path)), exist_ok=True)
    plt.savefig(save_path, bbox_inches='tight')
    plt.close()
