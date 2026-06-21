import mlflow
import random

def run_experiment():
    mlflow.set_experiment("Dataset_Size_Scaling")

    dataset_sizes = [1000, 3000, 5000]

    for size in dataset_sizes:
        with mlflow.start_run(run_name=f"Size_{size}"):
            mlflow.log_param("dataset_size", size)
            
            # Mock metrics
            accuracy = min(1.0, 0.7 + (size / 10000.0) + random.uniform(-0.02, 0.02))
            f1 = accuracy - random.uniform(0.01, 0.03)
            training_time_secs = size * random.uniform(0.5, 0.8)
            
            mlflow.log_metric("Accuracy", accuracy)
            mlflow.log_metric("F1", f1)
            mlflow.log_metric("Training Time", training_time_secs)
            
            print(f"Logged run for dataset size {size}")

if __name__ == "__main__":
    run_experiment()
