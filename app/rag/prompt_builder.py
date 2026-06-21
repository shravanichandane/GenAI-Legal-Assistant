import json
from typing import Any, Dict, List

def build_prompt(context: Dict[str, Any], evidence: List[Dict[str, str]]) -> str:
    """
    Constructs a few-shot prompt forcing the LLM to adhere to the expected JSON output structure.
    
    Args:
        context (Dict[str, Any]): The context dictionary.
        evidence (List[Dict[str, str]]): List of retrieved evidence.
        
    Returns:
        str: The constructed prompt.
    """
    context_str = json.dumps(context, indent=2)
    evidence_str = "\n".join([f"- {item['text']}" for item in evidence])
    
    prompt = f"""You are an expert legal AI assistant. Your task is to analyze a legal clause against a playbook rule and provide a structured assessment.

### CONTEXT
{context_str}

### PRECEDENT EVIDENCE
{evidence_str}

### INSTRUCTIONS
1. Analyze the 'clause' against the 'playbook_rule'.
2. Consider any 'deterministic_violations' provided.
3. Use the 'PRECEDENT EVIDENCE' as the "Gold Standard" for acceptable fallback language.
4. If a rule violation occurs, your `suggested_language` MUST strictly mirror the phrasing and structure found in the PRECEDENT EVIDENCE, adapting it only to fit the current contract's context.
5. Output your response strictly as a JSON object matching the following schema.
6. Do not include markdown formatting like ```json ... ```, just output the raw JSON object.

### JSON SCHEMA
{{
    "clause_type": "string (The type of the clause being analyzed)",
    "risk_level": "string (High, Medium, Low)",
    "risk_score": "float (0.0 to 1.0)",
    "policy_violation": "boolean",
    "violations": ["string (list of violations)"],
    "evidence": ["string (citations from the provided context or precedents)"],
    "recommendation": "string (Actionable recommendation)",
    "suggested_language": "string (Optional suggested alternative language)",
    "confidence": "float (0.0 to 1.0)"
}}

### OUTPUT
"""
    return prompt
