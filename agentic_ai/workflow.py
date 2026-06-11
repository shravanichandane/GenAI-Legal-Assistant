from typing import Dict, Any

class ExtractorAgent:
    def run(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Extracts key entities from the clause."""
        print("[Extractor Agent] Extracting entities...")
        # Mock extraction logic
        state["extracted_entities"] = ["Acme Corp", "$50,000"]
        return state

class ClassifierAgent:
    def run(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Classifies the clause type based on the text."""
        print("[Classifier Agent] Classifying clause...")
        text = state["text"].lower()
        if "liability" in text or "exceed" in text:
            state["classification"] = "LIMITATION_OF_LIABILITY"
            state["confidence"] = 0.95
        else:
            state["classification"] = "UNKNOWN"
            state["confidence"] = 0.40
        return state

class CriticAgent:
    def run(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Critiques the classification to prevent hallucination/heading sensitivity."""
        print("[Critic Agent] Verifying classification evidence...")
        if state["classification"] == "LIMITATION_OF_LIABILITY":
            if "$50,000" in state["extracted_entities"]:
                state["verification_status"] = "APPROVED"
                state["critic_feedback"] = "Evidence found: Monetary cap aligns with liability limitation."
            else:
                state["verification_status"] = "REJECTED"
                state["critic_feedback"] = "No monetary cap found to support liability limitation."
        return state

class LegalAgenticWorkflow:
    """
    A simplified representation of a LangGraph State Machine Workflow.
    Data flows from Agent to Agent, carrying the 'state' dictionary.
    """
    def __init__(self):
        self.extractor = ExtractorAgent()
        self.classifier = ClassifierAgent()
        self.critic = CriticAgent()
        
    def process_clause(self, clause_text: str) -> Dict[str, Any]:
        state = {"text": clause_text}
        
        # Sequential Graph Execution
        state = self.extractor.run(state)
        state = self.classifier.run(state)
        state = self.critic.run(state)
        
        return state

if __name__ == "__main__":
    workflow = LegalAgenticWorkflow()
    
    sample_text = "The Vendor's total aggregate liability shall not exceed $50,000."
    print(f"Processing Clause: '{sample_text}'\n")
    
    final_state = workflow.process_clause(sample_text)
    
    print("\n--- Final Agentic Output ---")
    for key, value in final_state.items():
        print(f"{key}: {value}")
