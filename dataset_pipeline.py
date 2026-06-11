import pandas as pd
from sklearn.model_selection import train_test_split
import os

class LegalDatasetPipeline:
    def __init__(self, output_dir="data/processed"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def normalize_cuad(self, raw_data_path):
        """
        Mock function to demonstrate how we would ingest CUAD data.
        In reality, this would parse the complex SQuAD-style JSON of CUAD.
        """
        # Imagine we parse JSON into a list of dictionaries
        data = [
            {"text": "The Contractor shall indemnify the Client...", "label": "Indemnification"},
            {"text": "This Agreement shall terminate on...", "label": "Termination"},
        ]
        return pd.DataFrame(data)

    def process_and_save(self, df, dataset_name):
        """
        Splits the dataframe into Train/Val/Test and saves as Parquet.
        """
        # Split: 80% Train, 20% Temp (which becomes 10% Val / 10% Test)
        train_df, temp_df = train_test_split(df, test_size=0.2, random_state=42, stratify=df['label'])
        val_df, test_df = train_test_split(temp_df, test_size=0.5, random_state=42, stratify=temp_df['label'])

        # Save using PyArrow engine for Parquet
        train_df.to_parquet(f"{self.output_dir}/{dataset_name}_train.parquet")
        val_df.to_parquet(f"{self.output_dir}/{dataset_name}_val.parquet")
        test_df.to_parquet(f"{self.output_dir}/{dataset_name}_test.parquet")
        
        print(f"✅ Successfully processed {dataset_name}.")
        print(f"Train: {len(train_df)}, Val: {len(val_df)}, Test: {len(test_df)}")

if __name__ == "__main__":
    pipeline = LegalDatasetPipeline()
    # 1. Ingest
    cuad_df = pipeline.normalize_cuad("data/raw/cuad.json")
    # 2. Process and Save
    pipeline.process_and_save(cuad_df, "cuad")
