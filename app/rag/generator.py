import json
from typing import List, Optional, Dict
from pydantic import ValidationError

from .schemas import RAGResponse
from .context_builder import build_context
from .prompt_builder import build_prompt
from .grounding import GroundingValidator
from .providers.base import BaseLLMProvider

class RAGPipeline:
    """
    Orchestrator for the RAG Pipeline.
    Ties together context building, evidence selection, prompt construction, generation, and validation.
    """
    
    def __init__(self, provider: BaseLLMProvider):
        """
        Initialize the RAG Pipeline with a specific LLM provider.
        
        Args:
            provider (BaseLLMProvider): An instance of an LLM provider.
        """
        self.provider = provider
        self.validator = GroundingValidator()
        
    async def run(self, clause: str, playbook_rule: str, deterministic_violations: List[str], evidence: List[Dict[str, str]] = None) -> RAGResponse:
        """
        Executes the RAG pipeline.
        
        Args:
            clause (str): The clause to analyze.
            playbook_rule (str): The playbook rule to evaluate against.
            deterministic_violations (List[str]): Pre-calculated deterministic violations.
            evidence (List[Dict[str, str]]): Retrieved evidence from FAISS + Reranker.
            
        Returns:
            RAGResponse: The validated structured output.
        """
        if evidence is None:
            evidence = []
            
        # 1. Build Context
        context = build_context(clause, playbook_rule, deterministic_violations)
        
        # 3. Build Prompt
        prompt = build_prompt(context, evidence)
        
        # 4. Generate Response
        raw_response = await self.provider.generate(prompt)
        
        # 5. Parse JSON
        try:
            # Clean up the response in case it contains markdown formatting
            raw_response = raw_response.strip()
            if raw_response.startswith("```json"):
                raw_response = raw_response[7:]
            if raw_response.startswith("```"):
                raw_response = raw_response[3:]
            if raw_response.endswith("```"):
                raw_response = raw_response[:-3]
                
            parsed_json = json.loads(raw_response.strip())
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse LLM response as JSON: {str(e)}\nRaw response: {raw_response}")
            
        # 6. Validate Grounding
        validated_json = self.validator.validate(parsed_json, context, evidence)
        
        # 7. Convert to Pydantic Model
        final_response = RAGResponse(**validated_json)
        
        return final_response
