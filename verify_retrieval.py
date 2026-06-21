import asyncio
import logging
from app.services.pipeline import get_pipeline

logging.basicConfig(level=logging.INFO)

async def test():
    # 1. Initialize Pipeline (this will seed the DB with CUAD data)
    print("\n--- Initializing Pipeline (FAISS Seeding) ---")
    pipeline = get_pipeline()
    
    print("\n--- FAISS Index Size ---")
    print(f"Total documents in FAISS index: {len(pipeline.retriever.documents)}")
    
    # 2. Process a Mock Clause
    print("\n--- Processing Clause ---")
    mock_clause = {
        "text": "The Distributor agrees to indemnify, defend, and hold harmless the Company from any claims, damages, liabilities, and expenses arising out of the Distributor's gross negligence or willful misconduct.",
        "id": "test_clause_001"
    }
    
    resp, trace = await pipeline.process_clause(mock_clause)
    
    if trace:
        print("\n✅ Verification Successful!")
        print(f"Clause classified as: {trace['playbook_rule_id']}")
        print(f"Evidence retrieved: {trace['faiss_id']}")
    else:
        print("\n❌ Verification Failed: Pipeline returned None.")

if __name__ == "__main__":
    asyncio.run(test())
