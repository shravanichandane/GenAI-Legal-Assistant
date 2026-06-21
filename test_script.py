import asyncio
import logging
from app.parsers.spatial_parser import SpatialParser
from app.services.pipeline import get_pipeline

# Configure basic logging so we can see output
logging.basicConfig(level=logging.INFO)

async def test():
    with open('test_contract.pdf', 'rb') as f:
        pdf_bytes = f.read()
    
    spatial_clauses = SpatialParser.parse_pdf(pdf_bytes)
    print(f'Parsed {len(spatial_clauses)} spatial clauses.')
    for c in spatial_clauses:
        print(f"Text: {c['text']} -> Box: {c['boundingBox']}")
        
    pipeline = get_pipeline()
    print('Running pipeline analysis...')
    res = await pipeline.analyze('Dummy text', organization_id=None, spatial_clauses=spatial_clauses)
    print('Risks found:')
    for r in res['risks']:
        print(f"Type: {r['clause_type']} -> Box: {r.get('boundingBox')}")

if __name__ == '__main__':
    asyncio.run(test())
