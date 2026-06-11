import argparse
import logging
from typing import Tuple

import torch
from transformers import (
    BertForSequenceClassification,
    BertTokenizerFast,
    Trainer,
    TrainingArguments,
    set_seed
)

from dataset import LegalDataset
from metrics import compute_metrics

# Configure basic logging
logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
    datefmt='%m/%d/%Y %H:%M:%S',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def prepare_dummy_data(tokenizer: BertTokenizerFast) -> Tuple[LegalDataset, LegalDataset]:
    """
    Prepares a small dummy dataset for testing the pipeline.
    In a production scenario, replace this with actual logic to parse and tokenize CUAD data.
    """
    texts = [
        "The governing law of this agreement shall be the laws of the State of New York.",
        "Either party may terminate this Agreement upon thirty (30) days written notice.",
        "Confidential information shall not be disclosed to any third party.",
        "This contract represents the entire agreement between the parties."
    ]
    # For dummy purposes, we assign arbitrary labels (e.g., 0: Governing Law, 1: Termination, etc.)
    labels = [0, 1, 0, 1]

    encodings = tokenizer(texts, truncation=True, padding=True, max_length=128)
    
    # Split into train and eval sets for demonstration
    train_dataset = LegalDataset(encodings, labels)
    eval_dataset = LegalDataset(encodings, labels)
    
    return train_dataset, eval_dataset


def main():
    parser = argparse.ArgumentParser(description="Phase 2 Fine-Tuning: Legal-BERT for Sequence Classification")
    parser.add_argument("--output_dir", type=str, default="./results", help="Directory to save the fine-tuned model")
    parser.add_argument("--num_labels", type=int, default=2, help="Number of classification categories")
    parser.add_argument("--seed", type=int, default=42, help="Random seed for reproducibility")
    args = parser.parse_args()

    # Set random seed for deterministic training
    set_seed(args.seed)

    model_name = "nlpaueb/legal-bert-base-uncased"
    logger.info(f"Initializing Tokenizer and Model: {model_name}")

    # Load tokenizer and pre-trained Legal-BERT model for classification
    tokenizer = BertTokenizerFast.from_pretrained(model_name)
    model = BertForSequenceClassification.from_pretrained(
        model_name,
        num_labels=args.num_labels
    )

    logger.info("Preparing datasets...")
    # NOTE: Replace `prepare_dummy_data` with actual CUAD data ingestion pipeline
    train_dataset, eval_dataset = prepare_dummy_data(tokenizer)

    logger.info("Configuring Training Arguments...")
    # Training configuration adhering to target specifications
    training_args = TrainingArguments(
        output_dir=args.output_dir,
        num_train_epochs=1,                     # Specified in requirements
        per_device_train_batch_size=8,          # Specified in requirements
        per_device_eval_batch_size=8,
        learning_rate=2e-5,                     # Specified in requirements
        evaluation_strategy="epoch",
        save_strategy="epoch",
        logging_dir="./logs",
        logging_steps=10,
        load_best_model_at_end=True,
        metric_for_best_model="f1",
        weight_decay=0.01,
        report_to="none"                        # Disable third-party loggers (like wandb) by default
    )

    logger.info("Initializing HuggingFace Trainer...")
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=eval_dataset,
        compute_metrics=compute_metrics,
    )

    logger.info("Starting Fine-Tuning Process...")
    trainer.train()

    logger.info(f"Saving final model artifacts to {args.output_dir}...")
    trainer.save_model(args.output_dir)
    tokenizer.save_pretrained(args.output_dir)
    
    logger.info("Fine-tuning completed successfully.")

if __name__ == "__main__":
    main()
