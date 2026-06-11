# mlops/mlflow_tracker.py
import os
import logging
from typing import Dict, Any, Optional

try:
    import mlflow
    MLFLOW_AVAILABLE = True
except ImportError:
    MLFLOW_AVAILABLE = False

logger = logging.getLogger(__name__)

class MLOpsTracker:
    """
    MLOps Tracking Layer integrating MLflow for experiment tracking
    and optionally tracking data versions via DVC concepts.
    """
    def __init__(self, experiment_name: str = "legal_assistant_experiments", tracking_uri: Optional[str] = None):
        self.experiment_name = experiment_name
        self.is_active = False
        self.run_id = None
        
        if MLFLOW_AVAILABLE:
            try:
                if tracking_uri:
                    mlflow.set_tracking_uri(tracking_uri)
                mlflow.set_experiment(experiment_name)
                self.is_active = True
                logger.info(f"MLflow initialized for experiment: {experiment_name}")
            except Exception as e:
                logger.warning(f"Failed to initialize MLflow: {e}")
        else:
            logger.warning("MLflow not installed. Tracking will be disabled or logged to console only.")

    def start_run(self, run_name: Optional[str] = None) -> None:
        """Start a new MLflow run."""
        if not self.is_active:
            return
            
        run = mlflow.start_run(run_name=run_name)
        self.run_id = run.info.run_id
        logger.info(f"Started MLflow run: {self.run_id}")

    def log_params(self, params: Dict[str, Any]) -> None:
        """Log hyperparameters or configuration."""
        if not self.is_active:
            logger.info(f"Mock Log Params: {params}")
            return
            
        mlflow.log_params(params)

    def log_metrics(self, metrics: Dict[str, float], step: Optional[int] = None) -> None:
        """Log evaluation metrics."""
        if not self.is_active:
            logger.info(f"Mock Log Metrics: {metrics}")
            return
            
        mlflow.log_metrics(metrics, step=step)

    def log_model_artifact(self, model_path: str, artifact_path: str = "models") -> None:
        """Log model files or prompts as artifacts."""
        if not self.is_active:
            logger.info(f"Mock Log Artifact: {model_path} -> {artifact_path}")
            return
            
        if os.path.exists(model_path):
            mlflow.log_artifact(model_path, artifact_path)
            
    def log_dvc_version(self, data_version: str) -> None:
        """Track DVC data version as an MLflow tag."""
        if not self.is_active:
            return
            
        mlflow.set_tag("dvc_data_version", data_version)

    def end_run(self) -> None:
        """End the current MLflow run."""
        if not self.is_active:
            return
            
        mlflow.end_run()
        self.run_id = None
        logger.info("Ended MLflow run")

# Example usage singleton
tracker = MLOpsTracker()
