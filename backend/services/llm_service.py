### backend/services/llm_service.py

import os
import json
from typing import List, Dict, Any
import logging
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

class GeminiLLMService:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("GOOGLE_API_KEY")
        # AI turned optional; default to rule-based (no hard deps on LangChain)
        self.llm = None
        self._local_classifier = None
        if not self.api_key:
            logger.warning("GOOGLE_API_KEY not found. AI features will be disabled.")
        else:
            try:
                # Prefer direct google-generativeai usage if desired in future
                import google.generativeai as genai  # type: ignore
                genai.configure(api_key=self.api_key)
                self.llm = genai.GenerativeModel("gemini-1.5-flash")
            except Exception as e:
                logger.error(f"Failed to initialize Gemini API: {e}")
                self.llm = None
    
    def extract_clauses(self, document_text: str) -> List[Dict[str, Any]]:
        """Extract clauses from document text using actual text analysis"""
        if not self.llm:
            return self._extract_clauses_fallback(document_text)
        
        # Build prompt dynamically (used only if self.llm is available)
        try:
            # Gemini 1.5 Flash handles up to 1M tokens natively, no need to chunk/truncate
            prompt_text = (
                "Analyze the following legal document and extract ALL significant clauses. For each clause, provide:\n"
                "1. The exact clause text from the document\n"
                "2. A clause type (LIABILITY, INDEMNITY, TERMINATION, PAYMENT, CONFIDENTIALITY, INTELLECTUAL_PROPERTY, GENERAL)\n"
                "3. A brief description of what the clause covers\n\n"
                "Return ONLY a valid JSON array with no additional text. Each object should have keys: clause_text, clause_type, description.\n\n"
                f"Document text:\n{document_text}\n"
            )
            
            # Use JSON response format for deterministic structure
            response = self.llm.generate_content(
                prompt_text,
                generation_config={"response_mime_type": "application/json"}
            )
            
            try:
                all_clauses = json.loads(response.text)
                if not isinstance(all_clauses, list):
                    all_clauses = [all_clauses] if isinstance(all_clauses, dict) else []
                return all_clauses
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse JSON from Gemini: {e}")
                return self._extract_clauses_fallback(document_text)
            
        except Exception as e:
            logger.error(f"Error extracting clauses with Gemini: {e}")
            return self._extract_clauses_fallback(document_text)
    
    def _get_local_classifier(self):
        if self._local_classifier is None:
            from app.models.legal_bert_classifier import LegalBertClassifier
            self._local_classifier = LegalBertClassifier()
        return self._local_classifier

    def _extract_clauses_fallback(self, document_text: str) -> List[Dict[str, Any]]:
        """Extract clauses using local LegalBert model fallback powered by the new HierarchicalParser"""
        if not document_text or len(document_text.strip()) < 50:
            return []
        
        # IMPORT PARSER HERE to avoid circular imports during startup
        from app.parsers.document_parser import HierarchicalParser
        
        # Flatten the tree so we have a linear list of clauses to classify
        flat_nodes = HierarchicalParser.extract_flat_clauses(document_text)
        
        classifier = self._get_local_classifier()
        
        extracted_clauses = []
        
        for node in flat_nodes:
            text = node.get("text", "")
            if len(text) < 20: continue # Skip very short structural fragments
            
            clause_type, confidence = classifier.predict(text)
            
            # If we matched a specific type, or it's a substantive paragraph
            if clause_type != "GENERAL" or len(text) > 100:
                # Carry over hierarchical metadata!
                extracted_clauses.append({
                    "id": node.get("id"),
                    "clause_text": text,
                    "clause_type": clause_type,
                    "description": f"Clause related to {clause_type.lower().replace('_', ' ')} (confidence: {confidence:.2f})",
                    "section_number": node.get("section_number"),
                    "metadata": node.get("metadata", {})
                })
        
        return extracted_clauses
    
    def summarize_clause(self, clause_text: str) -> str:
        """Generate AI summary for a clause"""
        if not self.llm:
            return self._generate_rule_based_summary(clause_text)
        
        try:
            prompt_text = (
                "Provide a concise, professional summary of this legal clause in 2-3 sentences. "
                "Focus on the key obligations, rights, and implications for both parties.\n\n"
                f"Clause: {clause_text}"
            )
            response = self.llm.generate_content(prompt_text)
            return response.text.strip()
        except Exception as e:
            logger.error(f"Error summarizing clause: {e}")
            return self._generate_rule_based_summary(clause_text)
    
    def _generate_rule_based_summary(self, clause_text: str) -> str:
        """Generate rule-based summary when AI is not available"""
        text_lower = clause_text.lower()
        
        # Identify key terms and generate appropriate summary
        if any(term in text_lower for term in ["indemnify", "hold harmless"]):
            return "Indemnification clause that outlines protection obligations and liability allocation between parties."
        elif any(term in text_lower for term in ["terminate", "termination"]):
            return "Termination clause specifying conditions and procedures for ending the agreement."
        elif any(term in text_lower for term in ["payment", "pay", "fee"]):
            return "Payment clause defining financial obligations, terms, and payment schedules."
        elif any(term in text_lower for term in ["confidential", "non-disclosure"]):
            return "Confidentiality clause establishing obligations to protect sensitive information."
        elif any(term in text_lower for term in ["liability", "damages", "liable"]):
            return "Liability clause defining responsibility for damages and limitation of liability."
        else:
            # Extract first meaningful sentence for general clauses
            sentences = [s.strip() for s in clause_text.split('.') if len(s.strip()) > 20]
            if sentences:
                return f"This clause establishes specific terms and obligations. Key provisions include: {sentences[0][:100]}..."
            return "General contract provision establishing rights and obligations between parties."
    
    def analyze_risk(self, clause_text: str, clause_type: str) -> Dict[str, Any]:
        """Analyze risk level and score for a clause"""
        if not self.llm:
            return self._analyze_risk_rule_based(clause_text, clause_type)
        
        try:
            prompt_text = (
                f"Analyze the risk level of this {clause_type} clause on a scale of 0-10 where:\n"
                "- 0-3: LOW risk (minimal impact, standard terms)\n"
                "- 4-6: MEDIUM risk (moderate impact, some concerns)\n"
                "- 7-10: HIGH risk (significant impact, major liability)\n\n"
                "Consider factors like liability exposure, financial impact, enforceability, and potential disputes.\n"
                "Return ONLY a JSON object with keys: risk_score (float), risk_level (string), reasoning (string).\n\n"
                f"Clause: {clause_text}"
            )
            response = self.llm.generate_content(prompt_text)
            result = json.loads(response.text)
            
            # Validate and normalize the response
            risk_score = float(result.get('risk_score', 3.0))
            risk_score = max(0.0, min(10.0, risk_score))  # Clamp between 0-10
            
            if risk_score <= 3.0:
                risk_level = 'LOW'
            elif risk_score <= 6.0:
                risk_level = 'MEDIUM'
            else:
                risk_level = 'HIGH'
            
            return {
                'risk_score': round(risk_score, 2),
                'risk_level': risk_level,
                'reasoning': result.get('reasoning', 'AI risk assessment based on clause analysis')
            }
            
        except Exception as e:
            logger.error(f"Error analyzing risk with Gemini: {e}")
            return self._analyze_risk_rule_based(clause_text, clause_type)
    
    def _analyze_risk_rule_based(self, clause_text: str, clause_type: str) -> Dict[str, Any]:
        """Rule-based risk analysis when AI is not available"""
        text_lower = clause_text.lower()
        
        # Base risk scores by clause type
        base_scores = {
            "INDEMNITY": 7.5,
            "LIABILITY": 7.0,
            "TERMINATION": 4.0,
            "PAYMENT": 3.0,
            "CONFIDENTIALITY": 5.0,
            "INTELLECTUAL_PROPERTY": 6.0,
            "GENERAL": 2.0
        }
        
        base_score = base_scores.get(clause_type, 3.0)
        
        # Adjust based on high-risk terms
        high_risk_terms = [
            "unlimited", "uncapped", "consequential damages", "punitive damages",
            "liquidated damages", "immediate termination", "without notice",
            "personal guarantee", "joint and several", "successor liability"
        ]
        
        medium_risk_terms = [
            "limited liability", "reasonable", "material breach", 
            "30 days notice", "cure period", "confidential information"
        ]
        
        # Count risk indicators
        high_risk_count = sum(1 for term in high_risk_terms if term in text_lower)
        medium_risk_count = sum(1 for term in medium_risk_terms if term in text_lower)
        
        # Adjust score based on risk indicators
        adjusted_score = base_score + (high_risk_count * 1.5) + (medium_risk_count * 0.5)
        adjusted_score = max(0.0, min(10.0, adjusted_score))
        
        # Determine risk level
        if adjusted_score <= 3.0:
            risk_level = 'LOW'
        elif adjusted_score <= 6.0:
            risk_level = 'MEDIUM'  
        else:
            risk_level = 'HIGH'
        
        # Generate reasoning based on analysis
        reasoning_parts = []
        if clause_type in ["INDEMNITY", "LIABILITY"]:
            reasoning_parts.append("High-impact clause type")
        if high_risk_count > 0:
            reasoning_parts.append(f"Contains {high_risk_count} high-risk terms")
        if medium_risk_count > 0:
            reasoning_parts.append(f"Contains {medium_risk_count} moderate risk indicators")
        
        reasoning = "; ".join(reasoning_parts) if reasoning_parts else f"Standard {clause_type.lower()} clause"
        
        return {
            "risk_score": round(adjusted_score, 2),
            "risk_level": risk_level,
            "reasoning": f"Rule-based analysis: {reasoning}"
        }
    
    # Remove all mock methods - deleted
    
# Global instance
llm_service = GeminiLLMService()
