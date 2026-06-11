import mlflow
import random

def run_experiment():
    mlflow.set_experiment("RAG_Ablation")

    configurations = ["FAISS-RAG", "No-RAG"]

    for config in configurations:
        with mlflow.start_run(run_name=config):
            mlflow.log_param("configuration", config)
            
            # Mock metrics
            retrieval_precision = random.uniform(0.75, 0.9) if "RAG" in config else 0.0
            retrieval_recall = random.uniform(0.8, 0.95) if "RAG" in config else 0.0
            
            mlflow.log_metric("Retrieval Precision", retrieval_precision)
            mlflow.log_metric("Retrieval Recall", retrieval_recall)
            
            print(f"Logged run for {config}")

if __name__ == "__main__":
    run_experiment()
