import logging
import time
from typing import Dict, Any, List, Tuple

from app.parsers.document_parser import HierarchicalParser
from app.models.legal_bert_classifier import LegalBertClassifier
from app.playbooks.retriever import get_playbook_rule
from app.playbooks.risk_rules import evaluate_clause_risk
from app.retrieval.embedder import Embedder
from app.retrieval.faiss_index import FaissIndex
from app.retrieval.retriever import Retriever
from app.retrieval.reranker import CrossEncoderReranker
from app.rag.generator import RAGPipeline
from app.rag.providers.gemini import GeminiLLMProvider
from app.rag.providers.mock import MockLLMProvider
from app.risk_engine.aggregator import RiskAggregator
from app.explainability.evidence_trace import EvidenceTracer
from app.config import settings

logger = logging.getLogger(__name__)

class ContractAnalysisPipeline:
    """
    The Brain Controller: Orchestrates the entire AI reasoning engine.
    """
    
    def __init__(self, use_mock_llm: bool = False):
        logger.info("Initializing ContractAnalysisPipeline...")
        
        # 1. NLP Models
        self.classifier = LegalBertClassifier()
        
        # 2. Retrieval System
        # Note: In a real production system, the FAISS index would be loaded from disk or a vector DB.
        # Here we initialize an empty one for the session, but we could populate it with precedents.
        self.embedder = Embedder()
        self.faiss_index = FaissIndex(embedding_dimension=384) # Default for all-MiniLM-L6-v2
        self.retriever = Retriever(embedder=self.embedder, faiss_index=self.faiss_index)
        
        # Load CUADv1 dataset into FAISS index
        try:
            import json
            import os
            # Use absolute or relative path that works
            cuad_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data", "CUADv1.json"))
            if os.path.exists(cuad_path):
                logger.info(f"Seeding FAISS from {cuad_path} (Loading first 500 precedents for speed)")
                with open(cuad_path, "r", encoding="utf-8") as f:
                    cuad_data = json.load(f)
                
                precedents = []
                # Parse SQuAD format
                for doc in cuad_data.get("data", []):
                    for paragraph in doc.get("paragraphs", []):
                        for qa in paragraph.get("qas", []):
                            for answer in qa.get("answers", []):
                                text = answer.get("text", "").strip()
                                if text and len(text) > 10:
                                    precedents.append(text)
                                    if len(precedents) >= 500:
                                        break
                            if len(precedents) >= 500:
                                break
                    if len(precedents) >= 500:
                        break
                        
                self.seed_precedents(precedents)
                logger.info(f"FAISS index seeded with {len(precedents)} CUAD precedents.")
            else:
                logger.warning(f"CUAD dataset not found at {cuad_path}. Index will be empty.")
        except Exception as e:
            logger.error(f"Failed to seed FAISS: {e}")
            
        try:
            self.reranker = CrossEncoderReranker(mode="production")
        except Exception as e:
            logger.warning(f"Could not load reranker: {e}")
            self.reranker = None
            
        # 3. LLM Reasoning
        if not use_mock_llm and settings.GOOGLE_API_KEY:
            self.llm_provider = GeminiLLMProvider(api_key=settings.GOOGLE_API_KEY, model=settings.LLM_MODEL_NAME)
        else:
            self.llm_provider = MockLLMProvider()
            
        self.rag_pipeline = RAGPipeline(provider=self.llm_provider)
        
        # 4. Deterministic Engines
        self.risk_aggregator = RiskAggregator()
        self.tracer = EvidenceTracer()
        
        logger.info("ContractAnalysisPipeline initialized.")

    def seed_precedents(self, precedents: List[str]):
        """Helper to seed the FAISS index with precedent clauses."""
        if precedents:
            self.retriever.add_documents(precedents)

    async def process_clause(self, clause_dict: Dict[str, Any]) -> Tuple[Any, Any]:
        clause_text = clause_dict.get("text", "")
        if not clause_text.strip():
            return None, None
            
        import asyncio
        # Step 2: Classify Clause in thread
        clause_type, confidence = await asyncio.to_thread(self.classifier.predict, clause_text)
        
        # Step 3: Fetch Playbook Rule
        playbook_rule = await asyncio.to_thread(get_playbook_rule, clause_type)
        playbook_text = playbook_rule.preferred_language if playbook_rule else "No specific rule available."
        playbook_rule_id = playbook_rule.clause_type if playbook_rule else "none"
        
        # Step 4: Deterministic Risk Check
        deterministic_violations = []
        
        # Step 5 & 6: Retrieval & Reranking in thread
        retrieval_res = await asyncio.to_thread(self.retriever.retrieve, clause_text, 10)
        docs = [item["metadata"]["text"] for item in retrieval_res["results"]]
        
        if self.reranker and docs:
            reranked = await asyncio.to_thread(self.reranker.rerank, clause_text, docs, 3)
            evidence = [{"id": f"prec_{i}", "text": res["text"]} for i, res in enumerate(reranked)]
        else:
            evidence = [{"id": f"prec_{i}", "text": text} for i, text in enumerate(docs[:3])]
            
        if not evidence:
            logger.warning("FAISS retrieved no evidence for clause.")
            evidence = []
            
        # Step 7: Gemini Reasoning
        from app.rag.context_builder import build_context
        from app.rag.prompt_builder import build_prompt
        import json
        from app.rag.schemas import RAGResponse
        
        context = build_context(clause_text, playbook_text, deterministic_violations)
        prompt = build_prompt(context, evidence)
        raw_response = await self.llm_provider.generate(prompt)
        
        try:
            raw_response = raw_response.strip()
            if raw_response.startswith("```json"):
                raw_response = raw_response[7:]
            if raw_response.startswith("```"):
                raw_response = raw_response[3:]
            if raw_response.endswith("```"):
                raw_response = raw_response[:-3]
                
            parsed_json = json.loads(raw_response.strip())
            validated_json = self.rag_pipeline.validator.validate(parsed_json, context, evidence)
            
            clause_id = clause_dict.get("id", f"clause_{time.time()}")
            validated_json["clause_id"] = clause_id
            validated_json["text_snippet"] = clause_text[:200] + "..." if len(clause_text) > 200 else clause_text
            
            rag_resp = RAGResponse(**validated_json)
            
            trace = self.tracer.create_trace(
                llm_output=raw_response,
                clause_id=clause_id,
                faiss_id=evidence[0]["id"] if evidence else "none",
                playbook_rule_id=playbook_rule_id
            )
            return rag_resp, trace
            
        except Exception as e:
            logger.error(f"Failed to process clause {clause_type}: {e}")
            return None, None

    async def analyze(self, contract_text: str) -> Dict[str, Any]:
        """
        Executes the full end-to-end pipeline concurrently.
        """
        start_time = time.time()
        import asyncio
        
        # Step 1: Parse Contract
        logger.info("Parsing document...")
        flat_clauses = HierarchicalParser.extract_flat_clauses(contract_text)
        
        # Step 2-8: Process all clauses concurrently
        tasks = [self.process_clause(c) for c in flat_clauses]
        results = await asyncio.gather(*tasks)
        
        rag_responses = []
        traces = []
        for resp, trace in results:
            if resp and trace:
                rag_responses.append(resp)
                traces.append(trace)
                
        # Step 9: Aggregate Risk Score
        evaluation = self.risk_aggregator.evaluate_contract(rag_responses)
        
        end_time = time.time()
        logger.info(f"Pipeline completed in {end_time - start_time:.2f}s")
        
        return {
            "status": "success",
            "processing_time": end_time - start_time,
            "overall_score": evaluation["score"],
            "overall_status": evaluation["status"],
            "clauses_analyzed": len(flat_clauses),
            "risks": [resp.dict() for resp in rag_responses],
            "traces": traces
        }

# Global singleton
pipeline_instance = None

def get_pipeline():
    global pipeline_instance
    if pipeline_instance is None:
        pipeline_instance = ContractAnalysisPipeline()
    return pipeline_instance
