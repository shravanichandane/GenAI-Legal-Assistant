import mlflow
import random

def run_experiment():
    mlflow.set_experiment("Model_Comparison")

    models = ["Legal-BERT", "Atticus RoBERTa", "DeBERTa"]

    for model in models:
        with mlflow.start_run(run_name=model):
            mlflow.log_param("model_name", model)
            
            # Mock metrics
            accuracy = random.uniform(0.85, 0.95)
            latency_ms = random.uniform(100, 300)
            memory_mb = random.uniform(500, 1500)
            
            mlflow.log_metric("Accuracy", accuracy)
            mlflow.log_metric("Latency", latency_ms)
            mlflow.log_metric("Memory Usage", memory_mb)
            
            print(f"Logged run for {model}")

if __name__ == "__main__":
    run_experiment()
