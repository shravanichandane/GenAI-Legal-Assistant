import json
from .base import BaseLLMProvider

class MockLLMProvider(BaseLLMProvider):
    """
    A mock LLM provider that returns a hardcoded, valid JSON string.
    Useful for testing the pipeline without incurring API costs.
    """
    
    async def generate(self, prompt: str) -> str:
        """
        Returns a mock JSON response.
        """
        mock_response = {
            "clause_type": "Limitation of Liability",
            "risk_level": "High",
            "risk_score": 0.85,
            "policy_violation": True,
            "violations": ["Liability is not capped at the contract value."],
            "evidence": ["Precedent 1: Limitation of liability is capped at 1x contract value."],
            "recommendation": "Revise the clause to cap liability at 1x the total contract value.",
            "suggested_language": "In no event shall either party's aggregate liability exceed the total amounts paid under this Agreement.",
            "confidence": 0.9
        }
        return json.dumps(mock_response)
