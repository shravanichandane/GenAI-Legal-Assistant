"""
Evidence Trace utility for linking LLM outputs to specific evidence points.
"""
from typing import Dict, Any, Optional
import uuid
import time

class EvidenceTracer:
    """
    Links Gemini LLM output to a specific parsed clause_id, 
    retrieved faiss_id, and playbook_rule_id.
    """
    def __init__(self):
        self.traces = []

    def create_trace(
        self, 
        llm_output: str, 
        clause_id: str, 
        faiss_id: str, 
        playbook_rule_id: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Create a new evidence trace.
        """
        trace_id = f"trace_{uuid.uuid4().hex[:8]}"
        
        trace = {
            "trace_id": trace_id,
            "timestamp": time.time(),
            "llm_output": llm_output,
            "evidence": {
                "clause_id": clause_id,
                "faiss_id": faiss_id,
                "playbook_rule_id": playbook_rule_id
            },
            "metadata": metadata or {}
        }
        self.traces.append(trace)
        return trace
        
    def get_trace(self, trace_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve a specific trace by ID."""
        for t in self.traces:
            if t["trace_id"] == trace_id:
                return t
        return None
        
    def get_all_traces(self):
        """Retrieve all recorded traces."""
        return self.traces
