import os
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix

def generate_and_save_confusion_matrix(y_true, y_pred, labels=None, save_path="confusion_matrix.png", title="Confusion Matrix"):
    """
    Generates a confusion matrix and saves it to a file.
    """
    cm = confusion_matrix(y_true, y_pred, labels=labels)
    
    plt.figure(figsize=(10, 8))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=labels, yticklabels=labels)
    plt.xlabel('Predicted Label')
    plt.ylabel('True Label')
    plt.title(title)
    
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(os.path.abspath(save_path)), exist_ok=True)
    
    plt.savefig(save_path, bbox_inches='tight')
    plt.close()
    return cm
