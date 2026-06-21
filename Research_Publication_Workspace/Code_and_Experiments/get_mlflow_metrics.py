import mlflow
import pandas as pd
import json

def analyze_mlflow_runs():
    try:
        # Get tracking URI
        tracking_uri = mlflow.get_tracking_uri()
        print(f"Tracking URI: {tracking_uri}")
        
        # Get all experiments
        experiments = mlflow.search_experiments()
        print(f"Found {len(experiments)} experiments")
        
        results = {}
        for exp in experiments:
            print(f"Experiment: {exp.name} (ID: {exp.experiment_id})")
            
            # Get all runs for this experiment
            runs = mlflow.search_runs(experiment_ids=[exp.experiment_id])
            
            if len(runs) == 0:
                print("  No runs found.")
                continue
                
            print(f"  Found {len(runs)} runs.")
            
            # Print column names to help us see what metrics are available
            print(f"  Columns: {list(runs.columns)}")
            
            # Print a summary of metrics
            metric_cols = [c for c in runs.columns if c.startswith('metrics.')]
            param_cols = [c for c in runs.columns if c.startswith('params.')]
            
            for index, row in runs.iterrows():
                run_id = row['run_id']
                print(f"  Run ID: {run_id}")
                for col in metric_cols + param_cols:
                    if pd.notna(row[col]):
                        print(f"    {col}: {row[col]}")
            print("-" * 50)
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    analyze_mlflow_runs()
