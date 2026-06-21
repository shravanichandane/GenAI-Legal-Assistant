import asyncio
import logging
from app.db.database import SessionLocal, engine, Base
from app.db.models import PlaybookRule, Organization
from app.services.pipeline import get_pipeline

# Configure logging
logging.basicConfig(level=logging.WARNING)

Base.metadata.create_all(bind=engine)

db = SessionLocal()
org = db.query(Organization).first()
if not org:
    org = Organization(name='Default Org')
    db.add(org)
    db.commit()
    db.refresh(org)

# Clear existing rules for clean test
db.query(PlaybookRule).delete()
db.commit()

# Create rule
rule = PlaybookRule(
    organization_id=org.id,
    clause_type='Liability',
    rule_description='Under no circumstances should we accept uncapped liability. The absolute maximum liability cap we can accept is $50,000.',
    is_mandatory=True
)
db.add(rule)
db.commit()

async def test():
    pipeline = get_pipeline()
    contract_text = 'This Master Services Agreement... Provider liability shall be capped at $1,000,000. Indemnification shall be mutual.'
    result = await pipeline.analyze(contract_text)
    
    print('\n--- Analysis Results ---')
    print('Overall Score:', result['overall_score'])
    for risk in result['risks']:
        print(f"Risk Level: {risk.get('risk_level')}")
        print(f"Summary: {risk.get('summary')}")
        print(f"Recommendation: {risk.get('recommendation')}")
        print("---")

if __name__ == "__main__":
    asyncio.run(test())
