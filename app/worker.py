import os
import time
import logging
from celery import Celery

# Configure basic logging for the worker
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger(__name__)

# Retrieve Redis broker URL from environment, default to localhost for development
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

# Initialize Celery App
celery_app = Celery(
    "legalsight_worker",
    broker=REDIS_URL,
    backend=REDIS_URL
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    worker_prefetch_multiplier=1, # Fair distribution for long-running tasks
)

@celery_app.task(bind=True, name="process_contract_task")
def process_contract_task(self, contract_id: str, file_path: str):
    """
    Dummy Celery task that simulates the contract processing pipeline.
    Pipeline stages:
    1. Parsing
    2. Classification
    3. Embedding & Retrieval preparation
    4. RAG indexing
    """
    logger.info(f"Starting processing for contract ID: {contract_id} at {file_path}")
    
    try:
        # Simulate Parsing
        logger.info(f"[{contract_id}] Stage 1: Parsing document...")
        time.sleep(2) # Simulate work
        
        # Simulate Classification
        logger.info(f"[{contract_id}] Stage 2: Classifying document type and clauses...")
        time.sleep(1.5)
        
        # Simulate Retrieval/Embedding
        logger.info(f"[{contract_id}] Stage 3: Generating embeddings for vector store...")
        time.sleep(2.5)
        
        # Simulate RAG indexing
        logger.info(f"[{contract_id}] Stage 4: Indexing in RAG database...")
        time.sleep(1)
        
        logger.info(f"Completed processing for contract ID: {contract_id}")
        return {"status": "success", "contract_id": contract_id, "message": "Pipeline completed successfully."}
        
    except Exception as e:
        logger.error(f"Error processing contract ID {contract_id}: {str(e)}")
        # Allow retry on failure
        raise self.retry(exc=e, countdown=60, max_retries=3)
