"""
Utility script to generate a sample of the CUAD (Contract Understanding Atticus Dataset)
format locally so you can inspect its structure before training.
"""
import os
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    logger.info("Generating CUAD dataset sample...")
    
    # Note: The official 'cuad' HuggingFace loader was deprecated in datasets>=2.20
    # because it uses a legacy python script instead of modern Parquet format.
    # To avoid manually downloading the 500MB ZIP file for a simple preview,
    # we will generate a local sample file that perfectly mimics the CUAD SQuAD 2.0 format.
    
    samples = [
        {
            "id": "cuad_sample_001",
            "title": "ACME_CORP_MASTER_SERVICES_AGREEMENT",
            "context_snippet": "This Master Services Agreement (the \"Agreement\") is entered into as of January 1, 2023, by and between ACME Corp, a Delaware corporation (\"Client\"), and TechSolutions Inc., a California corporation (\"Vendor\")... 8. INDEMNIFICATION. Vendor agrees to indemnify, defend, and hold harmless Client from any claims arising out of Vendor's gross negligence.",
            "question": "Highlight the parts (if any) of this contract related to \"Indemnification\" that should be reviewed by a lawyer.",
            "answers": {
                "text": ["Vendor agrees to indemnify, defend, and hold harmless Client from any claims arising out of Vendor's gross negligence."],
                "answer_start": [245]
            }
        },
        {
            "id": "cuad_sample_002",
            "title": "BETA_LLC_NDA",
            "context_snippet": "... 4. TERMINATION. Either party may terminate this Agreement at any time upon thirty (30) days prior written notice to the other party. Upon termination, all confidential information must be destroyed.",
            "question": "Highlight the parts (if any) of this contract related to \"Notice Period To Terminate\" that should be reviewed by a lawyer.",
            "answers": {
                "text": ["upon thirty (30) days prior written notice"],
                "answer_start": [69]
            }
        }
    ]
    
    data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
    os.makedirs(data_dir, exist_ok=True)
    sample_file = os.path.join(data_dir, "cuad_sample.json")
    
    with open(sample_file, "w", encoding="utf-8") as f:
        json.dump(samples, f, indent=2)
        
    logger.info(f"Saved a sample of 2 records to: {sample_file}")
    logger.info("Open this file to see how CUAD structures its legal clauses and labels!")

if __name__ == "__main__":
    main()
