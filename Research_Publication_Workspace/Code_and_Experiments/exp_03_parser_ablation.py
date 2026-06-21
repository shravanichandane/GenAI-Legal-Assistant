import mlflow
import random

def run_experiment():
    mlflow.set_experiment("Parser_Ablation")

    configurations = ["Parser + Model", "Raw + Model"]

    for config in configurations:
        with mlflow.start_run(run_name=config):
            mlflow.log_param("configuration", config)
            
            # Mock metrics
            grounding_score = random.uniform(0.8, 0.95) if "Parser" in config else random.uniform(0.6, 0.75)
            hallucination_rate = random.uniform(0.01, 0.05) if "Parser" in config else random.uniform(0.1, 0.2)
            
            mlflow.log_metric("Grounding Score", grounding_score)
            mlflow.log_metric("Hallucination Rate", hallucination_rate)
            
            print(f"Logged run for {config}")

if __name__ == "__main__":
    run_experiment()
