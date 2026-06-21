import logging
from typing import Tuple, List, Any
import torch

logger = logging.getLogger(__name__)

class LegalBertClassifier:
    """
    Phase 3 Legal-BERT Inference Pipeline.
    
    Uses sentence-transformers with a legally fine-tuned model (NchuNLP/Legal-Sentence-RoBERTa)
    to generate embeddings for clauses and playbook rules. Cosine similarity is used 
    to classify the clauses against the rules.
    """
    
    def __init__(self):
        try:
            logger.info("Initializing LegalBertClassifier with NchuNLP/Legal-Sentence-RoBERTa...")
            from sentence_transformers import SentenceTransformer, util
            self.util = util
            # Use a robust, legal-specific sentence transformer to avoid standard BERT anisotropy
            self.model = SentenceTransformer("NchuNLP/Legal-Sentence-RoBERTa")
            logger.info("LegalBertClassifier initialized successfully.")
        except ImportError:
            logger.error("sentence-transformers is not installed.")
            self.model = None
            self.util = None
        except Exception as e:
            logger.error(f"Failed to initialize sentence-transformers pipeline: {e}")
            self.model = None
            self.util = None

    def encode(self, texts: List[str]) -> Any:
        """
        Generates embeddings for a list of texts.
        """
        if not self.model or not texts:
            return None
        return self.model.encode(texts, convert_to_tensor=True)

    def compute_similarity(self, clause_embedding: Any, rule_embeddings: Any) -> Tuple[int, float]:
        """
        Computes cosine similarity between a clause embedding and a list of rule embeddings.
        Returns the (best_match_index, highest_similarity_score).
        """
        if not self.util or clause_embedding is None or rule_embeddings is None:
            return -1, 0.0
            
        cosine_scores = self.util.cos_sim(clause_embedding, rule_embeddings)[0]
        best_match_idx = torch.argmax(cosine_scores).item()
        best_score = cosine_scores[best_match_idx].item()
        
        return best_match_idx, best_score
