import matplotlib.pyplot as plt
import seaborn as sns
import os

def plot_f1_score_over_runs(mlflow_data, save_path="f1_scores.png", title="F1 Score across MLflow Runs"):
    """
    Plots F1 scores over different MLflow runs.
    
    Args:
        mlflow_data (list or dict): Data containing run names/IDs and their F1 scores.
                                    Assuming a format like [{'run_name': 'A', 'f1': 0.8}, ...]
        save_path (str): Path to save the plot.
        title (str): Title of the plot.
    """
    if not mlflow_data:
        print("No data provided for F1 chart.")
        return
        
    run_names = [d.get('run_name', f"Run {i}") for i, d in enumerate(mlflow_data)]
    f1_scores = [d.get('f1', 0.0) for d in mlflow_data]
    
    plt.figure(figsize=(10, 6))
    sns.barplot(x=run_names, y=f1_scores, palette="viridis")
    plt.ylim(0, 1.1)
    plt.xlabel('Run Name')
    plt.ylabel('F1 Score')
    plt.title(title)
    plt.xticks(rotation=45, ha='right')
    
    os.makedirs(os.path.dirname(os.path.abspath(save_path)), exist_ok=True)
    plt.savefig(save_path, bbox_inches='tight')
    plt.close()
