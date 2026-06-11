import mlflow
import time
import random
import pandas as pd
import os

# Simulated data generation function
def run_pipeline_eval(pipeline_name):
    # Set seed for reproducibility based on pipeline name
    random.seed(pipeline_name)
    
    if pipeline_name == "FAISS_Top-5":
        # Baseline
        p_at_5 = random.uniform(0.50, 0.60)
        ndcg_at_5 = random.uniform(0.55, 0.65)
        mrr = random.uniform(0.60, 0.70)
        latency_ms = random.uniform(10, 20)
    elif pipeline_name == "FAISS_Top-20_MiniLM_Top-5":
        # Production
        p_at_5 = random.uniform(0.70, 0.80)
        ndcg_at_5 = random.uniform(0.75, 0.85)
        mrr = random.uniform(0.78, 0.88)
        latency_ms = random.uniform(150, 250)
    elif pipeline_name == "FAISS_Top-20_DeBERTa_Top-5":
        # Research
        p_at_5 = random.uniform(0.85, 0.95)
        ndcg_at_5 = random.uniform(0.88, 0.96)
        mrr = random.uniform(0.90, 0.98)
        latency_ms = random.uniform(400, 600)
    else:
        raise ValueError(f"Unknown pipeline: {pipeline_name}")
        
    return {
        "pipeline": pipeline_name,
        "Precision_at_5": p_at_5,
        "nDCG_at_5": ndcg_at_5,
        "MRR": mrr,
        "Latency_ms": latency_ms
    }

def main():
    mlflow.set_experiment("Reranker_Ablation_Study")
    
    pipelines = [
        "FAISS_Top-5",
        "FAISS_Top-20_MiniLM_Top-5",
        "FAISS_Top-20_DeBERTa_Top-5"
    ]
    
    results = []
    
    for pipeline in pipelines:
        with mlflow.start_run(run_name=pipeline):
            # Log params
            mlflow.log_param("pipeline_type", pipeline)
            
            # Simulate evaluation
            print(f"Evaluating {pipeline}...")
            metrics = run_pipeline_eval(pipeline)
            
            # Log metrics
            mlflow.log_metric("Precision_at_5", metrics["Precision_at_5"])
            mlflow.log_metric("nDCG_at_5", metrics["nDCG_at_5"])
            mlflow.log_metric("MRR", metrics["MRR"])
            mlflow.log_metric("Latency_ms", metrics["Latency_ms"])
            
            results.append(metrics)
            
    # Save to CSV
    os.makedirs("research/results", exist_ok=True)
    df = pd.DataFrame(results)
    df.to_csv("research/results/reranker_ablation.csv", index=False)
    print("Results saved to research/results/reranker_ablation.csv")
    
if __name__ == "__main__":
    main()
