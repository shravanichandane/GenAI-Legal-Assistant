import mlflow
import random

def run_experiment():
    mlflow.set_experiment("Baseline_vs_Transformer")

    models = ["TF-IDF + LR", "Legal-BERT"]

    for model in models:
        with mlflow.start_run(run_name=model):
            mlflow.log_param("model_name", model)
            
            # Mock metrics
            accuracy = random.uniform(0.7, 0.9) if model == "Legal-BERT" else random.uniform(0.6, 0.8)
            precision = accuracy - random.uniform(0.01, 0.05)
            recall = accuracy + random.uniform(0.01, 0.05)
            f1 = 2 * (precision * recall) / (precision + recall)
            
            mlflow.log_metric("Accuracy", accuracy)
            mlflow.log_metric("Precision", precision)
            mlflow.log_metric("Recall", recall)
            mlflow.log_metric("F1", f1)
            
            print(f"Logged run for {model}")

if __name__ == "__main__":
    run_experiment()
