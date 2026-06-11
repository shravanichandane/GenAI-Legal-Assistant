# LegalSight Case Study: Non-Disclosure Agreement (NDA)

## 1. Context
This case study demonstrates the LegalSight pipeline analyzing a standard Non-Disclosure Agreement, focusing on a problematic indemnification clause often sneaked into mutual NDAs.

## 2. Mock Clause
**Clause ID:** `clause_nda_001`
> "Receiving Party shall indemnify, defend, and hold harmless the Disclosing Party from and against any and all claims, losses, liabilities, damages, and expenses (including attorney's fees) arising out of or related to any breach of this Agreement by the Receiving Party."

## 3. Playbook Violation
**Playbook Rule ID:** `rule_nda_indemnity_04`
**Rule Description:** Mutual NDAs should not contain indemnification clauses. Breach of contract remedies are sufficient for unauthorized disclosure.

## 4. Risk Assessment
### Risk Score: HIGH

## 5. Explainability Trace
**Trace ID:** `trace_8f9a2b1c`
**FAISS Retrieval ID:** `faiss_doc_782`

**System Trace Record:**
```json
{
  "llm_output": "The clause introduces an asymmetric indemnification obligation in what should be a mutual NDA. This exposes the Receiving Party to unlimited liability and attorney's fees.",
  "evidence": {
    "clause_id": "clause_nda_001",
    "faiss_id": "faiss_doc_782",
    "playbook_rule_id": "rule_nda_indemnity_04"
  }
}
```

**Risk Explanation:**
- **Factor**: Inclusion of indemnification in a standard NDA.
- **Factor**: Requirement to cover "attorney's fees" shifts standard litigation cost rules.
- **Recommended Mitigation**: Strike the entire indemnification clause. Standard breach of contract claims provide adequate remedy for disclosure violations.
